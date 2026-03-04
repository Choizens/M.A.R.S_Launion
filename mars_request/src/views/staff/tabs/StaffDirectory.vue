<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex flex-col gap-1">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Student Directory</h1>
        <p class="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
          <div class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
          Master Database - {{ students.length }} Records
        </p>
      </div>
      
      <div class="flex flex-col sm:flex-row gap-3">
        <div class="relative">
          <input 
            v-model="studentSearch" 
            @input="onSearch"
            type="text" 
            placeholder="Search LRN or name..." 
            class="w-full sm:w-64 py-2.5 px-4 bg-white border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#00334d]/10 focus:border-[#00334d] outline-none font-medium shadow-sm" 
          />
          <SearchIcon class="absolute right-3 top-2.5 w-4 h-4 text-slate-400" />
        </div>
        <button class="px-6 py-2.5 bg-[#00334d] text-white font-black text-xs uppercase tracking-widest rounded-lg hover:bg-[#004d66] transition-all shadow-md active:scale-95">
          + Add Student
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="std in students" :key="std.id" 
           class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all group relative overflow-hidden">
        <!-- Decorative pattern -->
        <div class="absolute -top-6 -right-6 w-24 h-24 bg-slate-50 rounded-full opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
        
        <div class="flex items-center gap-4 mb-6 relative">
          <div class="w-14 h-14 rounded-xl bg-slate-100 flex items-center justify-center font-black text-slate-400 text-xl border-2 border-white shadow-sm">
            {{ initials(std.first_name, std.last_name) }}
          </div>
          <div class="flex flex-col">
            <span class="text-xs font-black text-[#00334d] uppercase tracking-tighter opacity-50">LRN: {{ std.lrn_number }}</span>
            <h3 class="font-black text-slate-800 tracking-tight">{{ std.first_name }} {{ std.last_name }}</h3>
          </div>
        </div>

        <div class="space-y-3 mb-6 relative">
          <div class="flex justify-between items-center text-[0.7rem] font-bold">
            <span class="text-slate-400 uppercase tracking-widest">Strand</span>
            <span class="text-slate-700">{{ std.strand_display || std.strand || 'N/A' }}</span>
          </div>
          <div class="flex justify-between items-center text-[0.7rem] font-bold">
            <span class="text-slate-400 uppercase tracking-widest">Digitized Docs</span>
            <span class="px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full border border-blue-100">{{ std.documents?.length || 0 }} Files</span>
          </div>
        </div>

        <button class="w-full py-3 bg-slate-50 border border-slate-100 text-[#00334d] font-black text-[0.65rem] uppercase tracking-[0.2em] rounded-xl hover:bg-[#ffca28] hover:border-[#ffca28] transition-all group-hover:shadow-lg">
          Open Master Record
        </button>
      </div>

      <!-- Empty State -->
      <div v-if="students.length === 0 && !loading" class="col-span-full py-20 bg-white rounded-2xl border-2 border-dashed border-slate-200 text-center">
        <SearchIcon class="w-12 h-12 text-slate-200 mx-auto mb-4" />
        <p class="text-slate-400 font-bold uppercase tracking-widest text-xs">No matching students found in directory</p>
      </div>
      
      <div v-if="loading" class="col-span-full py-20 text-center">
         <div class="animate-spin rounded-full h-10 w-10 border-4 border-[#00334d] border-t-transparent mx-auto"></div>
         <p class="mt-4 text-[0.65rem] font-black text-slate-400 uppercase tracking-widest">Accessing Student Vault...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { adminService } from '@/services/api';
import { Search as SearchIcon } from 'lucide-vue-next';

const students = ref([]);
const loading = ref(false);
const studentSearch = ref('');

async function loadStudents() {
  loading.value = true;
  try {
    const res = await adminService.getStudents({ search: studentSearch.value });
    students.value = res.data;
  } catch (err) {
    console.error('Failed to load students');
  } finally {
    loading.value = false;
  }
}

let searchTimeout = null;
const onSearch = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(loadStudents, 350);
};

const initials = (f, l) => {
  if (!f) return '?';
  return `${f[0]}${l?.[0] || l?.[l.length-1] || ''}`.toUpperCase();
};

onMounted(loadStudents);
</script>
