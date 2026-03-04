<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-[#103059]">Staff Directory</h1>
      <p class="text-slate-500 text-sm mt-1">View information about other staff members in your department.</p>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-24">
      <div class="w-10 h-10 border-4 border-[#103059] border-t-transparent rounded-full animate-spin"></div>
    </div>

    <div v-else-if="staffList.length === 0" class="text-center py-24 text-slate-400">
      <svg class="w-14 h-14 mx-auto mb-4 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
      </svg>
      <p class="font-medium">No staff members found.</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="staff in staffList"
        :key="staff.id"
        class="bg-white rounded-xl shadow-sm border border-slate-100 p-5 flex items-start gap-4 hover:shadow-md transition-shadow"
      >
        <div class="w-12 h-12 rounded-full bg-[#103059] text-white flex items-center justify-center text-lg font-bold shrink-0">
          {{ initials(staff.full_name) }}
        </div>
        <div class="min-w-0">
          <p class="font-semibold text-slate-800 truncate">{{ staff.full_name || staff.username }}</p>
          <p class="text-xs text-slate-400 truncate">{{ staff.department || 'No Department' }}</p>
          <p class="text-xs text-slate-500 mt-1">{{ staff.email || '—' }}</p>
          <span
            :class="staff.is_active
              ? 'bg-green-100 text-green-700'
              : 'bg-red-100 text-red-500'"
            class="mt-2 inline-block text-[0.65rem] font-bold px-2 py-0.5 rounded-full uppercase"
          >
            {{ staff.is_active ? 'Active' : 'Inactive' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { adminService } from '@/services/api';

const staffList = ref([]);
const loading = ref(false);

const initials = (name) => {
  if (!name) return '?';
  return name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();
};

onMounted(async () => {
  loading.value = true;
  try {
    const res = await adminService.getStaffList();
    staffList.value = res.data;
  } catch (err) {
    console.error('Error loading staff directory:', err);
  } finally {
    loading.value = false;
  }
});
</script>
