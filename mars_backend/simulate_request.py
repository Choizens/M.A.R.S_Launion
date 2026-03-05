import os
import django
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mars_backend.settings')
django.setup()

from request_backend.models import FileRequest, Strand
from request_backend.utils import send_submission_confirmation
from django.utils import timezone

def simulate_email():
    # Create a dummy request instance (not saved to DB to avoid clutter, or saved and then deleted)
    # Actually, the utils function might need it in the DB for some things, but maybe not.
    # Let's create a real one but with a test email.
    
    print("DEBUG: Creating dummy request...")
    strand, _ = Strand.objects.get_or_create(name="STEM")
    
    test_request = FileRequest(
        first_name="Test",
        last_name="User",
        email="dummychan70@gmail.com", # Send to the same test email
        phone_number="09123456789",
        permanent_address="Test Address",
        year_graduated="2024",
        strand="STEM",
        strand_type=strand,
        requested_files=["Form 137", "Diploma"],
        pickup_date=timezone.now().date(),
        pickup_time="Morning",
        status="Pending"
    )
    # Save to trigger passkey generation
    test_request.save()
    print(f"DEBUG: Created request with Passkey: {test_request.passkey}")
    
    try:
        print(f"DEBUG: Triggering send_submission_confirmation for {test_request.email}...")
        send_submission_confirmation(test_request)
        print("DEBUG: send_submission_confirmation call finished (thread should be running).")
        
        # Wait a bit for the thread to finish since it's a daemon thread
        import time
        print("DEBUG: Waiting 10 seconds for background thread to complete...")
        time.sleep(10)
        print("DEBUG: Simulation finished.")
        
    finally:
        # Clean up
        print("DEBUG: Cleaning up test request...")
        test_request.delete()

if __name__ == "__main__":
    simulate_email()
