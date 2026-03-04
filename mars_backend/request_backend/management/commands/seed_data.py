from django.core.management.base import BaseCommand
from django.utils import timezone
from request_backend.models import Strand, DocumentType, PickupSlot, Student, Staff, FileRequest
import datetime

class Command(BaseCommand):
    help = 'Seeds initial data for the M.A.R.S system'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # 1. Seed Strands
        strands = [
            {'name': 'STEM', 'description': 'Science, Technology, Engineering, and Mathematics'},
            {'name': 'ABM', 'description': 'Accountancy, Business, and Management'},
            {'name': 'HUMSS', 'description': 'Humanities and Social Sciences'},
            {'name': 'GAS', 'description': 'General Academic Strand'},
            {'name': 'TVL', 'description': 'Technical-Vocational-Livelihood'},
        ]
        for s_data in strands:
            strand, created = Strand.objects.get_or_create(name=s_data['name'], defaults={'description': s_data['description']})
            if created:
                self.stdout.write(f'Created Strand: {strand.name}')

        # 2. Seed DocumentTypes
        docs = [
            {'name': 'Transcript of Records (TOR)', 'price': 100.00, 'description': 'Official transcript of records.'},
            {'name': 'Diploma', 'price': 150.00, 'description': 'Official school diploma.'},
            {'name': 'Certificate of Enrollment', 'price': 50.00, 'description': 'Proof of current enrollment.'},
            {'name': 'Good Moral Certificate', 'price': 75.00, 'description': 'Certificate of good moral character.'},
            {'name': 'Form 137', 'price': 100.00, 'description': 'Student Permanent Record.'},
            {'name': 'Form 138', 'price': 50.00, 'description': 'Report Card.'},
        ]
        for d_data in docs:
            doc, created = DocumentType.objects.get_or_create(name=d_data['name'], defaults={'price': d_data['price'], 'description': d_data['description']})
            if created:
                self.stdout.write(f'Created DocumentType: {doc.name}')

        # 3. Seed PickupSlots (Next 7 days)
        today = timezone.now().date()
        for i in range(1, 8):
            slot_date = today + datetime.timedelta(days=i)
            # Skip weekends (optional, but realistic)
            if slot_date.weekday() < 5:
                slot, created = PickupSlot.objects.get_or_create(date=slot_date, defaults={'morning_slots': 10, 'afternoon_slots': 10})
                if created:
                    self.stdout.write(f'Created PickupSlot: {slot.date}')

        # 4. Seed a Sample Student
        stem_strand = Strand.objects.filter(name='STEM').first()
        student_data = {
            'lrn_number': '123456789012',
            'first_name': 'John',
            'last_name': 'Doe',
            'middle_name': 'Sample',
            'sex': 'Male',
            'year_graduated': '2024',
            'strand_type': stem_strand,
            'email': 'john.doe@example.com',
            'phone_number': '09123456789',
            'permanent_address': '123 Sample St, Cabadbaran City, La Union',
        }
        student, created = Student.objects.get_or_create(lrn_number=student_data['lrn_number'], defaults=student_data)
        if created:
            self.stdout.write(f'Created Student: {student.first_name} {student.last_name}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
