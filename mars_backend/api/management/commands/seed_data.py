import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from request_backend.models import (
    Staff, Strand, Student, FileRequest, AuditLog, 
    PickupSlot, DocumentType
)

class Command(BaseCommand):
    help = 'Seeds the database with sample data for all models.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting data seeding..."))

        # 1. Strand
        strands_data = [
            ("STEM", "Science, Technology, Engineering, and Mathematics"),
            ("ABM", "Accountancy, Business, and Management"),
            ("HUMSS", "Humanities and Social Sciences"),
            ("GAS", "General Academic Strand"),
            ("TVL", "Technical-Vocational-Livelihood Track"),
        ]
        strand_objs = []
        for name, desc in strands_data:
            strand, created = Strand.objects.get_or_create(name=name, defaults={'description': desc})
            strand_objs.append(strand)
            if created: self.stdout.write(f"Created Strand: {name}")

        # 2. DocumentType
        docs_data = [
            ("Form 137", "Permanent Record (Student’s Permanent Record)", 50.00),
            ("Diploma", "Certificate of Graduation", 150.00),
            ("Certificate of Good Moral", "Character verification", 75.00),
            ("Transcript of Records", "Detailed academic records", 100.00),
            ("Certification of Enrollment", "Proof of current status", 30.00),
            ("Graduation Certificate", "Official proof of graduation", 50.00),
            ("Honorable Dismissal", "Transfer credential", 100.00),
            ("CAV (Certification, Authentication, Verification)", "For DFA/Abroad use", 200.00),
        ]
        doc_type_objs = []
        for name, desc, price in docs_data:
            doc_type, created = DocumentType.objects.get_or_create(
                name=name, 
                defaults={'description': desc, 'price': price}
            )
            doc_type_objs.append(doc_type)
            if created: self.stdout.write(f"Created DocumentType: {name}")

        # ... (Staff seeding) ...
        staff_data = [
            ('registrar_user', 'reg123!', 'registrar@example.com', 'S-2024-010', 'Registrar', 'Emma Watson'),
            ('office_user', 'off123!', 'office@example.com', 'S-2024-011', 'Admin Office', 'Tom Hanks'),
        ]
        staff_objs = []
        for username, pwd, email, sid, dept, name in staff_data:
            if not Staff.objects.filter(username=username).exists():
                staff = Staff.objects.create_user(
                    username=username, password=pwd, email=email, 
                    staff_id=sid, department=dept, full_name=name
                )
                staff_objs.append(staff)
                self.stdout.write(f"Created Staff: {username}")
            else:
                staff_objs.append(Staff.objects.get(username=username))

        # 4. Student
        students_data = [
            ('123456789001', 'John', 'Quincy', 'Doe', '', 'Male', '2023', random.choice(strand_objs), 'john@example.com', '09123456789', 'City A'),
            ('123456789002', 'Jane', 'Marie', 'Smith', '', 'Female', '2024', random.choice(strand_objs), 'jane@example.com', '09987654321', 'City B'),
            ('123456789003', 'Bobby', '', 'Brown', 'Jr.', 'Male', '2022', random.choice(strand_objs), 'bobby@example.com', '09112233445', 'City C'),
        ]
        student_objs = []
        from request_backend.models import StudentMasterDocument
        from django.core.files.base import ContentFile

        for lrn, f, m, l, sfx, sex, yr, strand, email, phone, addr in students_data:
            student, created = Student.objects.get_or_create(
                lrn_number=lrn,
                defaults={
                    'first_name': f, 'middle_name': m, 'last_name': l, 'suffix': sfx,
                    'sex': sex, 'year_graduated': yr, 'strand_type': strand,
                    'email': email, 'phone_number': phone, 'permanent_address': addr
                }
            )
            student_objs.append(student)
            if created: 
                self.stdout.write(f"Created Student: {f} {l}")
            
        # Ensure ALL students in the database have sample digitized records for testing
        all_students = Student.objects.all()
        self.stdout.write(f"Verifying digitized records for {all_students.count()} students...")
        
        needed_docs = ["Form 137", "Diploma", "Graduation Certificate"]
        for student in all_students:
            seeded_any = False
            for doc_type_name in needed_docs:
                if not StudentMasterDocument.objects.filter(student=student, document_type__iexact=doc_type_name).exists():
                    dummy_file = ContentFile(b"Dummy document content", name=f"{doc_type_name.replace(' ', '_')}.pdf")
                    StudentMasterDocument.objects.create(
                        student=student,
                        document_type=doc_type_name,
                        file=dummy_file
                    )
                    seeded_any = True
            if seeded_any:
                self.stdout.write(f"Digitized sample records for {student.first_name} {student.last_name}")

        # 5. FileRequest
        for i, student in enumerate(student_objs):
            # Pick documents that the student actually HAS in StudentMasterDocument
            available_docs = student.documents.values_list('document_type', flat=True)
            if available_docs:
                requested_files = random.sample(list(available_docs), k=min(2, len(available_docs)))
                req, created = FileRequest.objects.get_or_create(
                    student=student,
                    defaults={
                        'first_name': student.first_name, 'middle_name': student.middle_name,
                        'last_name': student.last_name, 'suffix': student.suffix,
                        'sex': student.sex, 'year_graduated': student.year_graduated,
                        'strand_type': student.strand_type, 'lrn_number': student.lrn_number,
                        'email': student.email, 'phone_number': student.phone_number,
                        'permanent_address': student.permanent_address,
                        'requested_files': requested_files,
                        'status': 'Pending' if i == 0 else 'Approved' if i == 1 else 'Received',
                        'no_accountabilities': True
                    }
                )
                if created: self.stdout.write(f"Created FileRequest for: {student.first_name}")

        # 6. AuditLog
        if staff_objs:
            AuditLog.objects.create(
                user=staff_objs[0],
                action="Seeding Database",
                details="Automated data seeding command executed."
            )
            self.stdout.write("Logged seeding action.")

        # 7. PickupSlot
        today = date.today()
        for i in range(1, 8):
            future_date = today + timedelta(days=i)
            if future_date.weekday() < 5:
                PickupSlot.objects.get_or_create(
                    date=future_date,
                    defaults={'morning_slots': 15, 'afternoon_slots': 15}
                )
        self.stdout.write("Created PickupSlots for next 5 business days.")

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully."))
