<template>
  <div class="flex h-screen bg-[#f5f7fa] font-sans overflow-hidden">

    <!-- Mobile Overlay Backdrop -->
    <Transition name="fade">
      <div 
        v-if="sidebarOpen && isMobile"
        class="fixed inset-0 bg-black/50 z-30"
        @click="sidebarOpen = false"
      />
    </Transition>

    <!-- Sidebar -->
    <aside 
      :class="[
        'bg-[#103059] text-white flex flex-col transition-all duration-300 ease-in-out z-40 shadow-xl shrink-0',
        // Mobile: fixed drawer that slides in/out
        isMobile ? (
          sidebarOpen ? 'fixed inset-y-0 left-0 w-72 translate-x-0' : 'fixed inset-y-0 left-0 w-72 -translate-x-full'
        ) : (
        // Desktop: static, collapses to icon rail
          sidebarOpen ? 'w-64' : 'w-16'
        )
      ]"
    >
      <!-- Sidebar Top Brand + Close btn on mobile -->
      <div class="flex items-center justify-between px-4 py-5 border-b border-white/10 shrink-0">
        <Transition name="fade">
          <div v-if="sidebarOpen" class="flex items-center gap-3 overflow-hidden">
            <img :src="logoImg" alt="Logo" class="w-8 h-8 object-contain brightness-0 invert shrink-0" />
            <div class="flex flex-col leading-tight">
              <span class="text-xs font-black uppercase tracking-wider whitespace-nowrap">La Union SHS</span>
              <span class="text-[0.55rem] opacity-60 uppercase tracking-widest">Admin Panel</span>
            </div>
          </div>
        </Transition>
        <!-- Desktop collapse / Mobile close button -->
        <button
          @click="sidebarOpen = false"
          class="p-2 rounded hover:bg-white/10 transition-colors shrink-0"
          :class="!sidebarOpen && !isMobile ? 'mx-auto' : ''"
          title="Close sidebar"
        >
          <XIcon class="w-5 h-5" />
        </button>
      </div>

      <!-- Sidebar Nav -->
      <nav class="flex-grow pt-4 overflow-y-auto overflow-x-hidden">
        <ul class="flex flex-col">
          <li 
            v-for="item in navItems" 
            :key="item.id"
            @click="navigateTo(item.id)"
            :class="[
              'group flex items-center px-4 py-3.5 cursor-pointer transition-colors border-b border-white/5 relative',
              currentView === item.id ? 'bg-[#ffca28] text-[#103059]' : 'hover:bg-white/10'
            ]"
            :title="!sidebarOpen ? item.label : ''"
          >
            <div class="flex items-center min-w-[24px] justify-center shrink-0" :class="!sidebarOpen && !isMobile ? 'mx-auto' : ''">
              <component :is="item.icon" class="w-5 h-5 shrink-0" />
            </div>
            <span 
              :class="[
                'ml-4 font-semibold text-sm whitespace-nowrap transition-all duration-200 overflow-hidden',
                sidebarOpen ? 'opacity-100 max-w-xs' : 'opacity-0 max-w-0 ml-0'
              ]"
            >
              {{ item.label }}
            </span>
            <!-- Pending Badge -->
            <span 
              v-if="sidebarOpen && item.id === 'record_requests' && stats.pending > 0" 
              class="ml-auto bg-red-500 text-white text-[0.6rem] font-bold px-1.5 py-0.5 rounded-full shrink-0"
            >
              {{ stats.pending }}
            </span>
            <!-- Active Bar for collapsed desktop -->
            <div v-if="!sidebarOpen && !isMobile && currentView === item.id" class="absolute left-0 top-0 w-1 h-full bg-[#ffca28] rounded-r"></div>
          </li>
        </ul>
      </nav>

      <!-- Sidebar Footer / Logout -->
      <div class="p-4 border-t border-white/10 shrink-0">
        <button 
          @click="handleLogout" 
          :class="[
            'w-full flex items-center p-2.5 rounded border border-white/30 text-white hover:bg-red-600 hover:border-red-600 transition-all duration-200',
            sidebarOpen ? 'justify-start' : 'justify-center'
          ]"
          :title="!sidebarOpen ? 'Logout' : ''"
        >
          <LogOutIcon class="w-5 h-5 shrink-0" />
          <span 
            :class="[
              'font-semibold text-sm whitespace-nowrap transition-all duration-200 overflow-hidden',
              sidebarOpen ? 'ml-3 opacity-100 max-w-xs' : 'opacity-0 max-w-0'
            ]"
          >
            Logout
          </span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- Top Header -->
      <header class="h-16 bg-[#103059] text-white flex items-center justify-between px-4 md:px-8 shadow-md z-10 shrink-0">
        <div class="flex items-center gap-3">
          <!-- Burger toggle -->
          <button 
            @click="sidebarOpen = !sidebarOpen" 
            class="p-2 hover:bg-white/10 rounded transition-colors focus:outline-none"
            title="Toggle Sidebar"
          >
            <MenuIcon class="w-6 h-6" />
          </button>
          
          <div class="hidden sm:flex flex-col">
            <h2 class="text-xs md:text-sm font-bold leading-tight uppercase tracking-wide">La Union SHS — Admin</h2>
            <p class="text-[0.55rem] opacity-60 tracking-widest uppercase">M.A.R.S Dashboard</p>
          </div>
        </div>

        <div class="flex items-center gap-4 md:gap-8">
          <div class="hidden md:flex flex-col text-right">
            <span class="text-xs font-medium opacity-90 italic">Welcome, {{ user?.full_name || 'Admin' }}</span>
            <span class="text-[0.7rem] font-bold uppercase tracking-wider text-amber-300 mt-0.5">Administrator</span>
          </div>
          
          <div class="relative cursor-pointer hover:opacity-80 transition-opacity">
            <BellIcon class="w-6 h-6" />
            <span v-if="stats.pending > 0" class="absolute -top-1.5 -right-1.5 bg-[#ff4d4d] text-white text-[0.6rem] font-bold px-1.5 py-0.5 rounded-full border-2 border-[#103059]">
              {{ stats.pending }}
            </span>
          </div>
        </div>
      </header>

      <!-- Page Content Area -->
      <main class="flex-1 overflow-y-auto p-8 lg:p-12">
        <div class="max-w-7xl mx-auto">
          
          <DashboardOverview 
            v-if="currentView === 'overview'"
            :stats="stats"
            :statCards="statCards"
            :loadingStats="loadingStats"
            :strandPercent="strandPercent"
            :formatDate="formatDate"
            :formatDateFull="formatDateFull"
            :initials="initials"
            :statusClass="statusClass"
            @change-view="currentView = $event"
            @open-modal="openModal"
          />

          <RequestsList 
            v-if="currentView === 'record_requests'"
            :requests="requests"
            :loadingRequests="loadingRequests"
            v-model:searchQuery="searchQuery"
            v-model:strandFilter="strandFilter"
            v-model:yearFilter="yearFilter"
            v-model:statusFilter="statusFilter"
            :strands="strands"
            :stats="stats"
            :statusFilters="statusFilters"
            :formatDate="formatDate"
            :initials="initials"
            :statusClass="statusClass"
            @refresh="loadRequests"
            @open-modal="openModal"
            @bulk-action="handleBulkAction"
          />

          <StudentDirectory 
            v-if="currentView === 'student_directory'"
            :students="filteredStudents"
            :loadingStudents="loadingStudents"
            v-model:searchQuery="searchQuery"
            v-model:strandFilter="strandFilter"
            v-model:yearFilter="yearFilter"
            v-model:missingDocsFilter="missingDocsFilter"
            :strands="strands"
            :initials="initials"
            @open-student-modal="openStudentModal()"
            @open-profile="openStudentProfileModal"
            @delete-student="deleteStudent"
          />

          <StaffTable 
            v-if="currentView === 'staff_management'"
            :staffList="staffOnlyUsers"
            :formatDateTime="formatDateTime"
            @open-modal="openStaffModal(null, false)"
            @edit="openStaffModal"
            @delete="deleteStaff"
            @toggle-status="toggleStaffStatus"
          />

          <AdminTable 
            v-if="currentView === 'admin_management'"
            :adminList="adminUsers"
            :formatDateTime="formatDateTime"
            @open-modal="openStaffModal(null, true)"
            @edit="openStaffModal"
            @delete="deleteStaff"
            @toggle-status="toggleStaffStatus"
          />



          <AdminSettings 
            v-if="currentView === 'admin_settings'"
            :user="user"
          />

          <SystemAuditLogs 
            v-if="currentView === 'audit_logs'"
            :auditLogs="auditLogs"
            :formatDateTime="formatDateTime"
          />

          <StrandSettings 
            v-if="currentView === 'strand_settings'"
            :strands="strands"
            @open-strand-modal="openStrandModal()"
            @edit-strand="openStrandModal"
            @delete-strand="deleteStrand"
          />

          <DocumentTypes 
            v-if="currentView === 'document_types'"
            :docTypes="docTypes"
            @open-doc-modal="openDocModal()"
            @edit-doc="openDocModal"
            @delete-doc="deleteDoc"
          />
          
          <PickupScheduling 
            v-if="currentView === 'scheduling'"
          />

        </div>
      </main>
    </div>

    <!-- Modals -->
    <RequestDetailModal 
      :show="showModal"
      :request="selectedRequest"
      :formatDate="formatDate"
      :statusClass="statusClass"
      @close="closeModal"
    />

    <StaffModal 
      :show="showStaffModal"
      :editingId="editingStaff"
      :form="staffForm"
      :submitting="submittingStaff"
      @close="showStaffModal = false"
      @submit="handleStaffSubmit"
    />



    <DocumentModal 
      :show="showDocModal"
      :editingId="editingDoc"
      :form="docForm"
      :submitting="submittingDoc"
      @close="showDocModal = false"
      @submit="handleDocSubmit"
    />

    <StrandModal 
      :show="showStrandModal"
      :editingId="editingStrand"
      :form="strandForm"
      :submitting="submittingStrand"
      @close="showStrandModal = false"
      @submit="handleStrandSubmit"
    />

    <StudentModal 
      :show="showStudentModal"
      :editingId="editingStudent?.id"
      :form="studentForm"
      :submitting="submittingStudent"
      :strands="strands"
      @close="showStudentModal = false"
      @submit="handleStudentSubmit"
    />

    <StudentProfileModal 
      :show="showStudentProfileModal"
      :student="liveSelectedStudent"
      :form="masterDocForm"
      :docTypes="docTypes"
      :uploading="uploadingMasterDoc"
      :formatDate="formatDate"
      :initials="initials"
      ref="studentDocsModalRef"
      @close="showStudentProfileModal = false"
      @upload="handleMasterDocUpload"
      @file-change="onMasterDocFileChange"
      @update:document_type="masterDocForm.document_type = $event"
      @delete-doc="handleDeleteMasterDoc"
      @edit-student="openStudentModal"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, markRaw, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { authService, adminService } from '@/services/api';
