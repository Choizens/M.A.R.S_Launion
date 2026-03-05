import os, django
from django.core.mail import send_mail, get_connection
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mars_backend.settings')
django.setup()

def test_send_email():
    subject = 'M.A.R.S Test Email'
    message = 'This is a test email from the M.A.R.S backend to verify SMTP settings.'
    recipient_list = ['dummychan70@gmail.com'] # Test with the same email as sender or provide a valid one
    
    print(f"DEBUG: Attempting to send test email to {recipient_list}...")
    try:
        sent = send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        if sent:
            print("SUCCESS: Test email sent successfully!")
        else:
            print("FAILED: send_mail returned 0 (no email sent).")
    except Exception as e:
        print(f"ERROR: Failed to send test email: {str(e)}")

if __name__ == "__main__":
    test_send_email()
