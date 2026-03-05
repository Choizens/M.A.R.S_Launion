import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mars_backend.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail, get_connection

def diagnose():
    print("--- EMAIL DIAGNOSTIC ---")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    if "sendgrid" in settings.EMAIL_BACKEND:
        print(f"SENDGRID_API_KEY set: {bool(os.getenv('SENDGRID_API_KEY'))}")
    elif "smtp" in settings.EMAIL_BACKEND:
        print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
        print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"EMAIL_HOST_PASSWORD set: {bool(settings.EMAIL_HOST_PASSWORD)}")
    
    print("\nAttempting to send a test email...")
    try:
        # Use a real email for testing if provided by user, else use a placeholder
        recipient = "knightcyberg@gmail.com" 
        sent = send_mail(
            'M.A.R.S Diagnostic Test',
            'If you receive this, the email system is working correctly.',
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        print(f"SUCCESS: Result of send_mail: {sent}")
    except Exception as e:
        print(f"FAILURE: Error sending email: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose()