import logoImg from '@/assets/form_logo.png';

// Tab Components
import DashboardOverview from './tabs/DashboardOverview.vue';
import RequestsList from './tabs/RequestsList.vue';
import StudentDirectory from './tabs/StudentDirectory.vue';
import StaffTable from './tabs/StaffTable.vue';
import AdminTable from './tabs/AdminTable.vue';
import AdminSettings from './tabs/AdminSettings.vue';
import SystemAuditLogs from './tabs/SystemAuditLogs.vue';
import StrandSettings from './tabs/StrandSettings.vue';
import DocumentTypes from './tabs/DocumentTypes.vue';
import PickupScheduling from './tabs/PickupScheduling.vue';

// Modal Components
import RequestDetailModal from './components/RequestDetailModal.vue';
import StaffModal from './components/StaffModal.vue';

import DocumentModal from './components/DocumentModal.vue';
import StrandModal from './components/StrandModal.vue';
import StudentModal from './components/StudentModal.vue';
import StudentProfileModal from './components/StudentProfileModal.vue';

// Lucide Icons
import { 
  Menu as MenuIcon, X as XIcon, LayoutDashboard as DashboardIcon, 
  List as ListIcon, Users as UsersIcon, User as UserIcon, 
  LogOut as LogOutIcon, Bell as BellIcon, Search as SearchIcon,
  FileText as FileIcon, Clock as ClockIcon, CheckCircle as CheckIcon,
  AlertCircle as AlertIcon, Settings as CogIcon, History as HistoryIcon,
  Activity as ActivityIcon, Copy as CopyIcon, ChevronLeft as ChevronLeftIcon, 
  ChevronRight as ChevronRightIcon, FileStack as DocsIcon, DollarSign as MoneyIcon,
  Paperclip as AttachmentIcon, ShieldCheck as AdminIcon, Calendar as CalendarIcon
} from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();
const user = ref(null);
const sidebarOpen = ref(window.innerWidth >= 768);
const isMobile = ref(window.innerWidth < 768);

