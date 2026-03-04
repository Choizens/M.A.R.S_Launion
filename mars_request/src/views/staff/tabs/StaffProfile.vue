<template>
  <div class="flex flex-col gap-6">
    <div class="max-w-2xl bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden mx-auto md:mx-0">
       <div class="h-32 bg-[#00334d] flex items-end px-8 pb-4 relative">
        <div class="absolute -bottom-10 left-8 w-24 h-24 bg-white rounded-full p-1 shadow-lg">
          <div class="w-full h-full bg-amber-400 rounded-full flex items-center justify-center text-[#00334d] font-black text-3xl">
            {{ initials(user?.full_name) }}
          </div>
        </div>
      </div>
      <div class="pt-16 pb-12 px-8">
        <div class="flex flex-col gap-1 mb-10">
          <h2 class="text-2xl font-black text-[#00334d]">{{ user?.full_name || 'Staff Member' }}</h2>
          <span class="text-amber-600 font-bold uppercase tracking-widest text-xs">{{ user?.department || 'Administration' }}</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="flex flex-col gap-1.5">
            <span class="text-[0.65rem] font-bold text-slate-400 uppercase tracking-widest">Username</span>
            <span class="text-sm font-bold text-[#00334d] px-4 py-2 bg-slate-50 rounded">@{{ user?.username }}</span>
          </div>
          <div class="flex flex-col gap-1.5">
            <span class="text-[0.65rem] font-bold text-slate-400 uppercase tracking-widest">Staff ID</span>
            <span class="text-sm font-bold text-[#00334d] px-4 py-2 bg-slate-50 rounded">{{ user?.staff_id }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const user = ref(null);

const initials = (name) => {
  if (!name) return '?';
  const parts = name.split(' ');
  const f = parts[0];
  const l = parts[parts.length - 1];
  return `${f[0]}${l?.[0] || ''}`.toUpperCase();
};

onMounted(() => {
  const storedUser = localStorage.getItem('user');
  if (storedUser) user.value = JSON.parse(storedUser);
});
</script>
