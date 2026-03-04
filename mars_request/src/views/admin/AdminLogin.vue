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
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.admin-login-root {
  min-height: 100vh;
  background: #0a0f1a;
  font-family: 'Poppins', sans-serif;
  display: flex;
  align-items: stretch;
  position: relative;
  overflow: hidden;
}

/* Ambient orbs */
.orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.18;
  pointer-events: none;
  z-index: 0;
}
.orb-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, #0ea5e9, transparent);
  top: -120px; left: -120px;
  animation: floatOrb 12s ease-in-out infinite;
}
.orb-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, #6366f1, transparent);
  bottom: -100px; right: 10%;
  animation: floatOrb 16s ease-in-out infinite reverse;
}
.orb-3 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, #f59e0b, transparent);
  top: 50%; right: 30%;
  animation: floatOrb 10s ease-in-out infinite 4s;
}
@keyframes floatOrb {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-30px) scale(1.05); }
}

/* Layout */
.login-wrapper {
  display: flex;
  width: 100%;
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

/* Left Panel */
.left-panel {
  flex: 1.1;
  background: linear-gradient(145deg, #0d1b2e 0%, #0a1628 50%, #050d1a 100%);
  border-right: 1px solid rgba(255,255,255,0.06);
  display: flex;
  flex-direction: column;
  padding: 40px 56px;
  position: relative;
  overflow: hidden;
}

.left-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  position: relative;
  z-index: 1;
}
.brand-logo {
  width: 44px;
  height: 44px;
  object-fit: contain;
  filter: drop-shadow(0 0 12px rgba(14, 165, 233, 0.4));
}
.brand-text {
  display: flex;
  flex-direction: column;
}
.brand-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #e2e8f0;
  letter-spacing: 0.02em;
}
.brand-sub {
  font-size: 0.72rem;
  color: #64748b;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.hero-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  z-index: 1;
  padding: 40px 0;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(14, 165, 233, 0.1);
  border: 1px solid rgba(14, 165, 233, 0.25);
  color: #38bdf8;
  padding: 6px 14px;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  width: fit-content;
  margin-bottom: 24px;
}
.hero-badge span {
  color: #22c55e;
  font-size: 0.5rem;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.hero-title {
  font-size: 4rem;
  font-weight: 900;
  color: #f1f5f9;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
}
.hero-title-accent {
  display: block;
  background: linear-gradient(135deg, #0ea5e9, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.7;
  max-width: 380px;
  margin-bottom: 48px;
}

.hero-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 14px 18px;
  transition: all 0.2s;
}
.stat-card:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(14, 165, 233, 0.2);
}
.stat-icon { font-size: 1.1rem; }
.stat-label {
  font-size: 0.85rem;
  font-weight: 500;
  color: #94a3b8;
}

.panel-footer {
  font-size: 0.72rem;
  color: #334155;
  position: relative;
  z-index: 1;
}

/* Right Panel */
.right-panel {
  flex: 0 0 480px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 48px;
  background: #050d1a;
}

.login-card {
  width: 100%;
  max-width: 380px;
}

.card-header {
  text-align: center;
  margin-bottom: 36px;
}
.admin-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, rgba(14,165,233,0.15), rgba(99,102,241,0.15));
  border: 1px solid rgba(14,165,233,0.25);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: #38bdf8;
}
.card-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: #f1f5f9;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}
.card-subtitle {
  font-size: 0.85rem;
  color: #475569;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.form-group label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #94a3b8;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.input-icon {
  position: absolute;
  left: 14px;
  color: #475569;
  pointer-events: none;
}
.input-wrapper input {
  width: 100%;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 13px 44px;
  color: #f1f5f9;
  font-size: 0.9rem;
  font-family: 'Poppins', sans-serif;
  transition: all 0.2s;
  outline: none;
}
.input-wrapper input::placeholder {
  color: #334155;
}
.input-wrapper input:focus {
  border-color: #0ea5e9;
  background: rgba(14, 165, 233, 0.05);
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
}
.form-group.has-error .input-wrapper input {
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.05);
}
.toggle-password {
  position: absolute;
  right: 14px;
  background: none;
  border: none;
  cursor: pointer;
  color: #475569;
  padding: 4px;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}
.toggle-password:hover { color: #94a3b8; }
.field-error {
  font-size: 0.78rem;
  color: #f87171;
}

/* Error Alert */
.error-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-radius: 10px;
  padding: 12px 14px;
  color: #f87171;
  font-size: 0.85rem;
  animation: slideIn 0.2s ease;
}
@keyframes slideIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Login Button */
.login-btn {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #0ea5e9, #6366f1);
  color: white;
  font-family: 'Poppins', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 24px rgba(14, 165, 233, 0.25);
  margin-top: 4px;
}
.login-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 32px rgba(14, 165, 233, 0.4);
  background: linear-gradient(135deg, #38bdf8, #818cf8);
}
.login-btn:active:not(:disabled) { transform: translateY(0); }
.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Card Footer */
.card-footer {
  margin-top: 28px;
  text-align: center;
}
.staff-link {
  font-size: 0.82rem;
  color: #475569;
  text-decoration: none;
  transition: color 0.2s;
}
.staff-link:hover { color: #38bdf8; }

/* Responsive */
@media (max-width: 900px) {
  .left-panel { display: none; }
  .right-panel {
    flex: 1;
    padding: 32px 24px;
    background: #0a0f1a;
  }
}
</style>