const handleResize = () => {
  const mobile = window.innerWidth < 768;
  isMobile.value = mobile;
  if (!mobile && !sidebarOpen.value) {
    // keep whatever the user set on desktop
  }
  if (mobile) {
    sidebarOpen.value = false;
  }
};

window.addEventListener('resize', handleResize);

const navigateTo = (id) => {
  currentView.value = id;
  if (isMobile.value) sidebarOpen.value = false;
};

const currentView = computed({
  get: () => route.params.tab || 'overview',
  set: (val) => router.push(`/admin/dashboard/${val}`)
});

const stats = ref({
  total: 0, pending: 0, approved: 0, processing: 0, completed: 0, rejected: 0,
  strand_breakdown: [], recent_requests: []
});
const requests = ref([]);
const staffList = ref([]);
const adminUsers = computed(() => staffList.value.filter(u => u.is_superuser));
const staffOnlyUsers = computed(() => staffList.value.filter(u => !u.is_superuser));
const auditLogs = ref([]);
const updatingStatus = ref(false);
const targetStatus = ref('');
const updateError = ref('');

const docTypes = ref([]);
const students = ref([]);
const loadingStats = ref(false);
const loadingRequests = ref(false);
const loadingStudents = ref(false);
const showModal = ref(false);
const selectedRequest = ref(null);



