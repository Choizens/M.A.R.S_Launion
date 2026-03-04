from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Count, Q, F
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (
    StaffSerializer, FileRequestSerializer, AuditLogSerializer,
    PickupSlotSerializer, DocumentTypeSerializer, StudentDocumentSerializer,
    StrandSerializer, ProcessedDocumentSerializer, StudentSerializer,
    StudentMasterDocumentSerializer
)
from .models import Staff, FileRequest, AuditLog, PickupSlot, DocumentType, StudentDocument, Strand, ProcessedDocument, Student, StudentMasterDocument


from .utils import send_request_notification, send_submission_confirmation

# ── Logging Helper ─────────────────────────────────────────────────────────────

def record_log(user, action, details=""):
    AuditLog.objects.create(user=user, action=action, details=details)


class RegisterView(generics.CreateAPIView):
    queryset = Staff.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StaffSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = Staff.objects.get(username=request.data['username'])
            response.data['user'] = {
                'username': user.username,
                'full_name': user.full_name,
                'staff_id': user.staff_id,
                'department': user.department,
                'is_admin': user.is_superuser or user.is_staff,
            }
            record_log(user, "User Login", f"User {user.username} logged in successfully.")
        return response


import random
import string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class FileRequestCreateView(generics.CreateAPIView):
    queryset = FileRequest.objects.all()
    serializer_class = FileRequestSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def generate_unique_code(self):
        while True:
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            code = f"SHS-2026-{random_str}"
            if not FileRequest.objects.filter(request_code=code).exists():
                return code

    def perform_create(self, serializer):
        request_code = self.generate_unique_code()
        instance = serializer.save(request_code=request_code)
        
        # Send Email Notification
        subject = 'Your File Request has been Sent'
        html_content = render_to_string('emails/request_notification.html', {
            'instance': instance,
        })
        text_content = strip_tags(html_content)
        
        from django.conf import settings
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [instance.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        # Send confirmation email immediately after the request is created
        send_submission_confirmation(instance)


class FileRequestLookupView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []


    def get(self, request, code, *args, **kwargs):
        try:
            file_request = FileRequest.objects.get(request_code=code.upper())
            serializer = FileRequestSerializer(file_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FileRequest.DoesNotExist:
            return Response({'error': 'Invalid request code. No request found.'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        instance = serializer.save()
        # Send confirmation email immediately after the request is created
        send_submission_confirmation(instance)


# ── Admin Views ────────────────────────────────────────────────────────────────

class AdminDashboardStatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        total       = FileRequest.objects.count()
        pending     = FileRequest.objects.filter(status='Pending').count()
        approved    = FileRequest.objects.filter(status='Approved').count()
        processing  = FileRequest.objects.filter(status='Processing').count()
        completed   = FileRequest.objects.filter(status='Completed').count()
        rejected    = FileRequest.objects.filter(status='Rejected').count()

        # Strand breakdown
        strand_data = (
            FileRequest.objects
            .filter(strand_type__isnull=False)
            .values(strand_name=F('strand_type__name'))
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # Document breakdown (Requested Files)
        all_requests = FileRequest.objects.all()
        doc_counts = {}
        for req in all_requests:
            for doc in req.requested_files:
                doc_counts[doc] = doc_counts.get(doc, 0) + 1
        
        # Get all defined doc types to include 0 counts
        all_doc_types = DocumentType.objects.filter(is_active=True)
        doc_breakdown = []
        for dt in all_doc_types:
            doc_breakdown.append({
                'document': dt.name,
                'count': doc_counts.get(dt.name, 0),
                'price': dt.price
            })
        
        # Also include docs that might not be in DocumentType but were requested (legacy)
        for doc, count in doc_counts.items():
            if not any(d['document'] == doc for d in doc_breakdown):
                doc_breakdown.append({'document': doc, 'count': count, 'price': 0})

        doc_breakdown = sorted(doc_breakdown, key=lambda x: x['count'], reverse=True)

        # Monthly breakdown (last 6 months)
        from django.db.models.functions import TruncMonth
        monthly_data = (
            FileRequest.objects
            .annotate(month=TruncMonth('submitted_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('-month')[:6]
        )

        # Upcoming Slots
        from django.utils import timezone
        today = timezone.now().date()
        upcoming_slots = PickupSlotSerializer(
            PickupSlot.objects.filter(date__gte=today, is_blocked=False).order_by('date')[:5],
            many=True
        ).data

        recent = FileRequestSerializer(
            FileRequest.objects.prefetch_related('documents').order_by('-submitted_at')[:5],
            many=True
        ).data

        return Response({
            'total': total,
            'pending': pending,
            'approved': approved,
            'processing': processing,
            'completed': completed,
            'rejected': rejected,
            'strand_breakdown': list(strand_data),
            'doc_breakdown': doc_breakdown,
            'monthly_trend': list(monthly_data),
            'upcoming_slots': upcoming_slots,
            'recent_requests': recent,
        })


class AdminRequestListView(generics.ListCreateAPIView):
    serializer_class = FileRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = FileRequest.objects.prefetch_related('documents').all().order_by('-submitted_at')
        status_filter = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        strand_filter = self.request.query_params.get('strand')
        year_filter = self.request.query_params.get('year')

        if status_filter:
            qs = qs.filter(status=status_filter)
        if strand_filter:
            qs = qs.filter(strand_type_id=strand_filter)
        if year_filter:
            qs = qs.filter(year_graduated=year_filter)
        if search:
            query = Q(first_name__icontains=search) | \
                    Q(last_name__icontains=search) | \
                    Q(email__icontains=search) | \
                    Q(lrn_number__icontains=search) | \
                    Q(strand__icontains=search) | \
                    Q(passkey__icontains=search)
            
            # If search is a number, also check against ID
            if search.isdigit():
                query |= Q(id=search)
                
            qs = qs.filter(query)
        return qs


class AdminRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = FileRequest.objects.all()
    serializer_class = FileRequestSerializer
    permission_classes = (IsAuthenticated,)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_status = instance.status
        if 'status' in request.data and new_status != old_status:
            record_log(
                request.user,
                "Updated Request Status",
                f"Changed Request #{instance.id} ({instance.passkey}) from '{old_status}' to '{new_status}'"
            )
            send_request_notification(instance)

        return Response(serializer.data)

        return Response(serializer.data)

class AdminRequestBulkUpdateView(APIView):
    """Admin bulk updates multiple request statuses at once."""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        action = request.data.get('action') # 'Approved', 'Rejected', etc.
        request_ids = request.data.get('ids', [])

        if not action or not request_ids:
            return Response({'error': 'Missing action or ids'}, status=status.HTTP_400_BAD_REQUEST)

        updated_count = FileRequest.objects.filter(id__in=request_ids).update(status=action)

        record_log(
            request.user, 
            "Bulk Updated Requests", 
            f"Set status to {action} for {updated_count} requests."
        )

        # Trigger email notifications for the updated requests
        if action in ['Approved', 'Completed', 'Needs Verification', 'Rejected']:
            updated_requests = FileRequest.objects.filter(id__in=request_ids)
            for file_request in updated_requests:
                send_request_notification(file_request)

        return Response({'message': f'Successfully updated {updated_count} requests to {action}'})


# ── Student Management Views (Admin only) ──────────────────────────────────────

class AdminStudentListView(generics.ListCreateAPIView):
    """Admin views all students and creates new students."""
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)  # Assuming both admin and staff might need to see student list

    def get_queryset(self):
        qs = Student.objects.all().order_by('-created_at')
        search = self.request.query_params.get('search')
        strand = self.request.query_params.get('strand')
        year = self.request.query_params.get('year')

        if strand:
            qs = qs.filter(strand_type_id=strand)
        if year:
            qs = qs.filter(year_graduated=year)
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(lrn_number__icontains=search) |
                Q(email__icontains=search)
            )
        return qs

    def perform_create(self, serializer):
        student = serializer.save()
        record_log(
            self.request.user,
            "Created Student Record",
            f"Admin/Staff created master record for student {student.first_name} {student.last_name} (LRN: {student.lrn_number})"
        )

class AdminStudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin manages a specific student record."""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        student = serializer.save()
        record_log(
            self.request.user,
            "Updated Student Record",
            f"Admin/Staff updated details for student {student.first_name} {student.last_name}"
        )

    def perform_destroy(self, instance):
        record_log(
            self.request.user,
            "Deleted Student Record",
            f"Admin/Staff removed master record for {instance.first_name} {instance.last_name} (LRN: {instance.lrn_number})"
        )
        instance.delete()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status
        old_acc = instance.no_accountabilities
        
        allowed = {'status', 'no_accountabilities'}
        data = {k: v for k, v in request.data.items() if k in allowed}
        
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        if 'status' in data and data['status'] != old_status:
            record_log(
                request.user, 
                "Update Request Status", 
                f"Changed ID #{instance.id} status from {old_status} to {data['status']}"
            )
            send_request_notification(instance)
            
        if 'no_accountabilities' in data and data['no_accountabilities'] != old_acc:
            action = "Verified No Accountabilities" if data['no_accountabilities'] else "Unverified Accountabilities"
            record_log(
                request.user,
                action,
                f"Accountability status updated for ID #{instance.id}"
            )
            
        return Response(serializer.data)


# ── Document Type Management ──────────────────────────────────────────────────

class AdminDocumentTypeListView(generics.ListCreateAPIView):
    queryset = DocumentType.objects.all().order_by('name')
    serializer_class = DocumentTypeSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        doc = serializer.save()
        record_log(self.request.user, "Created Document Type", f"Added document: {doc.name}")


class AdminDocumentTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_update(self, serializer):
        doc = serializer.save()
        record_log(self.request.user, "Updated Document Type", f"Modified document: {doc.name}")

    def perform_destroy(self, instance):
        record_log(self.request.user, "Deleted Document Type", f"Removed document: {instance.name}")
        instance.delete()


class PublicDocumentTypeListView(generics.ListAPIView):
    queryset = DocumentType.objects.filter(is_active=True).order_by('name')
    serializer_class = DocumentTypeSerializer
    permission_classes = (AllowAny,)


class AdminStrandListView(generics.ListCreateAPIView):
    queryset = Strand.objects.all().order_by('name')
    serializer_class = StrandSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        strand = serializer.save()
        record_log(self.request.user, "Created Strand", f"Added strand: {strand.name}")


class AdminStrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Strand.objects.all()
    serializer_class = StrandSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_update(self, serializer):
        strand = serializer.save()
        record_log(self.request.user, "Updated Strand", f"Modified strand: {strand.name}")

    def perform_destroy(self, instance):
        record_log(self.request.user, "Deleted Strand", f"Removed strand: {instance.name}")
        instance.delete()


class PublicStrandListView(generics.ListAPIView):
    queryset = Strand.objects.all().order_by('name')
    serializer_class = StrandSerializer
    permission_classes = (AllowAny,)


# ── Superadmin (User & Audit) Views ─────────────────────────────────────────────

class AdminStaffListView(generics.ListCreateAPIView):
    queryset = Staff.objects.all().order_by('-id')
    serializer_class = StaffSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        user = serializer.save()
        record_log(self.request.user, "Created Staff Account", f"Created account for {user.username}")


class AdminStaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_update(self, serializer):
        user = serializer.save()
        record_log(self.request.user, "Updated Staff Account", f"Modified account {user.username}")

    def perform_destroy(self, instance):
        record_log(self.request.user, "Deleted Staff Account", f"Removed account {instance.username}")
        instance.delete()


class AdminAuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


# ── Schedule / Slot Views ──────────────────────────────────────────────────────

class AdminPickupSlotListView(generics.ListCreateAPIView):
    queryset = PickupSlot.objects.all().order_by('date')
    serializer_class = PickupSlotSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_create(self, serializer):
        slot = serializer.save()
        record_log(self.request.user, "Created Pickup Slot", f"Set slot for {slot.date}")


class AdminPickupSlotDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PickupSlot.objects.all()
    serializer_class = PickupSlotSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_update(self, serializer):
        slot = serializer.save()
        record_log(self.request.user, "Updated Pickup Slot", f"Modified slot for {slot.date}")

    def perform_destroy(self, instance):
        record_log(self.request.user, "Deleted Pickup Slot", f"Removed slot for {instance.date}")
        instance.delete()


class PublicPickupSlotListView(generics.ListAPIView):
    """View for students to see available slots on the calendar."""
    queryset = PickupSlot.objects.filter(is_blocked=False).order_by('date')
    serializer_class = PickupSlotSerializer
    permission_classes = (AllowAny,)


# ── Student Document Management ────────────────────────────────────────────────

class AdminStudentDocumentCreateView(generics.CreateAPIView):
    queryset = StudentDocument.objects.all()
    serializer_class = StudentDocumentSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        request_id = self.kwargs.get('request_id')
        file_request = FileRequest.objects.get(id=request_id)
        doc = serializer.save(request=file_request)
        record_log(self.request.user, "Uploaded Student File", f"Added {doc.document_type} for ID #{request_id}")


class AdminStudentDocumentDeleteView(generics.DestroyAPIView):
    queryset = StudentDocument.objects.all()
    serializer_class = StudentDocumentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def perform_destroy(self, instance):
        record_log(self.request.user, "Deleted Student File", f"Removed {instance.document_type} from Request ID #{instance.request.id}")
        instance.delete()


# ── Processed Document Management (Staff uploads ready document) ───────────────

class StaffProcessedDocumentCreateView(generics.CreateAPIView):
    """Staff uploads the ready/processed document for a specific requested file."""
    queryset = ProcessedDocument.objects.all()
    serializer_class = ProcessedDocumentSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        request_id = self.kwargs.get('request_id')
        file_request = FileRequest.objects.get(id=request_id)
        doc = serializer.save(request=file_request, uploaded_by=self.request.user)
        record_log(
            self.request.user,
            "Uploaded Processed Document",
            f"Staff uploaded processed '{doc.document_type}' for Request ID #{request_id}"
        )


class StaffProcessedDocumentDeleteView(generics.DestroyAPIView):
    queryset = ProcessedDocument.objects.all()
    serializer_class = ProcessedDocumentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        record_log(
            self.request.user,
            "Deleted Processed Document",
            f"Removed processed '{instance.document_type}' from Request ID #{instance.request.id}"
        )
        instance.delete()

class AdminStudentMasterDocumentCreateView(generics.CreateAPIView):
    queryset = StudentMasterDocument.objects.all()
    serializer_class = StudentMasterDocumentSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        student_id = self.kwargs.get('student_id')
        student = Student.objects.get(id=student_id)
        doc = serializer.save(student=student)
        record_log(self.request.user, "Uploaded Student Master File", f"Added {doc.document_type} for Student {student.first_name} {student.last_name}")

class AdminStudentMasterDocumentDeleteView(generics.DestroyAPIView):
    queryset = StudentMasterDocument.objects.all()
    serializer_class = StudentMasterDocumentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        record_log(self.request.user, "Deleted Student Master File", f"Removed {instance.document_type} from Student {instance.student.first_name}")
        instance.delete()

class PublicRequestStatusView(APIView):
    """Public endpoint: student checks request status + downloads ready docs by email + ID."""
    permission_classes = (AllowAny,)

    def get(self, request):
        email = request.query_params.get('email', '').strip()
        passkey = request.query_params.get('passkey', '').strip()
        if not email or not passkey:
            return Response({'error': 'Provide both email and Passkey.'}, status=400)
        try:
            fr = FileRequest.objects.prefetch_related('processed_documents').get(passkey__iexact=passkey, email__iexact=email)
            serializer = FileRequestSerializer(fr)
            return Response(serializer.data)
        except FileRequest.DoesNotExist:
            return Response({'error': 'No matching request found. Please check your Passkey and Email.'}, status=404)

class PublicRecordCheckView(APIView):
    """Check if a student's record exists and what documents are digitized."""
    permission_classes = (AllowAny,)

    def get(self, request):
        lrn = request.query_params.get('lrn', '').strip()
        first_name = request.query_params.get('first_name', '').strip()
        last_name = request.query_params.get('last_name', '').strip()

        student = None
        if lrn:
            student = Student.objects.filter(lrn_number=lrn).first()
        
        if not student and first_name and last_name:
            student = Student.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name
            ).first()

        if not student:
            return Response({
                'exists': False,
                'message': 'No digital record found. Please visit the school office for manual processing.',
                'documents': []
            })

        # Check for existing requests (Pending, Approved, Needs Verification, Completed)
        # Only 'Rejected' requests allow a new submission. 
        # 'Completed' is blocked because the school has already given the physical file.
        active_request = FileRequest.objects.filter(
            email__iexact=student.email,
            status__in=['Pending', 'Approved', 'Needs Verification', 'Completed']
        ).first()

        if active_request:
            status_msg = "is being processed" if active_request.status != 'Completed' else "has already been completed and the file was issued"
            return Response({
                'exists': True,
                'has_active_request': True,
                'active_request_id': active_request.passkey,
                'message': f'You already have a request that {status_msg} (Passkey: {active_request.passkey}). Duplicate requests are not allowed.',
                'documents': []
            })

        # Get names of digitized documents
        digitized_docs = student.documents.values_list('document_type', flat=True)
        
        return Response({
            'exists': True,
            'has_active_request': False,
            'student_id': student.id,
            'full_name': f"{student.first_name} {student.last_name}",
            'documents': list(digitized_docs)
        })
