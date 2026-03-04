<template>
  <div class="flex flex-col gap-8">
    <!-- Page Header & Search -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex items-center gap-4">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Record Requests</h1>
        <button @click="exportCSV" class="px-4 py-2 bg-emerald-100 text-emerald-700 hover:bg-emerald-200 border border-emerald-200 rounded text-sm font-bold flex items-center gap-2 transition-colors">
          <DownloadIcon class="w-4 h-4" /> Export CSV
        </button>
      </div>
      <div class="flex flex-col sm:flex-row gap-2">
        <div class="relative w-full sm:w-auto">
          <input 
            type="text" 
            placeholder="Search Passkey, name, email or LRN..." 
            v-model="searchQuery"
            @input="onSearch"
            class="w-full sm:w-[280px] py-2.5 px-4 pr-10 bg-white border border-[#e2e8f0] rounded text-[0.95rem] focus:outline-none focus:ring-2 focus:ring-[#103059]/10 focus:border-[#103059] transition-all"
          />
          <SearchIcon class="absolute right-3 top-2.5 w-5 h-5 text-slate-400" />
        </div>
        
        <select v-model="strandFilter" @change="loadRequests" class="py-2.5 px-4 bg-white border border-[#e2e8f0] rounded text-[0.85rem] font-bold text-[#103059] outline-none">
          <option value="">All Strands</option>
          <option v-for="s in strands" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>

        <select v-model="yearFilter" @change="loadRequests" class="py-2.5 px-4 bg-white border border-[#e2e8f0] rounded text-[0.85rem] font-bold text-[#103059] outline-none">
          <option value="">All Years</option>
          <option v-for="y in Array.from({length: 11}, (_, i) => 2020 + i)" :key="y" :value="y">{{ y }}</option>
        </select>
      </div>
    </div>

    <!-- Filters Bar -->
    <div class="flex flex-wrap items-center gap-3">
      <button 
        v-for="s in statusFilters" 
        :key="s.value"
        @click="setFilter(s.value)"
        :class="[
          'px-6 py-2 rounded font-bold text-sm transition-all border shadow-sm',
          statusFilter === s.value 
            ? 'bg-[#103059] text-white border-[#103059]' 
            : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300'
        ]"
      >
        {{ s.label }}
      </button>
    </div>

    <!-- Table Content -->
    <div class="bg-white rounded-lg shadow-sm border border-[#e2e8f0] flex flex-col overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b-2 border-[#333]">
              <th @click="sortBy('submitted_at')" class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200 cursor-pointer hover:bg-slate-100 select-none">Date <span v-if="sortKey==='submitted_at'">{{ sortAsc ? '↑' : '↓' }}</span></th>
              <th @click="sortBy('passkey')" class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200 cursor-pointer hover:bg-slate-100 select-none">Passkey <span v-if="sortKey==='passkey'">{{ sortAsc ? '↑' : '↓' }}</span></th>
              <th @click="sortBy('first_name')" class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200 min-w-[200px] cursor-pointer hover:bg-slate-100 select-none">Student Name <span v-if="sortKey==='first_name'">{{ sortAsc ? '↑' : '↓' }}</span></th>
              <th @click="sortBy('strand')" class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200 cursor-pointer hover:bg-slate-100 select-none">Strand <span v-if="sortKey==='strand'">{{ sortAsc ? '↑' : '↓' }}</span></th>
              <th @click="sortBy('sex')" class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200 cursor-pointer hover:bg-slate-100 select-none">SEX <span v-if="sortKey==='sex'">{{ sortAsc ? '↑' : '↓' }}</span></th>
              <th @click="sortBy('status')" class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200 cursor-pointer hover:bg-slate-100 select-none">Status <span v-if="sortKey==='status'">{{ sortAsc ? '↑' : '↓' }}</span></th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest text-center">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200">
            <!-- Skeleton Loading -->
            <template v-if="loading">
               <tr v-for="i in 5" :key="'skel'+i">
                  <td class="px-6 py-5 border-r border-slate-100"><div class="h-4 bg-slate-200 rounded w-24 animate-pulse"></div></td>
                  <td class="px-6 py-5 border-r border-slate-100"><div class="h-6 bg-slate-200 rounded w-16 animate-pulse"></div></td>
                  <td class="px-6 py-5 border-r border-slate-100">
                     <div class="flex items-center gap-3">
                        <div class="h-4 bg-slate-200 rounded w-32 animate-pulse"></div>
                     </div>
                  </td>
                  <td class="px-6 py-5 border-r border-slate-100"><div class="h-4 bg-slate-200 rounded w-16 animate-pulse"></div></td>
                  <td class="px-6 py-5 border-r border-slate-100"><div class="h-4 bg-slate-200 rounded w-12 animate-pulse"></div></td>
                  <td class="px-6 py-5 border-r border-slate-100 flex justify-center"><div class="h-6 bg-slate-200 rounded-full w-20 animate-pulse mt-2"></div></td>
                  <td class="px-6 py-5 border-slate-100"><div class="h-8 mx-auto bg-slate-200 rounded w-20 animate-pulse"></div></td>
               </tr>
            </template>

            <tr v-else-if="paginatedRequests.length === 0" class="text-center">
              <td colspan="7" class="py-20 text-slate-400 italic">No records found.</td>
            </tr>

            <!-- Actual Data -->
            <template v-else>
              <tr v-for="req in paginatedRequests" :key="req.id" class="hover:bg-slate-50 transition-colors">
                <td class="px-6 py-5 text-[0.85rem] font-medium text-slate-500 border-r border-slate-100 italic">{{ formatDate(req.submitted_at) }}</td>
                <td class="px-6 py-5 border-r border-slate-100">
                  <span class="px-2 py-1 bg-slate-100 text-[0.8rem] font-black text-[#103059] rounded uppercase tracking-wide font-mono">{{ req.passkey || '—' }}</span>
                </td>
                <td class="px-6 py-5 border-r border-slate-100">
                  <div class="flex items-center gap-2">
                    <span class="text-[0.95rem] font-bold text-[#103059]">{{ req.first_name }} {{ req.last_name }}</span>
                    <AttachmentIcon v-if="req.documents?.length > 0" class="w-3.5 h-3.5 text-amber-500" />
                  </div>
                </td>
                <td class="px-6 py-5 border-r border-slate-100">
                  <span class="text-[0.8rem] font-semibold text-slate-600">{{ req.strand_display || req.strand || '—' }}</span>
                </td>
                <td class="px-6 py-5 border-r border-slate-100">
                  <span class="text-[0.8rem] font-semibold text-slate-600 capitalize">{{ req.sex || '—' }}</span>
                </td>
                <td class="px-6 py-5 border-r border-slate-100 text-center">
                  <span class="px-3 py-1 rounded-full text-[0.65rem] font-black uppercase tracking-wider" :class="statusClass(req.status)">
                    {{ req.status }}
                  </span>
                </td>
                <td class="px-6 py-5 text-center">
                  <button @click="$emit('open-request', req)" class="px-8 py-2 bg-[#ffde59] border-2 border-[#333] rounded font-bold text-sm text-[#333] hover:bg-white transition-all shadow-sm uppercase tracking-wide">
                    Details
                  </button>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination Controls -->
      <div v-if="!loading && sortedRequests.length > 0" class="p-4 border-t flex flex-col sm:flex-row items-center justify-between text-sm bg-slate-50">
        <span class="text-slate-500 font-medium">Showing {{ ((currentPage - 1) * itemsPerPage) + 1 }} to {{ Math.min(currentPage * itemsPerPage, sortedRequests.length) }} of {{ sortedRequests.length }} entries</span>
        <div class="flex gap-2 mt-4 sm:mt-0">
          <button @click="currentPage--" :disabled="currentPage === 1" class="px-4 py-1.5 rounded border bg-white text-slate-700 hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed font-bold">Prev</button>
          <button @click="currentPage++" :disabled="currentPage >= totalPages" class="px-4 py-1.5 rounded border bg-white text-slate-700 hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed font-bold">Next</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { adminService } from '@/services/api';
