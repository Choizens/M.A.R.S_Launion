import axios from 'axios';

const API_BASE_URL =
    import.meta.env.VITE_API_URL ||
    (import.meta.env.DEV
        ? 'http://127.0.0.1:8000/api/'
        : 'https://marslaunion-production.up.railway.app/api/');

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to include the JWT token in headers
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle 401 errors (Unauthorized/Expired Token)
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            const isAdmin = localStorage.getItem('is_admin') === 'true';
            authService.logout();
            // Redirect to the appropriate login page
            window.location.href = isAdmin ? '/admin/login' : '/Staff/login';
        }
        return Promise.reject(error);
    }
);

export const authService = {
    login(username, password) {
        return apiClient.post('login/', { username, password });
    },
    register(userData) {
        return apiClient.post('register/', userData);
    },
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        localStorage.removeItem('is_admin');
    },
};

export const requestService = {
    submitRequest(data) {
        return apiClient.post('requests/', data);
    },
    lookupRequest(code) {
        return apiClient.get(`requests/lookup/${code}/`);
    },
    getPublicDocTypes() {
        return apiClient.get('public/document-types/');
    },
    getPublicSlots() {
        return apiClient.get('public/slots/');
    },
    getPublicStrands() {
        return apiClient.get('public/strands/');
    }
};

export const adminService = {
    getStats() {
        return apiClient.get('admin/stats/');
    },
    getRequests(params = {}) {
        return apiClient.get('admin/requests/', { params });
    },
    bulkUpdateRequests(data) {
        return apiClient.post('admin/requests/bulk/', data);
    },
    // ...
    getStrands() {
        return apiClient.get('admin/strands/');
    },
    createStrand(data) {
        return apiClient.post('admin/strands/', data);
    },
    updateStrand(id, data) {
        return apiClient.patch(`admin/strands/${id}/`, data);
    },
    deleteStrand(id) {
        return apiClient.delete(`admin/strands/${id}/`);
    },
    getRequest(id) {
        return apiClient.get(`admin/requests/${id}/`);
    },
    updateRequest(id, data) {
        return apiClient.patch(`admin/requests/${id}/`, data);
    },
    createRequest(data) {
        return apiClient.post('admin/requests/', data);
    },
    uploadStudentDocument(requestId, formData) {
        return apiClient.post(`admin/requests/${requestId}/documents/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },
    deleteStudentDocument(docId) {
        return apiClient.delete(`admin/documents/${docId}/`);
    },
    // Superadmin: Staff Management
    getStaffList() {
        return apiClient.get('admin/staff/');
    },
    createStaff(data) {
        return apiClient.post('admin/staff/', data);
    },
    updateStaff(id, data) {
        return apiClient.patch(`admin/staff/${id}/`, data);
    },
    deleteStaff(id) {
        return apiClient.delete(`admin/staff/${id}/`);
    },
    // Superadmin: Audit Logs
    getAuditLogs() {
        return apiClient.get('admin/audit-logs/');
    },
    // Superadmin: Slot Management
    getSlots() {
        return apiClient.get('admin/slots/');
    },
    createSlot(data) {
        return apiClient.post('admin/slots/', data);
    },
    updateSlot(id, data) {
        return apiClient.patch(`admin/slots/${id}/`, data);
    },
    deleteSlot(id) {
        return apiClient.delete(`admin/slots/${id}/`);
    },
    // Superadmin: Document Management
    getDocTypes() {
        return apiClient.get('admin/document-types/');
    },
    createDocType(data) {
        return apiClient.post('admin/document-types/', data);
    },
    updateDocType(id, data) {
        return apiClient.patch(`admin/document-types/${id}/`, data);
    },
    deleteDocType(id) {
        return apiClient.delete(`admin/document-types/${id}/`);
    },
    // Staff: Processed Document Upload (ready doc for student)
    uploadProcessedDocument(requestId, formData) {
        return apiClient.post(`admin/requests/${requestId}/processed/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },
    deleteProcessedDocument(docId) {
        return apiClient.delete(`admin/processed/${docId}/`);
    },
    // Student Management
    getStudents(params = {}) {
        return apiClient.get('admin/students/', { params });
    },
    createStudent(data) {
        return apiClient.post('admin/students/', data);
    },
    updateStudent(id, data) {
        return apiClient.patch(`admin/students/${id}/`, data);
    },
    deleteStudent(id) {
        return apiClient.delete(`admin/students/${id}/`);
    },
    uploadStudentMasterDoc(studentId, formData) {
        return apiClient.post(`admin/students/${studentId}/documents/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },
    deleteStudentMasterDoc(docId) {
        return apiClient.delete(`admin/student-documents/${docId}/`);
    },
};

export const publicService = {
    // Student checks their own request status + downloads ready docs
    getMyRequest(passkey) {
        return apiClient.get('public/my-request/', { params: { passkey } });
    },
    checkRecord(params) {
        return apiClient.get('public/check-record/', { params });
    }
};

export default apiClient;
