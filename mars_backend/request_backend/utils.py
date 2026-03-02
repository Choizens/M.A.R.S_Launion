from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_submission_confirmation(file_request):
    """
    Sends an email to the student confirming their request submission.
    Includes the passkey for tracking.
    """
    subject = f"Request Received - M.A.R.S [Passkey: {file_request.passkey}]"
    
    # Formulate the message
    message = f"""
Dear {file_request.first_name} {file_request.last_name},

Thank you for your request. We have received your submission for the following documents:
{', '.join(file_request.requested_files)}

Your Passkey is: {file_request.passkey}
Please keep this passkey safe as you will need it to check your request status at: https://mars-launion.vercel.app/

Status: {file_request.status}

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
        print(f"Error sending submission confirmation: {e}")

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