import { Search as SearchIcon, Paperclip as AttachmentIcon, Download as DownloadIcon } from 'lucide-vue-next';

// Data
const requests = ref([]);
const strands = ref([]);
const loading = ref(false);

// Filters
const searchQuery = ref('');
const statusFilter = ref('');
const strandFilter = ref('');
const yearFilter = ref('');

// Sorting
const sortKey = ref('submitted_at');
const sortAsc = ref(false);

// Pagination
const currentPage = ref(1);
const itemsPerPage = 10;

const statusFilters = [
  { label: 'All', value: '' },
  { label: 'Pending', value: 'Pending' },
  { label: 'Approved', value: 'Approved' },
  { label: 'Completed', value: 'Completed' },
];

const loadRequests = async () => {
  loading.value = true;
  currentPage.value = 1; // reset page on load
  try {
    const params = {};
    if (statusFilter.value) params.status = statusFilter.value;
    if (searchQuery.value.trim()) params.search = searchQuery.value.trim();
    if (strandFilter.value) params.strand = strandFilter.value;
    if (yearFilter.value) params.year = yearFilter.value;
    const res = await adminService.getRequests(params);
    requests.value = res.data;
  } catch (err) { console.error('Requests error:', err); }
  finally { loading.value = false; }
};

const loadStrands = async () => {
  try {
    const res = await adminService.getStrands();
    strands.value = res.data;
  } catch (err) { console.error('Strands error:', err); }
};