// Staff Modal State
const showStaffModal = ref(false);
const editingStaff = ref(null);
const submittingStaff = ref(false);
const staffForm = reactive({ username: '', password: '', full_name: '', staff_id: '', department: '', email: '', is_staff: true, is_superuser: false });



// Strand Modal State
const showStrandModal = ref(false);
const editingStrand = ref(null);
const submittingStrand = ref(false);
const strandForm = reactive({ name: '', description: '' });
const strands = ref([]);

// Document Modal State
const showDocModal = ref(false);
const editingDoc = ref(null);
const submittingDoc = ref(false);
const docForm = reactive({ name: '', description: '', price: 0, is_active: true });

// Student Modal State
const showStudentModal = ref(false);
const editingStudent = ref(null);
const submittingStudent = ref(false);
const studentForm = reactive({
  lrn_number: '',
  first_name: '',
  middle_name: '',
  last_name: '',
  suffix: '',
  sex: 'Male',
  year_graduated: '',
  strand_type: '',
  email: '',
  phone_number: '',
  permanent_address: ''
});


const strandFilter = ref('');
const yearFilter = ref('');

const selectedFiles = reactive({});
const verifyKey = ref('');
const handleVerify = async () => {
  if (!verifyKey.value.trim()) return;
  try {
    const res = await adminService.getRequests({ search: verifyKey.value.trim() });
    const match = res.data.find(r => r.passkey === verifyKey.value.trim().toUpperCase());
    if (match) {
      openModal(match);
      verifyKey.value = '';
    } else {
      alert('Invalid Pass Key. No matching request found.');
    }
  } catch (err) {
    console.error('Verify error:', err);
    alert('Verification failed. Please check your connection.');
  }
};

const searchQuery = ref('');
const statusFilter = ref('');
let searchTimeout = null;

// ── Nav ─────────────────────────────────────────────────────────────────────
const navItems = [
  { id: 'overview', label: 'Dashboard', icon: markRaw(DashboardIcon) },
  { id: 'record_requests', label: 'Request List', icon: markRaw(ListIcon) },
  { id: 'student_directory', label: 'Student List', icon: markRaw(UsersIcon) },
  { id: 'strand_settings', label: 'Strand Settings', icon: markRaw(DocsIcon) },
  { id: 'admin_management', label: 'Administrators', icon: markRaw(AdminIcon) },
  { id: 'staff_management', label: 'Staff Members', icon: markRaw(UserIcon) },
  { id: 'document_types', label: 'Document Types', icon: markRaw(DocsIcon) },
  { id: 'scheduling', label: 'Pickup Scheduling', icon: markRaw(CalendarIcon) },
  { id: 'audit_logs', label: 'Audit Logs', icon: markRaw(HistoryIcon) },
  { id: 'admin_settings', label: 'Settings', icon: markRaw(CogIcon) },
];

