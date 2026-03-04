from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

def send_submission_confirmation(file_request):
    """
    Sends a rich HTML email to the student confirming their request submission.
    Includes the Passkey for tracking.
    """
    subject = f"Request Received - M.A.R.S [Passkey: {file_request.passkey}]"
    
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None) or 'noreply@mars.gov.ph'
    print(f"DEBUG: Attempting to send confirmation to {file_request.email} from {from_email}")
    
    try:
        print("DEBUG: Rendering template...")
        html_content = render_to_string('emails/request_notification.html', {
            'instance': file_request,
        })
        print(f"DEBUG: Template rendered (length: {len(html_content)})")
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [file_request.email]
        )
        email.attach_alternative(html_content, "text/html")
        print("DEBUG: Email object created, sending...")
        email.send(fail_silently=False)
        print(f"Successfully sent confirmation email to {file_request.email}")
    except Exception as e:
        import traceback
        print(f"ERROR: Failed to provide confirmation email: {str(e)}")
        traceback.print_exc()

def send_request_notification(file_request):
    """
    Sends an email to the student when their request status is updated (e.g. Approved, Completed).
    """
    subject = f"Update on your M.A.R.S Request - [Passkey: {file_request.passkey}]"
    
    status_msg = ""
    if file_request.status == 'Approved':
        status_msg = f"Your request has been APPROVED. Your pickup date is set for {file_request.pickup_date} ({file_request.pickup_time})."
    elif file_request.status == 'Completed':
        status_msg = "Your request is now COMPLETE. You can now access your digitized documents on our website."
    elif file_request.status == 'Needs Verification':
        status_msg = "Your request needs further verification. Please check your account dashboard or visit the office."
    elif file_request.status == 'Rejected':
        status_msg = "We regret to inform you that your request has been rejected. Please contact the office for more details."
    else:
        status_msg = f"The status of your request has been updated to: {file_request.status}."

    message = f"""
Dear {file_request.first_name} {file_request.last_name},

There is an update regarding your request (Passkey: {file_request.passkey}).

Current Status: {file_request.status}
{status_msg}

Best regards,
La Union SHS M.A.R.S Team
    """

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [file_request.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending request notification: {e}")

def notify_staff_new_request(file_request):
    """
    Alerts all staff members when a new request is submitted.
    """
    from .models import Staff
    # Notify ALL active accounts with administrative or staff privileges
    from django.db.models import Q
    staff_emails = Staff.objects.filter(
        Q(is_active=True) & (Q(is_staff=True) | Q(is_superuser=True))
    ).exclude(email='').values_list('email', flat=True)
    
    if not staff_emails:
        return

    subject = f"NEW Request Alert: {file_request.first_name} {file_request.last_name}"
    
    message = f"""
Attention Staff,

A new document request has been submitted to M.A.R.S.

APPLICANT: {file_request.first_name} {file_request.last_name}
STRAND: {file_request.strand}
DOCUMENTS: {', '.join(file_request.requested_files)}
PICKUP DATE: {file_request.pickup_date} ({file_request.pickup_time})

Please log in to the Admin Dashboard to review and begin processing this request.

Best regards,
M.A.R.S Automated System
    """

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None) or 'noreply@mars.gov.ph'
    
    print(f"DEBUG: Notifying staff of new request {file_request.passkey}. Recipients found: {len(staff_emails)}")
    
    try:
        send_mail(
            subject,
            message,
            from_email,
            list(staff_emails),
            fail_silently=False,
        )
        print(f"Successfully notified {len(staff_emails)} staff members about new request.")
    except Exception as e:
        print(f"ERROR: Failed to notify staff of new request: {e}")
