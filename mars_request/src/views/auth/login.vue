<template>
  <div class="min-h-screen flex flex-col font-sans text-white bg-cover bg-center"
       :style="{ backgroundImage: `url(${bgImg})` }">
    <!-- Navbar -->
    <nav class="flex flex-col md:flex-row justify-between items-center py-4 px-6 md:px-12 bg-[#0a243a] border-b-2 border-white gap-4 md:gap-0">
      <div class="flex items-center gap-3">
        <img :src="logoImg" alt="Logo" class="w-8 h-8 object-contain" />
        <span class="font-bold text-sm tracking-tight text-slate-100 italic">La Union Senior High School</span>
      </div>
      <div class="flex flex-wrap justify-center items-center gap-4 md:gap-6 text-xs md:text-sm">
        <router-link to="/" class="text-white font-medium transition-opacity hover:opacity-80">Home</router-link>
        <a href="#" class="hidden sm:inline text-white font-medium transition-opacity hover:opacity-80">About us</a>
        <a href="#" class="hidden sm:inline text-white font-medium transition-opacity hover:opacity-80">Contact</a>
        <div class="flex gap-2.5 invisible">
          <router-link to="/Staff/login" class="px-3 md:px-5 py-1.5 rounded font-semibold text-slate-900 bg-amber-300 hover:bg-amber-400 transition-colors pointer shadow-sm cursor-pointer whitespace-nowrap">Login</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="flex-1 flex items-center justify-center p-6 md:p-12">
      <div class="flex flex-col lg:flex-row w-full max-w-6xl gap-12 lg:gap-16 items-center">
        <!-- Left Info Content -->
        <div class="flex-1 flex flex-col items-center text-center pb-8">
          <div class="mb-6 md:mb-8 flex justify-center">
            <img :src="formLogoImg" alt="La Union Senior High School" class="w-48 h-48 md:w-64 md:h-64 object-contain drop-shadow-lg" />
          </div>
          
          <div class="flex flex-col gap-8 md:gap-10 max-w-[420px]">
            <div>
              <h3 class="text-base md:text-lg font-semibold mb-2 md:mb-3">Mission</h3>
              <p class="text-[0.8rem] md:text-sm leading-relaxed text-slate-200">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco</p>
            </div>
            <div>
              <h3 class="text-base md:text-lg font-semibold mb-2 md:mb-3">Vision</h3>
              <p class="text-[0.8rem] md:text-sm leading-relaxed text-slate-200">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.</p>
            </div>
          </div>
        </div>

        <!-- Right Form Content -->
        <div class="flex-1 flex justify-center relative w-full">
          <div class="bg-white py-8 md:py-10 px-6 md:px-10 rounded shadow-xl w-full max-w-[380px] relative z-10">
            <h1 class="text-[1.8rem] font-black text-center mb-8 text-[#111827] tracking-wide">LOGIN</h1>
            <form @submit.prevent="handleLogin" class="flex flex-col gap-6">
              <div class="flex flex-col gap-1.5">
                <label for="username" class="text-[0.85rem] font-semibold text-[#0d324d]">Username <span class="text-red-500">*</span></label>
                <input 
                  type="text" 
                  id="username" 
                  v-model="username" 
                  required
                  class="w-full py-2.5 px-3 border border-slate-400 rounded text-[0.95rem] text-slate-800 transition-all duration-200 focus:outline-none focus:border-[#004f71] focus:ring-1 focus:ring-[#004f71]"
                />
              </div>
              <div class="flex flex-col gap-1.5">
                <label for="password" class="text-[0.85rem] font-semibold text-[#0d324d]">Password <span class="text-red-500">*</span></label>
                <input 
                  type="password" 
                  id="password" 
                  v-model="password" 
                  required
                  class="w-full py-2.5 px-3 border border-slate-400 rounded text-[0.95rem] text-slate-800 transition-all duration-200 focus:outline-none focus:border-[#004f71] focus:ring-1 focus:ring-[#004f71]"
                />
              </div>
              
              <div v-if="error" class="text-red-500 text-sm text-center bg-red-100 p-2.5 rounded font-medium">
                {{ error }}
              </div>

              <div class="flex justify-center mt-4">
                <button type="submit" :disabled="loading" class="w-[140px] py-2.5 px-4 font-bold text-[0.9rem] rounded bg-[#ffca28] hover:bg-[#ffb300] text-[#0d324d] transition-colors disabled:opacity-70 disabled:cursor-not-allowed uppercase tracking-wide">
                  <span v-if="loading">Logging in...</span>
                  <span v-else>Login</span>
                </button>
              </div>
            </form>
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
import formLogoImg from '@/assets/form_logo.png';

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

const handleLogin = async () => {
  error.value = '';
  loading.value = true;
  try {
    const response = await authService.login(username.value, password.value);
    const userData = response.data.user;
    localStorage.setItem('token', response.data.access);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('is_admin', userData.is_admin ? 'true' : 'false');
    localStorage.setItem('is_superuser', userData.is_superuser ? 'true' : 'false');
    router.push('/Staff/dashboard');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Invalid username or password';
  } finally {
    loading.value = false;
  }
};
</script>