const statCards = computed(() => [
  { label: 'Total Requests', value: stats.value.total ?? 0, color: '#103059', icon: markRaw(FileIcon) },
  { label: 'Active Admins', value: stats.value.admin_count ?? 0, color: '#b45309', icon: markRaw(AdminIcon) },
  { label: 'Staff Members', value: stats.value.staff_count ?? 0, color: '#1d4ed8', icon: markRaw(UserIcon) },
  { label: 'Pending', value: stats.value.pending ?? 0, color: '#f59e0b', icon: markRaw(ClockIcon) },
  { label: 'Approved', value: stats.value.approved ?? 0, color: '#10b981', icon: markRaw(CheckIcon) },
  { label: 'Completed', value: stats.value.completed ?? 0, color: '#8b5cf6', icon: markRaw(CheckIcon) },
]);

const statusFilters = [
  { label: 'All Requests', value: '', stat: 'total' },
  { label: 'Pending', value: 'Pending', stat: 'pending' },
  { label: 'Approved', value: 'Approved', stat: 'approved' },
  { label: 'Completed', value: 'Completed', stat: 'completed' },
];

const statusOptions = [
  { value: 'Pending',    label: 'Mark Pending',  btnColor: 'border-amber-400 text-amber-600 hover:bg-amber-400 hover:text-white' },
  { value: 'Processing', label: 'Start Process', btnColor: 'border-cyan-400 text-cyan-600 hover:bg-cyan-400 hover:text-white' },
  { value: 'Needs Verification', label: 'Missing Record', btnColor: 'border-orange-400 text-orange-600 hover:bg-orange-400 hover:text-white' },
  { value: 'Approved',   label: 'Approve',       btnColor: 'border-green-400 text-green-600 hover:bg-green-400 hover:text-white' },
  { value: 'Completed',  label: 'Complete',      btnColor: 'border-purple-400 text-purple-600 hover:bg-purple-400 hover:text-white' },
  { value: 'Rejected',   label: 'Reject',        btnColor: 'border-red-400 text-red-600 hover:bg-red-400 hover:text-white' },
];

// ── Data loading ─────────────────────────────────────────────────────────────
const loadStats = async () => {
  loadingStats.value = true;
  try { const res = await adminService.getStats(); stats.value = res.data; } catch (err) { console.error('Stats error:', err); }
  finally { loadingStats.value = false; }
};

const loadRequests = async () => {
  loadingRequests.value = true;
  try {
    const params = {};
    if (statusFilter.value) params.status = statusFilter.value;
    if (searchQuery.value.trim()) params.search = searchQuery.value.trim();
    if (strandFilter.value) params.strand = strandFilter.value;
    if (yearFilter.value) params.year = yearFilter.value;
    const res = await adminService.getRequests(params);
    requests.value = res.data;
  } catch (err) { console.error('Requests error:', err); }
  finally { loadingRequests.value = false; }
};

const loadStaffList = async () => {
  try { const res = await adminService.getStaffList(); staffList.value = res.data; } catch (err) { console.error('Staff error:', err); }
};

const loadAuditLogs = async () => {
  try { const res = await adminService.getAuditLogs(); auditLogs.value = res.data; } catch (err) { console.error('Logs error:', err); }
};



const loadStrands = async () => {
  try { const res = await adminService.getStrands(); strands.value = res.data; } catch (err) { console.error('Strands error:', err); }
};

const openStrandModal = (s = null) => {
  editingStrand.value = s;
  if (s) {
    strandForm.name = s.name;
    strandForm.description = s.description;
  } else {
    strandForm.name = '';
    strandForm.description = '';
  }
  showStrandModal.value = true;
};

const handleStrandSubmit = async () => {
  submittingStrand.value = true;
  try {
    if (editingStrand.value) {
      await adminService.updateStrand(editingStrand.value.id, strandForm);
    } else {
      await adminService.createStrand(strandForm);
    }
    await loadStrands();
    showStrandModal.value = false;
  } catch (err) {
    console.error('Strand submit error:', err);
    alert('Failed to save strand.');
  } finally {
    submittingStrand.value = false;
  }
};

