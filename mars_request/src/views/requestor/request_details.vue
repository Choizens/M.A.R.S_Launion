<template>
  <div class="min-h-screen font-sans" style="background-color: #f5f5e8;">
    <!-- Navbar -->
    <nav class="flex justify-between items-center py-3 px-8 bg-[#154252]">
      <div class="flex items-center gap-2.5">
        <img :src="logoImg" alt="Logo" class="w-9 h-9 object-contain" />
        <div class="flex flex-col leading-tight">
          <span class="font-bold text-white text-sm">StandAlone</span>
          <span class="text-[0.6rem] text-[#a3c2c2] font-medium whitespace-nowrap">La Union Senior High School</span>
        </div>
      </div>
      <div class="flex items-center gap-10 text-[0.9rem]">
        <router-link to="/requestor/home" class="text-cyan-400 font-bold">Home</router-link>
        <a href="#" class="text-white font-medium hover:text-cyan-400 transition-colors">Navigation</a>
        <a href="#" class="text-white font-medium hover:text-cyan-400 transition-colors">Navigation</a>
        <a href="#" class="text-white font-medium hover:text-cyan-400 transition-colors">Navigation</a>
        <button @click="goBack" class="px-5 py-2 rounded font-bold text-slate-900 bg-[#2ec4b6] hover:bg-[#26a89d] transition-colors whitespace-nowrap text-sm">
          Check Your Request
        </button>
      </div>
    </nav>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <div class="w-12 h-12 border-4 border-[#154252] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
        <p class="text-slate-500 font-medium">Fetching your request...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex items-center justify-center min-h-[60vh] px-4">
      <div class="text-center">
        <div class="w-16 h-16 rounded-full bg-red-100 flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-slate-800 mb-2">Request Not Found</h2>
        <p class="text-slate-500 text-sm mb-6">{{ error }}</p>
        <button @click="goBack" class="px-6 py-2 bg-[#154252] text-white font-bold rounded-lg hover:bg-[#0d2a35] transition-colors">Go Back</button>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else-if="requestData" class="max-w-6xl mx-auto px-8 py-10 grid grid-cols-3 gap-10">

      <!-- Left: Status Panel (2/3 width) -->
      <div class="col-span-2 flex flex-col gap-5">
        <div>
          <h1 class="text-3xl font-black text-[#154252]">Status of your Request</h1>
          <p class="text-slate-500 mt-1 text-sm">incididunt ut labore et dolore magna aliqua. Ut ea</p>
        </div>

        <!-- Request Code + Status + Stepper Card -->
        <div class="rounded-lg overflow-hidden border border-slate-300 bg-white shadow-sm">
          <!-- Code Bar -->
          <div class="bg-[#154252] px-6 py-3 flex items-center justify-between">
            <span class="font-black text-white text-base tracking-widest font-mono">{{ requestData.request_code }}</span>
            <span class="text-yellow-400 font-bold text-sm">{{ requestData.status }}</span>
          </div>

          <!-- Stepper + Docs inside white area -->
          <div class="bg-white px-8 py-7">
            <!-- Stepper Row -->
            <div class="flex items-center justify-start gap-0 mb-1 relative" style="max-width: 360px;">
              <!-- Step 1 -->
              <div class="flex flex-col items-center z-10">
                <div :class="step >= 1 ? 'bg-yellow-400 text-slate-900' : 'bg-slate-200 text-slate-400'"
                     class="w-9 h-9 rounded-full flex items-center justify-center font-black text-sm shadow">1</div>
                <span :class="step >= 1 ? 'text-yellow-600' : 'text-slate-400'" class="text-[10px] font-bold mt-1">Pending</span>
              </div>
              <!-- Dashed line 1-->
              <div class="flex-1 relative" style="height:2px; min-width:80px; top:-8px;">
                <div class="absolute inset-0 border-t-2 border-dashed border-slate-300"></div>
              </div>
              <!-- Step 2 -->
              <div class="flex flex-col items-center z-10">
                <div :class="step >= 2 ? 'bg-yellow-400 text-slate-900' : 'bg-slate-100 text-slate-400'"
                     class="w-9 h-9 rounded-full flex items-center justify-center font-black text-sm border border-slate-300">2</div>
                <span :class="step >= 2 ? 'text-yellow-600' : 'text-slate-400'" class="text-[10px] font-bold mt-1">Pick up</span>
              </div>
              <!-- Dashed line 2 -->
              <div class="flex-1 relative" style="height:2px; min-width:80px; top:-8px;">
                <div class="absolute inset-0 border-t-2 border-dashed border-slate-300"></div>
              </div>
              <!-- Step 3 -->
              <div class="flex flex-col items-center z-10">
                <div :class="step >= 3 ? 'bg-yellow-400 text-slate-900' : 'bg-slate-100 text-slate-400'"
                     class="w-9 h-9 rounded-full flex items-center justify-center font-black text-sm border border-slate-300">3</div>
                <span :class="step >= 3 ? 'text-yellow-600' : 'text-slate-400'" class="text-[10px] font-bold mt-1">Received</span>
              </div>
            </div>

            <!-- Requested Documents -->
            <div class="mt-6">
              <p class="text-xs font-bold text-slate-600 mb-3">Requested Documents:</p>
              <div class="flex flex-wrap gap-4">
                <div
                  v-for="(file, index) in requestData.requested_files"
                  :key="index"
                  class="relative w-[120px] rounded-lg overflow-hidden border border-slate-300 bg-white shadow-sm"
                >
                  <!-- Blurred document body -->
                  <div class="w-full h-28 bg-slate-50 relative overflow-hidden flex items-end justify-center">
                    <!-- Document fake lines blur -->
                    <div class="absolute inset-0 p-2 flex flex-col gap-1 blur-[1.5px] opacity-70">
                      <div class="flex gap-1 mb-1">
                        <div class="w-5 h-5 bg-slate-300 rounded-sm flex-shrink-0"></div>
                        <div class="flex flex-col gap-0.5 flex-1">
                          <div class="h-1.5 bg-slate-300 rounded w-3/4"></div>
                          <div class="h-1.5 bg-slate-300 rounded w-1/2"></div>
                        </div>
                      </div>
                      <div class="h-1.5 bg-slate-300 rounded w-full"></div>
                      <div class="h-1.5 bg-slate-300 rounded w-4/5"></div>
                      <div class="h-1.5 bg-slate-300 rounded w-full"></div>
                      <div class="h-1.5 bg-slate-300 rounded w-2/3"></div>
                      <div class="h-1.5 bg-slate-300 rounded w-full"></div>
                      <div class="h-1.5 bg-slate-300 rounded w-3/5"></div>
                      <div class="h-1.5 bg-slate-300 rounded w-full"></div>
                      <div class="h-1.5 bg-red-200 rounded w-1/2"></div>
                    </div>
                    <!-- Document name overlay at bottom -->
                    <div class="absolute bottom-0 left-0 right-0 bg-white/80 px-2 py-1.5 text-center">
                      <p class="text-xs font-black text-slate-700 leading-tight">{{ file }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Sidebar (1/3 width) -->
      <div class="col-span-1 flex flex-col gap-4">
        <!-- Circles decoration (top right) -->
        <div class="flex justify-end gap-3">
          <div class="w-10 h-10 rounded-full bg-[#99dbce]"></div>
          <div class="w-10 h-10 rounded-full bg-[#99dbce]"></div>
        </div>

        <!-- Sidebar LOREM IPSUM section -->
        <div>
          <h3 class="text-lg font-black text-[#154252] mb-3">LOREM IPSUM</h3>
          <!-- Image + caption row -->
          <div class="flex gap-3 mb-3">
            <img :src="launionImg" alt="School" class="w-28 h-24 object-cover rounded flex-shrink-0" />
            <p class="text-slate-700 text-xs leading-relaxed mt-1">
              <strong>Lorem ipsum dolor sit amet,</strong> consectetur
            </p>
          </div>
          <p class="text-slate-700 text-xs leading-relaxed text-justify mb-3">
            incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
          </p>
          <p class="text-slate-700 text-xs leading-relaxed text-justify">
            <strong>Lorem ipsum</strong> dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import logoImg from '@/assets/form_logo.png';
import launionImg from '@/assets/launion.png';
import { requestService } from '@/services/api';

const route = useRoute();
const router = useRouter();

const loading = ref(true);
const error = ref('');
const requestData = ref(null);

onMounted(async () => {
  const code = route.params.code;
  try {
    const response = await requestService.lookupRequest(code);
    requestData.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load request. Please try again.';
  } finally {
    loading.value = false;
  }
});

function goBack() {
  router.push({ name: 'requestor-home' });
}

const step = computed(() => {
  if (!requestData.value) return 0;
  const s = requestData.value.status?.toLowerCase();
  if (s === 'received') return 3;
  if (s === 'processing' || s === 'approved') return 2;
  return 1; // Pending
});

const statusBadgeClass = computed(() => {
  const s = requestData.value?.status?.toLowerCase();
  if (s === 'approved') return 'bg-green-100 text-green-700';
  if (s === 'rejected') return 'bg-red-100 text-red-600';
  if (s === 'processing') return 'bg-blue-100 text-blue-600';
  return 'bg-yellow-100 text-yellow-700'; // pending
});
</script>

<style scoped>
</style>
