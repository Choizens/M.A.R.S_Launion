<template>
  <!-- Outer: full-height column — header on top, body row below -->
  <div class="flex flex-col h-screen bg-[#f5f7fa] font-sans overflow-hidden">

    <!-- ===== TOP HEADER (spans full width) ===== -->
    <header class="h-16 bg-[#004d66] text-white flex items-center justify-between px-4 md:px-8 shadow-md z-50 shrink-0">
      <div class="flex items-center gap-3 mr-auto">
        <!-- Burger toggle -->
        <button
          @click="sidebarOpen = !sidebarOpen"
          class="p-2 hover:bg-white/10 rounded transition-colors focus:outline-none"
          title="Toggle Sidebar"
        >
          <MenuIcon class="w-6 h-6" />
        </button>

        <div class="hidden sm:flex flex-col">
          <h2 class="text-xs md:text-sm font-bold leading-tight uppercase tracking-wide">La Union SHS — Staff</h2>
          <p class="text-[0.55rem] opacity-60 tracking-widest uppercase">M.A.R.S Dashboard</p>
        </div>
      </div>

      <div class="flex items-center gap-4 md:gap-8">
        <div class="hidden md:flex flex-col text-right">
          <span class="text-xs italic opacity-90">Welcome, {{ user?.full_name || 'Staff' }}</span>
          <span class="text-[0.7rem] font-bold text-amber-300 uppercase leading-none mt-1">{{ user?.department || 'Office' }}</span>
        </div>
        <div class="relative cursor-pointer hover:opacity-80 transition-opacity">
          <BellIcon class="w-6 h-6" />
          <span v-if="pendingCount > 0" class="absolute -top-1.5 -right-1.5 bg-red-500 text-white text-[0.6rem] font-bold px-1.5 py-0.5 rounded-full border-2 border-[#004d66]">
            {{ pendingCount }}
          </span>
        </div>
      </div>
    </header>

    <!-- ===== BODY ROW (sidebar + content, BELOW header) ===== -->
    <div class="flex flex-1 overflow-hidden">

      <!-- Mobile Overlay Backdrop -->
      <Transition name="fade">
        <div
          v-if="sidebarOpen && isMobile"
          class="fixed inset-0 bg-black/50 z-30 top-16"
          @click="sidebarOpen = false"
        />
      </Transition>

      <!-- Sidebar -->
      <aside
        :class="[
          'bg-[#00334d] text-white flex flex-col transition-all duration-300 ease-in-out shadow-xl shrink-0',
          isMobile ? (
            sidebarOpen ? 'fixed top-16 left-0 bottom-0 w-72 translate-x-0 z-40' : 'fixed top-16 left-0 bottom-0 w-72 -translate-x-full z-40'
          ) : (
            sidebarOpen ? 'w-64' : 'w-16'
          )
        ]"
      >
        <!-- Sidebar Nav -->
        <nav class="flex-grow pt-4 overflow-y-auto overflow-x-hidden">
          <ul class="flex flex-col">
            <li
              v-for="item in menuItems"
              :key="item.id"
              @click="navigateTo(item.id)"
              :class="[
                'group flex items-center px-4 py-3.5 cursor-pointer transition-colors border-b border-white/5 relative',
                currentView === item.id ? 'bg-[#ffca28] text-[#0d324d]' : 'hover:bg-white/10'
              ]"
              :title="!sidebarOpen ? item.label : ''"
            >
              <div
                class="flex items-center min-w-[24px] justify-center shrink-0"
                :class="!sidebarOpen && !isMobile ? 'mx-auto' : ''"
              >
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
              <!-- Pending badge -->
              <span
                v-if="sidebarOpen && item.id === 'requests' && pendingCount > 0"
                class="ml-auto bg-red-500 text-white text-[0.6rem] font-bold px-1.5 py-0.5 rounded-full shrink-0"
              >
                {{ pendingCount }}
              </span>
              <!-- Active bar for collapsed desktop -->
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

      <!-- Main Content Area -->
      <main class="flex-1 overflow-y-auto p-6 md:p-8 lg:p-12">
        <div class="max-w-7xl mx-auto">
          <StaffOverview
            v-if="currentView === 'overview'"
            @open-request="openModal"
          />
          <StaffRequests
            v-if="currentView === 'requests'"
            @open-request="openModal"
            ref="requestsTab"
          />
          <StaffDirectory
            v-if="currentView === 'directory'"
          />
          <StaffProfile
            v-if="currentView === 'profile'"
          />
        </div>
      </main>
    </div>

    <!-- Details Modal -->
    <DetailsModal
       v-if="selectedRequest"
       :request="selectedRequest"
       @close="closeModal"
       @refresh="refreshActiveTab"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, markRaw, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { authService, adminService } from '@/services/api';
import logoImg from '@/assets/form_logo.png';

// Tab Components
import StaffOverview from './tabs/StaffOverview.vue';
import StaffRequests from './tabs/StaffRequests.vue';
import StaffDirectory from './tabs/StaffDirectory.vue';
import StaffProfile from './tabs/StaffProfile.vue';
import DetailsModal from './components/RequestDetailModal.vue';

import {
  Menu as MenuIcon, LayoutDashboard as DashboardIcon,
  List as ListIcon, Users as UsersIcon, User as AccountIcon,
  LogOut as LogOutIcon, Bell as BellIcon
} from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();
const user = ref(null);

// Responsive sidebar state
const sidebarOpen = ref(window.innerWidth >= 768);
const isMobile = ref(window.innerWidth < 768);

const handleResize = () => {
  const mobile = window.innerWidth < 768;
  isMobile.value = mobile;
  if (mobile) sidebarOpen.value = false;
};
window.addEventListener('resize', handleResize);
onUnmounted(() => window.removeEventListener('resize', handleResize));

const navigateTo = (id) => {
  currentView.value = id;
  if (isMobile.value) sidebarOpen.value = false;
};

const pendingCount = ref(0);
const selectedRequest = ref(null);
const requestsTab = ref(null);

const menuItems = [
  { id: 'overview',   label: 'Summary',    icon: markRaw(DashboardIcon) },
  { id: 'requests',   label: 'Requests',   icon: markRaw(ListIcon) },
  { id: 'directory',  label: 'Directory',  icon: markRaw(UsersIcon) },
  { id: 'profile',    label: 'My Profile', icon: markRaw(AccountIcon) },
];

const currentView = computed({
  get: () => route.params.tab || 'overview',
  set: (val) => router.push(`/Staff/dashboard/${val}`)
});

const loadGlobalStats = async () => {
  try {
    const res = await adminService.getStats();
    pendingCount.value = res.data.pending || 0;
  } catch (err) { console.error(err); }
};

const openModal = (req) => { selectedRequest.value = req; };
const closeModal = () => { selectedRequest.value = null; };

const refreshActiveTab = () => {
  loadGlobalStats();
  if (requestsTab.value && requestsTab.value.refresh) {
    requestsTab.value.refresh();
  }
};

const handleLogout = () => {
  authService.logout();
  router.push('/Staff/login');
};

let statsInterval = null;

onMounted(() => {
  const userData = localStorage.getItem('user');
  if (!userData) { router.push('/Staff/login'); return; }
  user.value = JSON.parse(userData);
  loadGlobalStats();
  
  // Set up polling for new requests every 30 seconds
  statsInterval = setInterval(() => {
    loadGlobalStats();
  }, 30000);

  if (!route.params.tab) {
    router.replace('/Staff/dashboard/overview');
  }
});

onUnmounted(() => {
  if (statsInterval) clearInterval(statsInterval);
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
/* Mobile backdrop transition */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