const deleteStrand = async (id) => {
  if (!confirm('Are you sure you want to delete this strand?')) return;
  try {
    await adminService.deleteStrand(id);
    await loadStrands();
  } catch (err) {
    console.error('Delete strand error:', err);
    alert('Failed to delete strand.');
  }
};

const setFilter = (val) => { statusFilter.value = val; loadRequests(); };
const onSearch = () => { clearTimeout(searchTimeout); searchTimeout = setTimeout(loadRequests, 350); };

// ── Modal Handlers ────────────────────────────────────────────────────────────
const openModal = (req) => { selectedRequest.value = { ...req }; updateError.value = ''; showModal.value = true; };
const closeModal = () => { showModal.value = false; selectedRequest.value = null; };

const updateStatus = async (id, newStatus) => {
  updatingStatus.value = true;
  targetStatus.value = newStatus;
  updateError.value = '';
  try {
    const res = await adminService.updateRequest(id, { status: newStatus });
    selectedRequest.value.status = res.data.status;
    const idx = requests.value.findIndex(r => r.id === id);
    if (idx !== -1) requests.value[idx].status = res.data.status;
    await loadStats();
    loadAuditLogs();
  } catch (err) { updateError.value = 'Status update failed.'; }
  finally { updatingStatus.value = false; targetStatus.value = ''; }
};

const toggleAccountability = async () => {
  if (!selectedRequest.value) return;
  const newValue = !selectedRequest.value.no_accountabilities;
  try {
    const res = await adminService.updateRequest(selectedRequest.value.id, { no_accountabilities: newValue });
    selectedRequest.value.no_accountabilities = res.data.no_accountabilities;
    // update in local list
    const idx = requests.value.findIndex(r => r.id === selectedRequest.value.id);
    if (idx !== -1) requests.value[idx].no_accountabilities = res.data.no_accountabilities;
    loadAuditLogs();
  } catch (err) { console.error('Verification update failed'); }
};

// ── Staff Management ──────────────────────────────────────────────────────────
const toggleStaffStatus = async (staff) => {
  if (!confirm(`Are you sure you want to ${staff.is_active ? 'deactivate' : 'activate'} this account?`)) return;
  try {
    const res = await adminService.updateStaff(staff.id, { is_active: !staff.is_active });
    const idx = staffList.value.findIndex(s => s.id === staff.id);
    if (idx !== -1) staffList.value[idx].is_active = res.data.is_active;
    loadAuditLogs();
  } catch (err) {
    console.error('Toggle status error:', err);
    alert('Failed to update staff status.');
  }
};

const openStaffModal = (stf = null, preferAdmin = false) => {
  editingStaff.value = stf ? stf.id : null;
  if (stf) {
    staffForm.username = stf.username;
    staffForm.full_name = stf.full_name;
    staffForm.staff_id = stf.staff_id;
    staffForm.department = stf.department;
    staffForm.email = stf.email;
    staffForm.is_staff = stf.is_staff;
    staffForm.is_superuser = stf.is_superuser;
    staffForm.password = '';
  } else {
    staffForm.username = ''; staffForm.full_name = ''; staffForm.staff_id = ''; staffForm.department = ''; staffForm.password = ''; staffForm.email = '';
    staffForm.is_staff = true;
    staffForm.is_superuser = preferAdmin;
  }
  showStaffModal.value = true;
};

const handleStaffSubmit = async () => {
  submittingStaff.value = true;
  try {
    if (editingStaff.value) {
      await adminService.updateStaff(editingStaff.value, staffForm);
    } else {
      await adminService.createStaff(staffForm);
    }
    showStaffModal.value = false;
    await loadStaffList();
    loadAuditLogs();
  } catch (err) { 
    const msg = err.response?.data ? Object.values(err.response.data).flat().join(' ') : 'Error processing staff account.';
    alert(msg); 
  }
  finally { submittingStaff.value = false; }
};

const deleteStaff = async (id) => {
  if (!confirm('Are you sure you want to remove this staff account?')) return;
  try { await adminService.deleteStaff(id); await loadStaffList(); loadAuditLogs(); } catch (err) { alert('Failed to delete staff.'); }
};



