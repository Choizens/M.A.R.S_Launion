<template>
  <div class="min-h-screen flex flex-col font-sans text-white bg-cover bg-center"
       :style="{ backgroundImage: `url(${bgImg})` }">
    <!-- Navbar -->
    <nav class="flex flex-col md:flex-row justify-between items-center py-4 px-6 md:px-12 bg-[#103059] border-b-2 border-white gap-4 md:gap-0">
      <div class="flex items-center gap-3">
        <img :src="logoImg" alt="Logo" class="w-8 h-8 object-contain" />
        <span class="font-bold text-sm tracking-tight text-slate-100 italic">La Union Senior High School</span>
      </div>
      <div class="flex flex-wrap justify-center items-center gap-4 md:gap-6 text-xs md:text-sm">
        <router-link to="/" class="text-white font-medium transition-opacity hover:opacity-80">Home</router-link>
        <div class="flex gap-2.5 invisible">
          <router-link to="/Staff/login" class="px-3 md:px-5 py-1.5 rounded font-semibold text-slate-900 bg-amber-300 hover:bg-amber-400 transition-colors pointer shadow-sm cursor-pointer whitespace-nowrap">Staff Login</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="flex-1 flex items-center justify-center p-6 md:p-12">
      <div class="flex flex-col lg:flex-row w-full max-w-6xl gap-12 lg:gap-16 items-center">
        <!-- Left Info Content -->
        <div class="flex-1 flex flex-col items-center text-center pb-8">
          <div class="mb-6 md:mb-8 flex justify-center">
            <img :src="logoImg" alt="La Union Senior High School" class="w-48 h-48 md:w-64 md:h-64 object-contain drop-shadow-lg" />
          </div>
          
          <div class="flex flex-col gap-8 md:gap-10 max-w-[420px]">
            <div>
              <h3 class="text-base md:text-lg font-semibold mb-2 md:mb-3 uppercase tracking-widest text-amber-300">Admin Access</h3>
              <p class="text-[0.8rem] md:text-sm leading-relaxed text-slate-200 indent-8 text-justify italic">
                Secure access for authorized administrators only. Manage records, monitor student document requests, and oversee system operations with the M.A.R.S Administrative Portal.
              </p>
            </div>
          </div>
        </div>

        <!-- Right Form Content -->
        <div class="flex-1 flex justify-center relative w-full">
          <div class="bg-white py-8 md:py-10 px-6 md:px-10 rounded shadow-xl w-full max-w-[380px] relative z-10 border-t-4 border-[#103059]">
            <div class="flex justify-center mb-6">
               <div class="w-16 h-16 bg-[#103059] rounded-full flex items-center justify-center text-white">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
               </div>
            </div>
            <h1 class="text-[1.8rem] font-black text-center mb-2 text-[#111827] tracking-tight">ADMIN</h1>
            <p class="text-center text-slate-500 text-xs font-bold uppercase tracking-widest mb-8">Management Portal</p>
            
            <form @submit.prevent="handleLogin" class="flex flex-col gap-6">
              <div class="flex flex-col gap-1.5">
                <label for="username" class="text-[0.85rem] font-semibold text-[#103059]">Username <span class="text-red-500">*</span></label>
                <input 
                  type="text" 
                  id="username" 
                  v-model="username" 
                  required
                  class="w-full py-2.5 px-3 border border-slate-400 rounded text-[0.95rem] text-slate-800 transition-all duration-200 focus:outline-none focus:border-[#103059] focus:ring-1 focus:ring-[#103059]"
                />
              </div>
              <div class="flex flex-col gap-1.5">
                <label for="password" class="text-[0.85rem] font-semibold text-[#103059]">Password <span class="text-red-500">*</span></label>
                <input 
                  type="password" 
                  id="password" 
                  v-model="password" 
                  required
                  class="w-full py-2.5 px-3 border border-slate-400 rounded text-[0.95rem] text-slate-800 transition-all duration-200 focus:outline-none focus:border-[#103059] focus:ring-1 focus:ring-[#103059]"
                />
              </div>
              
              <div v-if="error" class="text-red-500 text-[0.65rem] text-center bg-red-50 border border-red-100 p-2.5 rounded font-bold uppercase">
                {{ error }}
              </div>

              <div class="flex justify-center mt-4">
                <button type="submit" :disabled="loading" class="w-full py-3.5 px-4 font-black text-[0.9rem] rounded bg-[#103059] hover:bg-[#103059] text-white transition-all shadow-md hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed uppercase tracking-widest">
                  <span v-if="loading">Verifying Identity...</span>
                  <span v-else>Authorize Access</span>
                </button>
              </div>
            </form>

            <div class="mt-8 pt-6 border-t border-slate-100 text-center">
              <router-link to="/Staff/login" class="text-[0.7rem] font-black text-slate-400 hover:text-[#103059] transition-colors uppercase tracking-widest">
                ← Return to Staff Portal
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authService } from '@/services/api';
import bgImg from '@/assets/Launion_backend.svg';
import logoImg from '@/assets/form_logo.png';

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

const handleLogin = async () => {
  error.value = '';
  loading.value = true;
  try {
    const response = await authService.login(username.value.trim(), password.value);
    const userData = response.data.user;

    // Only allow superusers / staff (Django is_superuser or is_staff)
    if (!userData.is_admin) {
      error.value = 'Access denied. Authorized administrators only.';
      return;
    }

    // Store tokens and user
    localStorage.setItem('token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('is_admin', userData.is_admin ? 'true' : 'false');
    localStorage.setItem('is_superuser', userData.is_superuser ? 'true' : 'false');

    router.push('/admin/dashboard');
  } catch (err) {
    const detail = err.response?.data?.detail;
    if (detail === 'No active account found with the given credentials') {
      error.value = 'Incorrect credentials';
    } else {
      error.value = detail || 'Authentication failed';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Inherited consistent design with Staff login */
</style>
