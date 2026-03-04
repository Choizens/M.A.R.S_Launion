<template>
  <div id="top" class="min-h-screen bg-slate-50 flex flex-col">
    <!-- Navbar (Simplified/Same as Home) -->
    <nav class="border-[#103059] border-t-10 shadow-lg bg-white">
      <div class="flex flex-col md:flex-row max-w-screen-2xl mx-auto justify-between items-center py-6 px-6 md:px-12 gap-4 md:gap-0">
        <div class="flex items-center gap-2.5">
          <router-link to="/">
            <img :src="logoImg" alt="Logo" class="object-contain" />
          </router-link>
        </div>
        <div class="flex flex-wrap justify-center items-center gap-4 md:gap-8 lg:gap-12 text-base md:text-sm">
          <router-link to="/" class="hover:text-cyan-500 transition-all">Home</router-link>
          <router-link to="/requestor/find-lrn" class="text-cyan-500 font-bold transition-all">FIND-LRN</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Section -->
    <main class="flex-1 flex flex-col items-center justify-center py-12 px-6">
      <div class="w-full max-w-2xl bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
        <!-- Header -->
        <div class="bg-[#154252] p-8 text-white relative">
          <div class="relative z-10">
            <h1 class="text-2xl font-black tracking-tight uppercase">Find Your LRN</h1>
            <p class="text-slate-300 text-sm mt-1">Please provide your details exactly as they appear in school records.</p>
          </div>
          <!-- Decorative element -->
          <div class="absolute top-0 right-0 w-32 h-full opacity-10 pointer-events-none overflow-hidden">
             <div class="w-24 h-24 border-4 border-white rounded-full -mr-10 -mt-10"></div>
          </div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleFindLrn" class="p-8 space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- First Name -->
            <div class="flex flex-col">
              <label class="text-[0.65rem] font-black text-slate-500 uppercase tracking-widest mb-1.5">First Name <span class="text-red-500">*</span></label>
              <input v-model="form.first_name" type="text" required placeholder="e.g. Juan" 
                class="w-full border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] transition-colors" />
            </div>

            <!-- Last Name -->
            <div class="flex flex-col">
              <label class="text-[0.65rem] font-black text-slate-500 uppercase tracking-widest mb-1.5">Last Name <span class="text-red-500">*</span></label>
              <input v-model="form.last_name" type="text" required placeholder="e.g. Dela Cruz" 
                class="w-full border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] transition-colors" />
            </div>

            <!-- Middle Name -->
            <div class="flex flex-col">
              <label class="text-[0.65rem] font-black text-slate-500 uppercase tracking-widest mb-1.5">Middle Name</label>
              <input v-model="form.middle_name" type="text" placeholder="Optional" 
                class="w-full border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] transition-colors" />
            </div>

            <!-- Suffix -->
            <div class="flex flex-col">
              <label class="text-[0.65rem] font-black text-slate-500 uppercase tracking-widest mb-1.5">Suffix (Optional)</label>
              <input v-model="form.suffix" type="text" placeholder="e.g. Jr., III" 
                class="w-full border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] transition-colors" />
            </div>

            <!-- SEX -->
            <div class="flex flex-col">
              <label class="text-[0.65rem] font-black text-slate-500 uppercase tracking-widest mb-1.5">Sex <span class="text-red-500">*</span></label>
              <select v-model="form.sex" required 
                class="w-full border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] transition-colors bg-white appearance-none cursor-pointer">
                <option value="" disabled>Select...</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>

            <!-- Strand -->
            <div class="flex flex-col">
              <label class="text-[0.65rem] font-black text-slate-500 uppercase tracking-widest mb-1.5">Strand <span class="text-red-500">*</span></label>
              <select v-model="form.strand" required 
                class="w-full border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] transition-colors bg-white appearance-none cursor-pointer">
                <option value="" disabled>Select Strand</option>
                <option v-for="s in strands" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
            </div>

            <!-- Year Graduate -->
            <div class="flex flex-col">
              <label class="text-[0.65rem] font-black text-slate-500 uppercase tracking-widest mb-1.5">Year Graduated <span class="text-red-500">*</span></label>
              <input v-model="form.year_graduated" type="text" required placeholder="e.g. 2024" 
                class="w-full border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-[#154252] focus:ring-1 focus:ring-[#154252] transition-colors" />
            </div>
          </div>

          <div v-if="error" class="text-red-500 text-sm font-bold bg-red-50 p-3 rounded-lg border border-red-100 italic">
            {{ error }}
          </div>

          <button type="submit" :disabled="loading"
            class="w-full py-4 bg-yellow-400 hover:bg-yellow-500 text-slate-900 font-black uppercase tracking-widest rounded-xl shadow-lg transition-all active:scale-[0.98] disabled:opacity-50 flex items-center justify-center gap-3">
            <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-2 border-slate-900 border-t-transparent"></span>
            {{ loading ? 'Searching...' : 'FIND-LRN' }}
          </button>
        </form>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-[#103059] text-slate-300 py-10 border-t-8 border-yellow-400">
      <div class="max-w-7xl mx-auto px-12 flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="flex items-center gap-3">
          <img :src="logoImgFoot" alt="Logo" class="h-8 object-contain" />
          <span class="text-sm font-bold italic">StandAlone - La Union SHS</span>
        </div>
        <p class="text-xs">&copy; {{ new Date().getFullYear() }} All rights reserved.</p>
      </div>
    </footer>

    <!-- Result Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
        <div class="bg-white w-full max-w-sm rounded-3xl shadow-2xl border-4 border-[#154252] overflow-hidden animate-in zoom-in duration-300">
          <div class="bg-[#154252] p-6 text-center">
            <div class="w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4 border-4 border-white/20">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-[#154252]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 class="text-white font-black uppercase tracking-tight text-xl">Record Found!</h2>
          </div>
          
          <div class="p-8 text-center bg-white">
            <p class="text-slate-500 font-bold uppercase tracking-widest text-[0.6rem] mb-2">Student LRN</p>
            <div class="bg-slate-100 p-6 rounded-2xl border-2 border-dashed border-[#154252]/30 mb-6">
               <span class="text-3xl font-black text-[#154252] tracking-widest">{{ foundLrn }}</span>
            </div>
            <p class="text-sm text-slate-600 font-medium mb-8">
              Hello, <strong>{{ foundName }}</strong>!<br/>You can now use this LRN to make your document requests.
            </p>
            
            <button @click="closeModal" class="w-full py-4 bg-[#154252] text-white font-black uppercase tracking-widest rounded-xl hover:bg-[#0d2a35] transition-all active:scale-[0.98]">
              Thank You
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { publicService, requestService } from '@/services/api';
import logoImg from '@/assets/logo_launion.svg';

const router = useRouter();
const logoImgFoot = logoImg;

const strands = ref([]);
const loading = ref(false);
const error = ref('');
const showModal = ref(false);
const foundLrn = ref('');
const foundName = ref('');

const form = ref({
  first_name: '',
  last_name: '',
  middle_name: '',
  suffix: '',
  sex: '',
  strand: '',
  year_graduated: ''
});

onMounted(async () => {
  try {
    const res = await requestService.getPublicStrands();
    strands.value = res.data;
  } catch (e) {
    console.error('Error fetching strands:', e);
  }
});

const handleFindLrn = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    const params = {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      middle_name: form.value.middle_name,
      suffix: form.value.suffix,
      sex: form.value.sex,
      strand: form.value.strand,
      year_graduated: form.value.year_graduated
    };
    
    const res = await publicService.checkRecord(params);
    
    if (res.data.exists) {
      foundLrn.value = res.data.lrn_number;
      foundName.value = res.data.full_name;
      showModal.value = true;
    } else {
      error.value = res.data.message || 'No digital record found.';
    }
  } catch (e) {
    console.error('Error finding LRN:', e);
    error.value = e.response?.data?.error || e.response?.data?.message || 'Something went wrong. Please try again.';
  } finally {
    loading.value = false;
  }
};

const closeModal = () => {
  showModal.value = false;
};
</script>

<style scoped>
.border-t-10 {
  border-top-width: 10px;
}
</style>