// ── Document Management ──────────────────────────────────────────────────────
const loadDocTypes = async () => {
  try { const res = await adminService.getDocTypes(); docTypes.value = res.data; } catch (err) { console.error('Docs error:', err); }
};

const openDocModal = (doc = null) => {
  editingDoc.value = doc ? doc.id : null;
  if (doc) {
    docForm.name = doc.name;
    docForm.description = doc.description;
    docForm.price = doc.price;
    docForm.is_active = doc.is_active;
  } else {
    docForm.name = ''; docForm.description = ''; docForm.price = 0; docForm.is_active = true;
  }
  showDocModal.value = true;
};

const handleDocSubmit = async () => {
  submittingDoc.value = true;
  try {
    if (editingDoc.value) {
      await adminService.updateDocType(editingDoc.value, docForm);
    } else {
      await adminService.createDocType(docForm);
    }
    showDocModal.value = false;
    await loadDocTypes();
    loadAuditLogs();
  } catch (err) { alert('Error saving document type.'); }
  finally { submittingDoc.value = false; }
};

const deleteDoc = async (id) => {
  if (!confirm('Are you sure you want to remove this document type?')) return;
  try { await adminService.deleteDocType(id); await loadDocTypes(); loadAuditLogs(); } catch (err) { alert('Failed to delete document.'); }
};

