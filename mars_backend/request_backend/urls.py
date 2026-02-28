from django.urls import path
from .views import (
    RegisterView, CustomTokenObtainPairView, FileRequestCreateView,
    AdminDashboardStatsView, AdminRequestListView, AdminRequestDetailView,
    AdminRequestBulkUpdateView,
    AdminStaffListView, AdminStaffDetailView, AdminAuditLogListView,
    AdminPickupSlotListView, AdminPickupSlotDetailView, PublicPickupSlotListView,
    AdminDocumentTypeListView, AdminDocumentTypeDetailView, PublicDocumentTypeListView,
    AdminStudentDocumentCreateView, AdminStudentDocumentDeleteView,
    AdminStrandListView, AdminStrandDetailView, PublicStrandListView,
    StaffProcessedDocumentCreateView, StaffProcessedDocumentDeleteView,
    PublicRequestStatusView, PublicRecordCheckView,
    AdminStudentListView, AdminStudentDetailView,
    AdminStudentMasterDocumentCreateView, AdminStudentMasterDocumentDeleteView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('requests/', FileRequestCreateView.as_view(), name='file_request_create'),
    
    # Admin endpoints
    path('admin/stats/', AdminDashboardStatsView.as_view(), name='admin_stats'),
    path('admin/requests/', AdminRequestListView.as_view(), name='admin_requests'),
    path('admin/requests/bulk/', AdminRequestBulkUpdateView.as_view(), name='admin_requests_bulk'),
    path('admin/requests/<int:pk>/', AdminRequestDetailView.as_view(), name='admin_request_detail'),
    
    # Document Type endpoints
    path('admin/document-types/', AdminDocumentTypeListView.as_view(), name='admin_doc_types'),
    path('admin/document-types/<int:pk>/', AdminDocumentTypeDetailView.as_view(), name='admin_doc_type_detail'),
    path('public/document-types/', PublicDocumentTypeListView.as_view(), name='public_doc_types'),
    
    # Strand endpoints
    path('admin/strands/', AdminStrandListView.as_view(), name='admin_strands'),
    path('admin/strands/<int:pk>/', AdminStrandDetailView.as_view(), name='admin_strand_detail'),
    path('public/strands/', PublicStrandListView.as_view(), name='public_strands'),

    # Superadmin User/Audit endpoints
    path('admin/staff/', AdminStaffListView.as_view(), name='admin_staff_list'),
    path('admin/staff/<int:pk>/', AdminStaffDetailView.as_view(), name='admin_staff_detail'),
    path('admin/audit-logs/', AdminAuditLogListView.as_view(), name='admin_audit_logs'),
    
    # Pickup Slot endpoints
    path('admin/slots/', AdminPickupSlotListView.as_view(), name='admin_slots'),
    path('admin/slots/<int:pk>/', AdminPickupSlotDetailView.as_view(), name='admin_slot_detail'),
    path('public/slots/', PublicPickupSlotListView.as_view(), name='public_slots'),

    # Student Document Management (student-uploaded scanned docs)
    path('admin/requests/<int:request_id>/documents/', AdminStudentDocumentCreateView.as_view(), name='admin_student_doc_create'),
    path('admin/documents/<int:pk>/', AdminStudentDocumentDeleteView.as_view(), name='admin_student_doc_delete'),

    # Processed Document Management (staff-uploaded ready docs)
    path('admin/requests/<int:request_id>/processed/', StaffProcessedDocumentCreateView.as_view(), name='staff_processed_doc_create'),
    path('admin/processed/<int:pk>/', StaffProcessedDocumentDeleteView.as_view(), name='staff_processed_doc_delete'),

    # Public: student checks their own request status
    path('public/my-request/', PublicRequestStatusView.as_view(), name='public_request_status'),
    path('public/check-record/', PublicRecordCheckView.as_view(), name='public_record_check'),

    # Student Management
    path('admin/students/', AdminStudentListView.as_view(), name='admin_students'),
    path('admin/students/<int:pk>/', AdminStudentDetailView.as_view(), name='admin_student_detail'),
    path('admin/students/<int:student_id>/documents/', AdminStudentMasterDocumentCreateView.as_view(), name='admin_student_master_doc_create'),
    path('admin/student-documents/<int:pk>/', AdminStudentMasterDocumentDeleteView.as_view(), name='admin_student_master_doc_delete'),
]
