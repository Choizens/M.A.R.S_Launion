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
    <div class="flex-1 flex items-center justify-center p-6 md:p-12 relative overflow-hidden">
      <!-- Ambient overlay for better contrast -->
      <div class="absolute inset-0 bg-[#103059]/40 backdrop-blur-[2px]"></div>

      <div class="flex flex-col lg:flex-row w-full max-w-6xl gap-12 lg:gap-24 items-center relative z-10">
        <!-- Left Info Content -->
        <div class="flex-1 flex flex-col items-center text-center pb-8 lg:pb-0">
          <div class="mb-6 md:mb-10 flex justify-center">
            <img :src="logoImg" alt="La Union Senior High School" class="w-56 h-56 md:w-80 md:h-80 object-contain drop-shadow-[0_0_25px_rgba(255,255,255,0.3)] animate-pulse-slow" />
          </div>
          
          <div class="flex flex-col gap-4 max-w-[480px]">
            <div>
              <h3 class="text-2xl md:text-3xl font-black mb-4 uppercase tracking-widest text-[#ffca28] drop-shadow-md">Admin Access</h3>
              <p class="text-base md:text-lg leading-relaxed text-slate-100 font-medium">
                Secure access for authorized administrators only. Manage records, monitor student document requests, and oversee system operations with the M.A.R.S Administrative Portal.
              </p>
            </div>
          </div>
        </div>

        <!-- Right Form Content -->
        <div class="flex-1 flex justify-center relative w-full">
          <div class="bg-white py-10 px-8 md:px-12 rounded-lg shadow-2xl w-full max-w-[420px] relative z-20 border-t-8 border-[#103059]">
            <!-- Admin Icon Header -->
            <div class="flex justify-center mb-6">
               <div class="w-20 h-20 bg-[#103059] rounded-full flex items-center justify-center text-white shadow-lg">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
               </div>
            </div>
            
            <h1 class="text-[2.2rem] font-black text-center mb-1 text-[#111827] tracking-tight uppercase">Admin</h1>
            <p class="text-center text-slate-500 text-[0.7rem] font-bold uppercase tracking-[0.3em] mb-10">Management Portal</p>
            
            <form @submit.prevent="handleLogin" class="flex flex-col gap-6">
              <div class="flex flex-col gap-2">
                <label for="username" class="text-[0.85rem] font-bold text-[#103059] uppercase tracking-wider">Username <span class="text-red-500">*</span></label>
                <input 
                  type="text" 
                  id="username" 
                  v-model="username" 
                  required
                  placeholder="Enter administrator username"
                  class="w-full py-3 px-4 border-2 border-slate-200 rounded-md text-[1rem] text-slate-800 transition-all duration-200 focus:outline-none focus:border-[#103059] focus:ring-0 placeholder:text-slate-300 placeholder:font-normal"
                />
              </div>
              <div class="flex flex-col gap-2">
                <label for="password" class="text-[0.85rem] font-bold text-[#103059] uppercase tracking-wider">Password <span class="text-red-500">*</span></label>
                <input 
                  type="password" 
                  id="password" 
                  v-model="password" 
                  required
                  placeholder="Enter secure password"
                  class="w-full py-3 px-4 border-2 border-slate-200 rounded-md text-[1rem] text-slate-800 transition-all duration-200 focus:outline-none focus:border-[#103059] focus:ring-0 placeholder:text-slate-300 placeholder:font-normal"
                />
              </div>
              
              <!-- Improved Error Message -->
              <div v-if="error" class="text-red-600 text-[0.7rem] text-center bg-red-50 border-l-4 border-red-500 p-3 rounded shadow-sm font-black uppercase tracking-wider animate-shake">
                <div class="flex items-center justify-center gap-2">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                  {{ error }}
                </div>
              </div>

              <div class="flex justify-center mt-6">
                <button type="submit" :disabled="loading" class="w-full py-4 px-6 font-black text-[1rem] rounded-md bg-[#103059] hover:bg-[#1a4a8a] text-white transition-all shadow-xl hover:shadow-2xl disabled:opacity-70 disabled:cursor-not-allowed uppercase tracking-widest active:scale-[0.98]">
                  <span v-if="loading" class="flex items-center justify-center gap-2">
                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Verifying...
                  </span>
                  <span v-else>Authorize Access</span>
                </button>
              </div>
            </form>

            <div class="mt-10 pt-6 border-t border-slate-100 text-center">
              <router-link to="/Staff/login" class="text-[0.75rem] font-bold text-slate-400 hover:text-[#103059] transition-all uppercase tracking-widest flex items-center justify-center gap-2 group">
                <span class="transition-transform group-hover:-translate-x-1">←</span> Return to Staff Portal
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

    // Only allow admins
    if (!userData.is_admin) {
      error.value = 'Access denied. Administrators only.';
      return;
    }

    // Store tokens
    localStorage.setItem('token', response.data.access);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('is_admin', userData.is_admin ? 'true' : 'false');
    localStorage.setItem('is_superuser', userData.is_superuser ? 'true' : 'false');

    router.push('/admin/dashboard');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Authentication failed';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@keyframes pulse-slow {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0 15px rgba(255,255,255,0.2)); }
  50% { transform: scale(1.02); filter: drop-shadow(0 0 30px rgba(255,255,255,0.4)); }
}
.animate-pulse-slow {
  animation: pulse-slow 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
.animate-shake {
  animation: shake 0.2s ease-in-out infinite;
  animation-iteration-count: 2;
}

/* Ensure Poppins or similar is used */
:deep(body) {
  font-family: 'Inter', 'Poppins', sans-serif;
}
</style>
