<template>
  <div class="flex flex-col gap-6">
    <!-- Header & Filters -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex flex-col gap-1">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#103059] tracking-tight">Staff Directory</h1>
        <p class="text-slate-500 text-sm">View information about other staff members.</p>
      </div>

      <div class="flex flex-col sm:flex-row gap-2">
        <div class="relative">
          <input 
            type="text" 
            placeholder="Search name or email..." 
            v-model="searchQuery"
            class="w-full sm:w-[250px] py-2.5 px-4 bg-white border border-[#e2e8f0] rounded text-[0.95rem] focus:outline-none focus:ring-2 focus:ring-[#103059]/10 focus:border-[#103059] transition-all"
          />
        </div>
        
        <select v-model="departmentFilter" class="py-2.5 px-4 bg-white border border-[#e2e8f0] rounded text-[0.85rem] font-bold text-[#103059] outline-none">
          <option value="">All Departments</option>
          <option v-for="dept in uniqueDepartments" :key="dept" :value="dept">{{ dept }}</option>
        </select>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-24">
      <div class="w-10 h-10 border-4 border-[#103059] border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredStaff.length === 0" class="text-center py-24 text-slate-400 bg-white rounded-xl border border-dashed border-slate-300">
      <svg class="w-14 h-14 mx-auto mb-4 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
      </svg>
      <p class="font-bold uppercase tracking-widest text-xs">No matching staff found</p>
    </div>

    <!-- Staff Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="staff in filteredStaff"
        :key="staff.id"
        class="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-start gap-4 hover:shadow-md hover:border-[#103059]/30 transition-all group"
      >
        <div class="w-14 h-14 rounded-full bg-[#103059] text-white flex items-center justify-center text-xl font-black shrink-0 border-4 border-slate-50 group-hover:bg-amber-400 group-hover:text-[#103059] transition-colors">
          {{ initials(staff.full_name || staff.username) }}
        </div>
        <div class="min-w-0 flex-1">
          <p class="font-black text-[#103059] truncate text-lg leading-tight">{{ staff.full_name || staff.username }}</p>
          <div class="flex items-center gap-1.5 mt-1">
            <span class="text-[0.6rem] font-black uppercase bg-slate-100 text-slate-500 px-2 py-0.5 rounded tracking-wider">{{ staff.department || 'General' }}</span>
          </div>
          <p class="text-xs text-slate-500 mt-2 flex items-center gap-1.5 truncate">
             <span class="opacity-50 font-medium">@</span>{{ staff.email || 'No email' }}
          </p>
          <div class="flex items-center gap-2 mt-4">
            <span
              :class="staff.is_active
                ? 'bg-emerald-50 text-emerald-600 border-emerald-100'
                : 'bg-rose-50 text-rose-500 border-rose-100'"
              class="text-[0.6rem] font-black px-2.5 py-1 rounded-full uppercase tracking-widest border"
            >
              {{ staff.is_active ? 'Active' : 'Inactive' }}
            </span>
            <span v-if="staff.is_superuser" class="bg-amber-50 text-amber-600 border border-amber-100 text-[0.6rem] font-black px-2.5 py-1 rounded-full uppercase tracking-widest">
              Admin
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { adminService } from '@/services/api';

const staffList = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const departmentFilter = ref('');

const initials = (name) => {
  if (!name) return '?';
  const parts = name.split(' ');
  if (parts.length >= 2) return (parts[0][0] + parts[parts.length-1][0]).toUpperCase();
  return name[0].toUpperCase();
};

const uniqueDepartments = computed(() => {
  const depts = staffList.value
    .map(s => s.department)
    .filter(d => d && d.trim() !== '');
  return [...new Set(depts)].sort();
});

const filteredStaff = computed(() => {
  return staffList.value.filter(s => {
    const matchesSearch = !searchQuery.value || 
      (s.full_name || '').toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (s.username || '').toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (s.email || '').toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesDept = !departmentFilter.value || s.department === departmentFilter.value;
    
    return matchesSearch && matchesDept;
  });
});

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
