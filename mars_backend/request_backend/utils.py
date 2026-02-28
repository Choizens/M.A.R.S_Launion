from django.core.mail import send_mail
from django.conf import settings


def send_submission_confirmation(request_obj):
    """
    Sends a confirmation email to the student immediately after their
    document request is submitted successfully.
    """
    name = f"{request_obj.first_name} {request_obj.last_name}"
    docs_list = "\n".join(f"  • {d}" for d in request_obj.requested_files)
    pickup = (
        f"{request_obj.pickup_date} ({request_obj.pickup_time})"
        if request_obj.pickup_date
        else "Not yet scheduled"
    )

    subject = "[Registrar] Acknowledgement of Document Request - La Union Senior High School"
    message = (
        f"Dear {name},\n\n"
        f"Greetings from the Records Office of La Union Senior High School.\n\n"
        f"This email is to formally acknowledge that we have received your request for academic documents. "
        f"Please find the summary of your transaction below:\n\n"
        f"--------------------------------------------------\n"
        f"TRANSACTION DETAILS\n"
        f"--------------------------------------------------\n"
        f"Reference Passkey : {request_obj.passkey}\n"
        f"Current Status    : {request_obj.status}\n"
        f"Scheduled Pickup  : {pickup}\n"
        f"--------------------------------------------------\n\n"
        f"REQUESTED DOCUMENTS:\n{docs_list}\n\n"
        f"IMPORTANT REMINDER:\n"
        f"Please secure your Reference Passkey. This will serve as your unique identifier to track the progress of your request through our online portal. Do not share this passkey with anyone for your privacy and security.\n\n"
        f"NEXT STEPS:\n"
        f"The Registrar's Office will now process your request and verify your records. You will be notified via email once there is an update regarding the status of your requested documents.\n\n"
        f"Should you have any urgent inquiries, please contact the school administration directly.\n\n"
        f"Thank you.\n\n"
        f"Sincerely,\n"
        f"The Registrar / Records Office\n"
        f"La Union Senior High School"
    )

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [request_obj.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"[Email Error] Submission confirmation failed: {e}")
        return False


def send_request_notification(request_obj):
    """
    Sends an email notification to the student based on the status of their request.
    """
    subject = ""
    message = ""
    status = request_obj.status
    
    # Base message template
    header = f"Dear {request_obj.first_name} {request_obj.last_name},\n\nGreetings from the Records Office of La Union Senior High School.\n\n"
    footer = f"\n\n--------------------------------------------------\nTRANSACTION REFERENCE\n--------------------------------------------------\nReference Passkey: {request_obj.passkey}\nScheduled Pickup: {request_obj.pickup_date} at {request_obj.pickup_time}\n\nShould you have any clarifications, please do not hesitate to reach out to the school administration.\n\nSincerely,\n\nThe Registrar / Records Office\nLa Union Senior High School"

    if status == 'Approved':
        subject = "[Registrar] Approved Document Request - La Union Senior High School"
        message = (
            f"{header}We are pleased to inform you that your document request has been officially APPROVED. "
            f"Your requested documents are currently being prepared by our staff.\n\n"
            f"Please ensure to bring any necessary requirements, such as valid identification and applicable fees, on your scheduled date of pickup."
            f"{footer}"
        )
    elif status == 'Completed':
        subject = "[Registrar] Document Request Completed - La Union Senior High School"
        message = (
            f"{header}This is to confirm that your requested academic documents have been successfully CLAIMED/RELEASED. "
            f"Your transaction with the Records Office is now marked as COMPLETED.\n\n"
            f"Thank you for utilizing the La Union Senior High School Document Request Portal."
            f"{footer}"
        )
    elif status == 'Needs Verification':
        subject = "[Registrar] Action Required: Record Verification - La Union Senior High School"
        message = (
            f"{header}Please be advised that your document request is currently ON HOLD pending verification. "
            f"We are currently unable to locate a digital copy of your master record within our system.\n\n"
            f"Our staff is presently conducting a manual retrieval of your file from our physical archives. Rest assured that we are taking the necessary steps to resolve this. No further action is required from your end at this moment."
            f"{footer}"
        )
    elif status == 'Rejected':
        subject = "[Registrar] Rejected Document Request - La Union Senior High School"
        message = (
            f"{header}We regret to inform you that your recent document request has been REJECTED.\n\n"
            f"This may be due to incomplete information, unresolved academic or administrative accountabilities, or other internal policies. We advise you to personally visit or contact the Records Office for further clarification regarding the rejection of your request."
            f"{footer}"
        )
    else:
        # Don't send email for other statuses unless needed
        return

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER, # Sender
            [request_obj.email],      # Recipient
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False
