from rest_framework import serializers
from .models import Staff, FileRequest, AuditLog, PickupSlot, DocumentType, StudentDocument, Strand, ProcessedDocument, Student, StudentMasterDocument

class StudentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDocument
        fields = ['id', 'document_type', 'file', 'uploaded_at']


class ProcessedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedDocument
        fields = ['id', 'document_type', 'file', 'uploaded_at', 'notes']

class StudentMasterDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMasterDocument
        fields = ['id', 'document_type', 'file', 'uploaded_at']

class StudentSerializer(serializers.ModelSerializer):
    strand_display = serializers.SerializerMethodField()
    documents = StudentMasterDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'lrn_number', 'first_name', 'middle_name', 'last_name', 'suffix',
            'sex', 'year_graduated', 'strand_type', 'strand_display',
            'email', 'phone_number', 'permanent_address', 'created_at', 'documents'
        ]

    def get_strand_display(self, obj):
        try:
            return obj.strand_type.name if obj.strand_type else "N/A"
        except:
            return "N/A"

class StaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Staff
        fields = ['id', 'username', 'password', 'email', 'staff_id', 'department', 'full_name', 'is_staff', 'is_superuser', 'is_active', 'last_login']
        extra_kwargs = {
            'password': {'required': False, 'allow_blank': True}
        }

    def create(self, validated_data):
        email = validated_data.pop('email', '')
        password = validated_data.pop('password', None)
        user = Staff.objects.create_user(
            email=email,
            password=password,
            **validated_data
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class StrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strand
        fields = ['id', 'name', 'description']

class FileRequestSerializer(serializers.ModelSerializer):
    documents = StudentDocumentSerializer(many=True, read_only=True)
    processed_documents = ProcessedDocumentSerializer(many=True, read_only=True)
    strand_display = serializers.CharField(source='strand_type.name', read_only=True)
    student_record = serializers.SerializerMethodField()

    class Meta:
        model = FileRequest
        fields = [
            'id', 'passkey', 'student', 'student_record', 'request_code',
            'first_name', 'middle_name', 'last_name', 'suffix',
            'sex', 'year_graduated', 'strand', 'strand_type', 'strand_display',
            'lrn_number', 'email', 'phone_number', 'permanent_address',
            'requested_files', 'submitted_at', 'status',
            'pickup_date', 'pickup_time', 'no_accountabilities',
            'documents', 'processed_documents'
        ]
        read_only_fields = ['id', 'passkey', 'submitted_at', 'request_code', 'documents', 'processed_documents', 'strand_display', 'student_record']

    def get_student_record(self, obj):
        # 1. If explicitly linked via ForeignKey
        child_student = obj.student
        
        # 2. Fallback 1: Search by LRN if not linked
        if not child_student and obj.lrn_number:
            child_student = Student.objects.filter(lrn_number=obj.lrn_number).first()
            
        # 3. Fallback 2: Search by Name (First & Last) if still not found
        if not child_student:
            child_student = Student.objects.filter(
                first_name__iexact=obj.first_name,
                last_name__iexact=obj.last_name
            ).first()

        if child_student:
            return StudentSerializer(child_student).data
        return None

    def validate_email(self, value):
        if not value.endswith(('.com', '.edu.ph', '.org', '.net')):
            raise serializers.ValidationError("Please provide a valid email address.")
        return value

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Please provide a valid phone number (at least 10 digits).")
        return value

    def validate(self, data):
        pickup_date = data.get('pickup_date')
        pickup_time = data.get('pickup_time')

        if pickup_date and pickup_time:
            # 1. Check if it's a weekend
            if pickup_date.weekday() >= 5:
                raise serializers.ValidationError({"pickup_date": "Pickups are only available from Monday to Friday."})

            # 2. Check if the date is blocked in PickupSlot
            slot = PickupSlot.objects.filter(date=pickup_date).first()
            if slot and slot.is_blocked:
                raise serializers.ValidationError({"pickup_date": f"This date is not available for pickup: {slot.reason or 'Blocked'}"})

            # 3. Check capacity
            max_slots = 5
            if slot:
                max_slots = slot.morning_slots if pickup_time == 'Morning' else slot.afternoon_slots

            current_bookings = FileRequest.objects.filter(
                pickup_date=pickup_date, 
                pickup_time=pickup_time
            ).count()

            if current_bookings >= max_slots:
                raise serializers.ValidationError({"pickup_time": f"The {pickup_time} slot for this date is already full."})

        return data


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_name', 'action', 'details', 'timestamp']


class PickupSlotSerializer(serializers.ModelSerializer):
    booked_morning = serializers.SerializerMethodField()
    booked_afternoon = serializers.SerializerMethodField()

    class Meta:
        model = PickupSlot
        fields = ['id', 'date', 'morning_slots', 'afternoon_slots', 'is_blocked', 'reason', 'booked_morning', 'booked_afternoon']

    def get_booked_morning(self, obj):
        return FileRequest.objects.filter(pickup_date=obj.date, pickup_time='Morning').count()

    def get_booked_afternoon(self, obj):
        return FileRequest.objects.filter(pickup_date=obj.date, pickup_time='Afternoon').count()


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'description', 'price', 'is_active']
