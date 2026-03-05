import threading
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
    print(f"DEBUG: Attempting to send confirmation to {file_request.email}")
    print(f"DEBUG: Config - HOST: {settings.EMAIL_HOST}, PORT: {settings.EMAIL_PORT}, USER: {settings.EMAIL_HOST_USER}, FROM: {from_email}, TLS: {getattr(settings, 'EMAIL_USE_TLS', False)}, SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
    
    try:
        print("DEBUG: Rendering template...")
        html_content = render_to_string('emails/request_notification.html', {
            'instance': file_request,
            'pickup_date_fmt': file_request.pickup_date.strftime('%B %d, %Y') if file_request.pickup_date else '—',
            'pickup_time_fmt': file_request.pickup_time or '—',
            'submitted_at_fmt': file_request.submitted_at.strftime('%B %d, %Y') if file_request.submitted_at else '—',
            'status_message': "Thank you! We have received your document request. Our team will review your application and notify you once it has been processed."
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
        
        def send_email_thread():
            try:
                print(f"DEBUG: (Thread) Attempting SMTP send to {file_request.email}...")
                email.send(fail_silently=False)
                print(f"DEBUG: (Thread) SUCCESS: Confirmation email sent to {file_request.email}")
            except Exception as thread_err:
                import traceback
                print(f"DEBUG: (Thread) CRITICAL ERROR sending email to {file_request.email}: {thread_err}")
                traceback.print_exc()

        # Use daemon=False to ensure the thread has a better chance of finishing in cloud environments
        threading.Thread(target=send_email_thread, daemon=False).start()
        print(f"DEBUG: Email thread started for {file_request.email}")

    except Exception as e:
        import traceback
        print(f"ERROR: Failed to prepare confirmation email: {str(e)}")
        traceback.print_exc()

def send_request_notification(file_request):
    """
    Sends a professional HTML email to the student when their request status is updated.
    """
    subject = f"Update on your M.A.R.S Request - [Passkey: {file_request.passkey}]"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None) or 'noreply@mars.gov.ph'
    
    status_msg = ""
    if file_request.status == 'Approved':
        status_msg = f"Good news! Your request has been APPROVED. Please visit the school on {file_request.pickup_date} ({file_request.pickup_time}) to collect your documents."
    elif file_request.status == 'Completed':
        status_msg = "Your request is now COMPLETE. If you requested digitized copies, they should now be accessible via your portal."
    elif file_request.status == 'Needs Verification':
        status_msg = "A record mismatch was found. Please check your details or visit the Registrar's Office for verification."
    elif file_request.status == 'Rejected':
        status_msg = f"Your request has been set to {file_request.status.upper()}. Please contact the office if you believe this is an error."
    else:
        status_msg = f"The status of your document request has been updated to: {file_request.status}."

    print(f"DEBUG: Sending Status Update Notification ({file_request.status}) to {file_request.email}")

    try:
        html_content = render_to_string('emails/request_notification.html', {
            'instance': file_request,
            'pickup_date_fmt': file_request.pickup_date.strftime('%B %d, %Y') if file_request.pickup_date else '—',
            'pickup_time_fmt': file_request.pickup_time or '—',
            'submitted_at_fmt': file_request.submitted_at.strftime('%B %d, %Y') if file_request.submitted_at else '—',
            'status_message': status_msg
        })
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [file_request.email]
        )
        email.attach_alternative(html_content, "text/html")
        
        def send_update_thread():
            try:
                email.send(fail_silently=False)
                print(f"Successfully sent {file_request.status} notification to {file_request.email}")
            except Exception as thread_err:
                print(f"ERROR in status update thread: {thread_err}")

        threading.Thread(target=send_update_thread, daemon=True).start()
    except Exception as e:
        print(f"ERROR: Failed to prepare status update email: {e}")

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
        def notify_staff_thread():
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    list(staff_emails),
                    fail_silently=False,
                )
                print(f"Successfully notified {len(staff_emails)} staff members about new request.")
            except Exception as thread_err:
                print(f"ERROR in notify staff thread: {thread_err}")

        threading.Thread(target=notify_staff_thread, daemon=True).start()
    except Exception as e:
        print(f"ERROR: Failed to prepare staff notification: {e}")