let searchTimeout = null;
const onSearch = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(loadRequests, 350);
};

const setFilter = (val) => {
  statusFilter.value = val;
  loadRequests();
};

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value;
  } else {
    sortKey.value = key;
    sortAsc.value = true;
  }
  currentPage.value = 1; // reset page on sort
};

// Computed Properties for Sorting & Pagination
const sortedRequests = computed(() => {
  return [...requests.value].sort((a, b) => {
    let valA = a[sortKey.value] || '';
    let valB = b[sortKey.value] || '';
    if (typeof valA === 'string') valA = valA.toLowerCase();
    if (typeof valB === 'string') valB = valB.toLowerCase();
    
    if (valA < valB) return sortAsc.value ? -1 : 1;
    if (valA > valB) return sortAsc.value ? 1 : -1;
    return 0;
  });
});

const totalPages = computed(() => {
  if (sortedRequests.value.length === 0) return 1;
  return Math.ceil(sortedRequests.value.length / itemsPerPage);
});

const paginatedRequests = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return sortedRequests.value.slice(start, start + itemsPerPage);
});

// CSV Export
const exportCSV = () => {
  if (sortedRequests.value.length === 0) return;
  
  const headers = ['Date Requested', 'Passkey', 'Student Name', 'Strand', 'Sex', 'LRN', 'Email', 'Phone', 'Status'];
  const rows = sortedRequests.value.map(r => [
    formatDate(r.submitted_at),
    r.passkey || '',
    `${r.first_name} ${r.last_name}`,
    r.strand_display || r.strand || '',
    r.sex || '',
    r.lrn_number || '',
    r.email || '',
    r.phone_number || '',
    r.status || ''
  ]);
  
  const csvContent = "data:text/csv;charset=utf-8," 
    + [headers.join(","), ...rows.map(e => `"${e.join('","')}"`)].join("\n");
    
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `staff_requests_export_${new Date().toISOString().slice(0,10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const formatDate = (dt) => dt ? new Date(dt).toLocaleDateString('en-PH', { year: 'numeric', month: 'short', day: 'numeric' }) : '—';
const statusClass = (s) => ({
  'bg-amber-100 text-amber-600 border border-amber-200': s === 'Pending',
  'bg-orange-100 text-orange-600 border border-orange-200': s === 'Needs Verification',
  'bg-green-100 text-green-600 border border-green-200': s === 'Approved',
  'bg-purple-100 text-purple-600 border border-purple-200': s === 'Completed',
  'bg-red-100 text-red-600 border border-red-200': s === 'Rejected',
});

onMounted(() => {
  loadRequests();
  loadStrands();
});

// Expose refresh function to parent
defineExpose({ refresh: loadRequests });
</script>
