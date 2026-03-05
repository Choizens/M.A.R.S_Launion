import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mars_backend.settings')
django.setup()

client = Client()

# Prepare test data
payload = {
    "first_name": "Test",
    "last_name": "User",
    "email": "another_test_user@example.com",
    "phone_number": "09123456789",
    "permanent_address": "123 Test St",
    "lrn_number": "123456789012",
    "sex": "Male",
    "year_graduated": "2024",
    "strand": "STEM",
    "requested_files": ["Form 137", "Diploma"],
    "pickup_date": "2026-04-01",
    "pickup_time": "Morning",
}

response = client.post('/api/requests/', data=payload, content_type='application/json')
print('Response status:', response.status_code)
print('Response data:', response.content.decode())
