import os
import sys
import django
from django.conf import settings
from django.core.mail import send_mail, get_connection

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mars_backend.settings')
django.setup()

def test_sendgrid_connection():
    print("--- SendGrid API Diagnostic Tool ---")
    
    api_key = os.getenv('SENDGRID_API_KEY')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'knightcyberg@gmail.com')
    
    print(f"DEBUG: SENDGRID_API_KEY is {'SET' if api_key else 'NOT SET'}")
    print(f"DEBUG: DEFAULT_FROM_EMAIL: {from_email}")
    print(f"DEBUG: EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    
    if not api_key:
        print("❌ ERROR: SENDGRID_API_KEY environment variable is missing.")
        return

    recipient = input("\nEnter recipient email address for test: ").strip()
    if not recipient:
        print("❌ ERROR: Recipient email is required.")
        return

    print(f"\n🚀 Attempting to send test email to {recipient}...")
    
    try:
        subject = "M.A.R.S SendGrid Diagnostic Test"
        message = "If you are reading this, your SendGrid API configuration is working correctly!"
        
        # Test using the configured backend
        result = send_mail(
            subject,
            message,
            from_email,
            [recipient],
            fail_silently=False,
        )
        
        if result == 1:
            print("\n✅ SUCCESS! Django reported that the email was sent successfully.")
            print("Please check the recipient's inbox (and SPAM folder).")
        else:
            print("\n⚠️ WARNING: Django returned 0. This usually means the email was not sent.")
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        print("\nPossible causes:")
        print("1. [403 Forbidden] -> Your 'From' email is NOT verified in SendGrid as a Single Sender.")
        print("2. [401 Unauthorized] -> Your SENDGRID_API_KEY is invalid.")
        print("3. [Network Error] -> Check your internet connection or firewall.")
        
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sendgrid_connection()
