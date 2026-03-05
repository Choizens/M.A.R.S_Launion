from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import string
import random


class Staff(AbstractUser):
    staff_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, default='')

    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.username


class Strand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

class Student(models.Model):
    SEX_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    
    lrn_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=20, blank=True, default='')
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    year_graduated = models.CharField(max_length=10)
    strand_type = models.ForeignKey(Strand, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    permanent_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.lrn_number})"

class FileRequest(models.Model):
    SEX_CHOICES = [('Male', 'Male'), ('Female', 'Female')]

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=20, blank=True, default='')
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    year_graduated = models.CharField(max_length=10)
    strand = models.CharField(max_length=100, blank=True, default='') # Keep for legacy/string storage
    strand_type = models.ForeignKey(Strand, on_delete=models.SET_NULL, null=True, blank=True)
    lrn_number = models.CharField(max_length=20, blank=True, default='')
    request_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    permanent_address = models.TextField()
    requested_files = models.JSONField(default=list)
    
    # New Proposal Fields
    pickup_date = models.DateField(null=True, blank=True)
    pickup_time = models.CharField(max_length=50, null=True, blank=True)
    
    # Verification Toggle from Proposal
    no_accountabilities = models.BooleanField(default=False)
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    passkey = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.passkey:
            now = timezone.now()
            year = now.year
            # Get count of requests in current year to generate sequence
            # Note: For production use a database sequence or atomic increment to avoid collisions
            count = FileRequest.objects.filter(submitted_at__year=year).count() + 1
            # Ensure it's unique if collisions happen
            while FileRequest.objects.filter(passkey=f"PASS-{year}-{str(count).zfill(3)}").exists():
                count += 1
            self.passkey = f"PASS-{year}-{str(count).zfill(3)}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AuditLog(models.Model):
    user = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: {self.action} by {self.user}"


class PickupSlot(models.Model):
    date = models.DateField(unique=True)
    morning_slots = models.IntegerField(default=5)
    afternoon_slots = models.IntegerField(default=5)
    is_blocked = models.BooleanField(default=False) # For holidays
    reason = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.date} ({'Blocked' if self.is_blocked else f'M:{self.morning_slots} A:{self.afternoon_slots}'})"
class DocumentType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class StudentDocument(models.Model):
    request = models.ForeignKey(FileRequest, related_name='documents', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='student_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} for {self.request.first_name}"


class ProcessedDocument(models.Model):
    """Stores the ready/processed document uploaded by staff for a specific requested file."""
    request = models.ForeignKey(FileRequest, related_name='processed_documents', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)  # matches the requested_files entry
    file = models.FileField(upload_to='processed_docs/')
    uploaded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Processed {self.document_type} for {self.request.first_name} {self.request.last_name}"

class StudentMasterDocument(models.Model):
    student = models.ForeignKey(Student, related_name='documents', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='student_master_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} for {self.student.first_name}"
