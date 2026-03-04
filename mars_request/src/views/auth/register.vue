<template>
  <div class="min-h-screen flex flex-col font-sans text-white bg-cover bg-center"
       :style="{ backgroundImage: `url(${bgImg})` }">
    <!-- Navbar -->
    <nav class="flex flex-col md:flex-row justify-between items-center py-4 px-6 md:px-12 bg-[#0a243a] border-b-2 border-white gap-4 md:gap-0">
      <div class="flex items-center gap-3">
        <img :src="formLogoImg" alt="Logo" class="w-8 h-8 object-contain" />
        <span class="font-bold text-sm tracking-tight text-slate-100 italic">La Union Senior High School</span>
      </div>
      <div class="flex flex-wrap justify-center items-center gap-4 md:gap-6 text-xs md:text-sm">
        <router-link to="/Staff/home" class="text-white font-medium transition-opacity hover:opacity-80">Home</router-link>
        <div class="flex gap-2.5">
          <router-link to="/Staff/login" class="px-3 md:px-5 py-1.5 rounded font-semibold text-slate-900 bg-amber-300 hover:bg-amber-400 transition-colors pointer shadow-sm cursor-pointer whitespace-nowrap">Login</router-link>
          <router-link to="/Staff/register" class="px-3 md:px-5 py-1.5 rounded font-semibold text-slate-900 bg-amber-300 hover:bg-amber-400 transition-colors pointer shadow-sm cursor-pointer whitespace-nowrap">Register</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col items-center py-8 md:py-12 px-4 md:px-8">
      <!-- Top Info -->
      <div class="flex flex-col lg:flex-row justify-center items-center lg:items-start gap-8 lg:gap-16 w-full max-w-6xl mb-8 md:mb-10">
        <div class="flex-1 max-w-[320px] text-center lg:text-right lg:mt-6">
          <h3 class="text-[1.1rem] md:text-[1.15rem] font-semibold mb-2 md:mb-3 text-center">Mission</h3>
          <p class="text-[0.75rem] md:text-[0.85rem] leading-relaxed text-slate-200">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco</p>
        </div>
        
        <div class="flex flex-col items-center text-center">
          <div class="flex justify-center mb-4 md:mb-5">
            <img :src="formLogoImg" alt="La Union Senior High School" class="w-40 h-40 md:w-56 md:h-56 object-contain drop-shadow-lg" />
          </div>
        </div>
 
        <div class="flex-1 max-w-[320px] text-center lg:text-left lg:mt-6">
          <h3 class="text-[1.1rem] md:text-[1.15rem] font-semibold mb-2 md:mb-3 text-center">Vision</h3>
          <p class="text-[0.75rem] md:text-[0.85rem] leading-relaxed text-slate-200">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.</p>
        </div>
      </div>
 
      <!-- Register Form -->
      <div class="w-full flex justify-center mt-2 md:mt-4 pb-8 relative">
        <div class="bg-white text-slate-800 py-8 md:py-12 px-6 md:px-12 lg:px-16 rounded-md w-full max-w-[850px] shadow-[0_10px_30px_rgba(0,0,0,0.35)] relative z-10">
          <h1 class="text-2xl md:text-4xl font-extrabold text-center mb-8 md:mb-10 text-slate-900 tracking-wide uppercase italic">Register</h1>
          <form @submit.prevent="handleRegister" class="flex flex-col gap-6">
            <!-- Row 1: Name Breakdown -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="flex flex-col gap-2">
                <label for="firstName" class="text-xs font-semibold text-slate-700">First Name <span class="text-red-500">*</span></label>
                <input type="text" id="firstName" v-model="uiForm.firstName" required class="p-3 border border-slate-400 rounded text-[0.95rem] transition-all duration-200 focus:outline-none focus:border-[#0d324d] focus:ring-2 focus:ring-[#0d324d]/15" />
              </div>
              <div class="flex flex-col gap-2">
                <label for="middleName" class="text-xs font-semibold text-slate-700">Middle Name</label>
                <input type="text" id="middleName" v-model="uiForm.middleName" class="p-3 border border-slate-400 rounded text-[0.95rem] transition-all duration-200 focus:outline-none focus:border-[#0d324d] focus:ring-2 focus:ring-[#0d324d]/15" />
              </div>
              <div class="flex flex-col gap-2">
                <label for="lastName" class="text-xs font-semibold text-slate-700">Last Name <span class="text-red-500">*</span></label>
                <input type="text" id="lastName" v-model="uiForm.lastName" required class="p-3 border border-slate-400 rounded text-[0.95rem] transition-all duration-200 focus:outline-none focus:border-[#0d324d] focus:ring-2 focus:ring-[#0d324d]/15" />
              </div>
            </div>

            <!-- Row 2: Contact & Access -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="flex flex-col gap-2">
                <label for="email" class="text-xs font-semibold text-slate-700">Email Address <span class="text-red-500">*</span></label>
                <input type="email" id="email" v-model="form.email" required class="p-3 border border-slate-400 rounded text-[0.95rem] transition-all duration-200 focus:outline-none focus:border-[#0d324d] focus:ring-2 focus:ring-[#0d324d]/15" />
              </div>
              <div class="flex flex-col gap-2">
                <label for="username" class="text-xs font-semibold text-slate-700">Username <span class="text-red-500">*</span></label>
                <input type="text" id="username" v-model="form.username" required class="p-3 border border-slate-400 rounded text-[0.95rem] transition-all duration-200 focus:outline-none focus:border-[#0d324d] focus:ring-2 focus:ring-[#0d324d]/15" />
              </div>
            </div>

            <!-- Row 3: Staff Status Details -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="flex flex-col gap-2">
                <label for="staff_id" class="text-xs font-semibold text-slate-700">Staff ID <span class="text-red-500">*</span></label>
                <input type="text" id="staff_id" v-model="form.staff_id" required class="p-3 border border-slate-400 rounded text-[0.95rem] transition-all duration-200 focus:outline-none focus:border-[#0d324d] focus:ring-2 focus:ring-[#0d324d]/15" />
              </div>
              <div class="flex flex-col gap-2">
                <label for="department" class="text-xs font-semibold text-slate-700">Department <span class="text-red-500">*</span></label>
                <input type="text" id="department" v-model="form.department" required class="p-3 border border-slate-400 rounded text-[0.95rem] transition-all duration-200 focus:outline-none focus:border-[#0d324d] focus:ring-2 focus:ring-[#0d324d]/15" />
              </div>
              <div class="flex flex-col gap-2">
                <label for="password" class="text-xs font-semibold text-slate-700">Password <span class="text-red-500">*</span></label>
                <input type="password" id="password" v-model="form.password" required class="p-3 border border-slate-400 rounded text-[0.95rem] transition-all duration-200 focus:outline-none focus:border-[#0d324d] focus:ring-2 focus:ring-[#0d324d]/15" />
              </div>
            </div>
            
            <div v-if="error" class="text-red-500 text-[0.85rem] text-center bg-red-100 p-2.5 rounded">
              {{ error }}
            </div>
            <div v-if="success" class="text-emerald-500 text-[0.85rem] text-center bg-emerald-100 p-2.5 rounded">
              Registration successful! Redirecting to login...
            </div>

            <div class="flex justify-center mt-6">
              <button type="submit" :disabled="loading" class="w-[140px] p-3 font-bold text-[0.95rem] rounded bg-amber-300 hover:bg-amber-400 text-slate-900 transition-colors disabled:opacity-70 disabled:cursor-not-allowed">
                <span v-if="loading">Registering...</span>
                <span v-else>Register</span>
              </button>
            </div>
          </form>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '@/services/api';
import bgImg from '@/assets/Launion_backend.svg';
import formLogoImg from '@/assets/form_logo.png';

const router = useRouter();
const loading = ref(false);
const error = ref('');
const success = ref(false);

const uiForm = reactive({
  firstName: '',
  middleName: '',
  lastName: ''
});

const form = reactive({
  username: '',
  email: '',
  staff_id: '',
  department: '',
  full_name: '',
  password: '',
});

const handleRegister = async () => {
  error.value = '';
  loading.value = true;
  
  // Combine full name
  const middle = uiForm.middleName.trim();
  form.full_name = `${uiForm.firstName.trim()} ${middle ? middle + ' ' : ''}${uiForm.lastName.trim()}`;
  
  try {
    await authService.register(form);
    success.value = true;
    setTimeout(() => {
      router.push('/Staff/login');
    }, 2000);
  } catch (err) {
    if (err.response?.data) {
      const firstError = Object.values(err.response.data)[0];
      error.value = Array.isArray(firstError) ? firstError[0] : firstError;
    } else {
      error.value = 'Registration failed. Please try again.';
    }
  } finally {
    loading.value = false;
  }
};
</script>