// ── Helpers ──────────────────────────────────────────────────────────────────
const initials = (first, last) => `${first?.[0] || ''}${last?.[0] || ''}`.toUpperCase();
const formatDate = (dt) => {
  if (!dt) return '—';
  return new Date(dt).toLocaleDateString('en-PH', { year: 'numeric', month: 'short', day: 'numeric' });
};
const formatDateFull = (dt) => {
  if (!dt) return '—';
  return new Date(dt).toLocaleDateString('en-PH', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
};
const formatDateTime = (dt) => {
  if (!dt) return '—';
  return new Date(dt).toLocaleString('en-PH', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
};
const copyPassKey = (key) => {
  if (!key) return;
  navigator.clipboard.writeText(key)
    .then(() => {
      // Small visual feedback could be added here if needed
      console.log('Pass Key copied');
    })
    .catch(err => console.error('Copy failed:', err));
};
const statusClass = (s) => ({
  'bg-amber-100 text-amber-600 border border-amber-200 shadow-amber-100': s === 'Pending',
  'bg-orange-100 text-orange-600 border border-orange-200 shadow-orange-100': s === 'Needs Verification',
  'bg-cyan-100 text-cyan-600 border border-cyan-200 shadow-cyan-100': s === 'Processing',
  'bg-green-100 text-green-600 border border-green-200 shadow-green-100': s === 'Approved',
  'bg-purple-100 text-purple-600 border border-purple-200 shadow-purple-100': s === 'Completed',
  'bg-red-100 text-red-600 border border-red-200 shadow-red-100': s === 'Rejected',
});
const strandPercent = (count) => {
  const total = stats.value.total || 1;
  return Math.round((count / total) * 100);
};

const handleLogout = () => { authService.logout(); router.push('/admin/login'); };

// ── Students Handlers ──────────────────────────────────────────────────────────
const loadStudents = async () => {
  loadingStudents.value = true;
  try {
    const params = { search: searchQuery.value };
    if (strandFilter.value) params.strand = strandFilter.value;
    if (yearFilter.value) params.year = yearFilter.value;
    const res = await adminService.getStudents(params);
    students.value = res.data;
  } catch (err) {
    console.error('Students error:', err);
  } finally {
    loadingStudents.value = false;
    loadingStudents.value = false;
  }
};

const missingDocsFilter = ref(false);

const filteredStudents = computed(() => {
  if (!students.value) return [];
  if (missingDocsFilter.value) {
    return students.value.filter(s => !s.documents || s.documents.length === 0);
  }
  return students.value;
});

const openStudentModal = (student = null) => {
  editingStudent.value = student;
  if (student) {
    Object.keys(studentForm).forEach(key => studentForm[key] = student[key] || '');
  } else {
    Object.keys(studentForm).forEach(key => {
        if (key === 'sex') studentForm[key] = 'Male';
        else studentForm[key] = '';
    });
  }
  showStudentModal.value = true;
};

const handleStudentSubmit = async () => {
  submittingStudent.value = true;
  try {
    if (editingStudent.value) {
      await adminService.updateStudent(editingStudent.value.id, studentForm);
    } else {
      await adminService.createStudent(studentForm);
    }
    showStudentModal.value = false;
    loadStudents();
  } catch (err) {
    const msg = err.response?.data ? JSON.stringify(err.response.data) : 'Failed to save student.';
    alert(msg);
  } finally {
    submittingStudent.value = false;
  }
};

const deleteStudent = async (id) => {
  if (confirm('Are you sure you want to delete this student record?')) {
    try {
      await adminService.deleteStudent(id);
      loadStudents();
    } catch (err) {
      console.error('Delete student error:', err);
    }
  }
};

// ── Student Documents Modal Handlers ──────────────────────────────────────────
const showStudentDocsModal = ref(false);
const selectedStudentForDocs = ref(null); // stores only the student's ID
const studentDocsModalRef = ref(null);
const uploadingMasterDoc = ref(false);
const masterDocForm = reactive({ document_type: '' });
const masterDocFile = ref(null);

// Reactively derive the live student object so the docs list auto-updates
const liveSelectedStudent = computed(() =>
  students.value.find(s => s.id === selectedStudentForDocs.value) || null
);

// ── Unified Student Profile Modal ──────────────────────────────────────────────
const showStudentProfileModal = ref(false);

const openStudentProfileModal = (student) => {
  selectedStudentForDocs.value = student.id; // Keep this state for document uploading
  showStudentProfileModal.value = true;
};

const masterDocFileInput = ref(null);

const onMasterDocFileChange = (e) => { 
  masterDocFile.value = e.target.files[0]; 
};

const handleMasterDocUpload = async () => {
  if (!masterDocForm.document_type) {
    alert('Please select a Document Type from the dropdown.');
    return;
  }
  if (!masterDocFile.value) {
    alert('Please select a file to upload.');
    return;
  }
  uploadingMasterDoc.value = true;
  try {
    const fd = new FormData();
    fd.append('file', masterDocFile.value);
    fd.append('document_type', masterDocForm.document_type);
    const res = await adminService.uploadStudentMasterDoc(selectedStudentForDocs.value, fd);
    
    // Update local state immediately for instant feedback
    const student = students.value.find(s => s.id === selectedStudentForDocs.value);
    if (student) {
      if (!student.documents) student.documents = [];
      student.documents.unshift(res.data); // Add to the top of the list
    }

    // Reset form
    masterDocForm.document_type = '';
    masterDocFile.value = null;
    if (studentDocsModalRef.value?.fileInput) {
      studentDocsModalRef.value.fileInput.value = '';
    }
    
    // Also background refresh to ensure full sync
    loadStudents();
  } catch (err) {
    console.error('Upload error:', err);
    alert('Failed to upload document.');
  } finally {
    uploadingMasterDoc.value = false;
  }
};

const handleDeleteMasterDoc = async (docId) => {
  if (!confirm('Are you sure you want to delete this document?')) return;
  try {
    await adminService.deleteStudentMasterDoc(docId);
    
    // Update local state immediately
    const student = students.value.find(s => s.id === selectedStudentForDocs.value);
    if (student && student.documents) {
      student.documents = student.documents.filter(d => d.id !== docId);
    }
    
    // Background refresh
    loadStudents();
  } catch (err) {
    console.error('Delete error:', err);
    alert('Failed to delete document.');
  }
};

watch(() => route.params.tab, (v) => {
  if (v === 'record_requests') { loadRequests(); loadDocTypes(); loadStrands(); }
  if (v === 'staff_management' || v === 'admin_management') loadStaffList();
  if (v === 'audit_logs') loadAuditLogs();

  if (v === 'document_types') loadDocTypes();
  if (v === 'strand_settings') loadStrands();
  if (v === 'student_directory') { loadStudents(); loadDocTypes(); }
}, { immediate: true });

onMounted(async () => {
  const userData = localStorage.getItem('user');
  if (!userData) { router.push('/admin/login'); return; }
  user.value = JSON.parse(userData);

  if (!route.params.tab) {
    router.replace('/admin/dashboard/overview');
  }

  await loadStats();
  loadDocTypes();
  loadStrands();
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

</script>

<style>
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* Mobile backdrop transition */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
