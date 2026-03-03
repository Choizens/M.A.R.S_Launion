import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mars_backend.settings')
django.setup()

from request_backend.models import Staff

print("Existing Staff records:")
for s in Staff.objects.all():
    print(f"Username: {s.username}, Staff ID: '{s.staff_id}'")
