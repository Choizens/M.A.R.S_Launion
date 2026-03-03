<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-[#00334d]">My Profile</h1>
      <p class="text-slate-500 text-sm mt-1">Your account information and details.</p>
    </div>

    <div class="max-w-xl bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
      <!-- Profile Header -->
      <div class="bg-gradient-to-r from-[#004d66] to-[#006b8f] px-8 py-10 flex items-center gap-6">
        <div class="w-20 h-20 rounded-full bg-white/20 border-4 border-white/50 flex items-center justify-center text-white text-3xl font-black">
          {{ initials }}
        </div>
        <div>
          <h2 class="text-xl font-bold text-white">{{ user?.full_name || user?.username || 'Staff Member' }}</h2>
          <p class="text-sm text-white/70 mt-0.5">{{ user?.department || 'No Department Assigned' }}</p>
          <span class="mt-2 inline-block bg-amber-400 text-[#0d324d] text-[0.65rem] font-bold px-2 py-0.5 rounded-full uppercase">Staff</span>
        </div>
      </div>

      <!-- Profile Details -->
      <div class="px-8 py-6 space-y-5">
        <div class="flex flex-col gap-1">
          <span class="text-[0.7rem] font-bold text-slate-400 uppercase tracking-wider">Username</span>
          <span class="text-slate-700 font-medium">{{ user?.username || '—' }}</span>
        </div>
        <div class="h-px bg-slate-100"></div>
        <div class="flex flex-col gap-1">
          <span class="text-[0.7rem] font-bold text-slate-400 uppercase tracking-wider">Full Name</span>
          <span class="text-slate-700 font-medium">{{ user?.full_name || '—' }}</span>
        </div>
        <div class="h-px bg-slate-100"></div>
        <div class="flex flex-col gap-1">
          <span class="text-[0.7rem] font-bold text-slate-400 uppercase tracking-wider">Email</span>
          <span class="text-slate-700 font-medium">{{ user?.email || '—' }}</span>
        </div>
        <div class="h-px bg-slate-100"></div>
        <div class="flex flex-col gap-1">
          <span class="text-[0.7rem] font-bold text-slate-400 uppercase tracking-wider">Staff ID</span>
          <span class="text-slate-700 font-medium">{{ user?.staff_id || '—' }}</span>
        </div>
        <div class="h-px bg-slate-100"></div>
        <div class="flex flex-col gap-1">
          <span class="text-[0.7rem] font-bold text-slate-400 uppercase tracking-wider">Department</span>
          <span class="text-slate-700 font-medium">{{ user?.department || '—' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const user = ref(null);

const initials = computed(() => {
  const name = user.value?.full_name || user.value?.username || '';
  return name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase() || '?';
});

onMounted(() => {
  const stored = localStorage.getItem('user');
  if (stored) {
    user.value = JSON.parse(stored);
  }
});
</script>
