<template>
  <div class="flex flex-col gap-6">
    <!-- Header & Search -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex flex-col gap-2">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Record Requests</h1>
        <p class="text-slate-500 text-sm">Manage and track student record applications.</p>
      </div>

      <!-- Bulk Actions Bar -->
      <div v-if="selectedRequests.length > 0" class="flex items-center gap-3 bg-blue-50 border border-blue-200 px-4 py-2 rounded-lg shadow-sm animate-in fade-in slide-in-from-top-2">
        <span class="text-sm font-bold text-blue-800">{{ selectedRequests.length }} selected</span>
        <button @click="$emit('bulk-action', { action: 'Approve', ids: selectedRequests })" class="px-4 py-1.5 bg-green-600 text-white text-xs font-bold rounded hover:bg-green-700 transition-colors shadow-sm">
          Approve All
        </button>
        <button @click="$emit('bulk-action', { action: 'Rejected', ids: selectedRequests })" class="px-4 py-1.5 bg-red-600 text-white text-xs font-bold rounded hover:bg-red-700 transition-colors shadow-sm">
          Reject All
        </button>
        <button @click="selectedRequests = []" class="px-2 py-1.5 text-slate-500 hover:text-slate-700 flex items-center">
          <XIcon class="w-4 h-4" />
        </button>
      </div>
    </div>
    <div class="flex flex-col sm:flex-row gap-2 mt-4">
      <div class="relative w-full sm:w-auto">
        <input 
          type="text" 
          placeholder="Search Passkey, name, email or LRN..." 
          :value="searchQuery"
          @input="$emit('update:searchQuery', $event.target.value)"
          class="w-full sm:w-[280px] py-2.5 px-4 pr-10 bg-white border border-[#e2e8f0] rounded text-[0.95rem] focus:outline-none focus:border-[#103059] transition-all"
        />
        <SearchIcon class="absolute right-3 top-2.5 w-5 h-5 text-slate-400" />
      </div>
      
      <select :value="strandFilter" @change="$emit('update:strandFilter', $event.target.value)" class="py-2.5 px-4 bg-white border border-[#e2e8f0] rounded text-[0.85rem] font-bold text-[#103059] outline-none">
        <option value="">All Strands</option>
        <option v-for="s in strands" :key="s.id" :value="s.id">{{ s.name }}</option>
      </select>

      <select :value="yearFilter" @change="$emit('update:yearFilter', $event.target.value)" class="py-2.5 px-4 bg-white border border-[#e2e8f0] rounded text-[0.85rem] font-bold text-[#103059] outline-none">
        <option value="">All Years</option>
        <option v-for="y in Array.from({length: 11}, (_, i) => 2020 + i)" :key="y" :value="y">{{ y }}</option>
      </select>

      <button @click="$emit('refresh')" class="w-full sm:w-auto px-6 py-2.5 border-2 border-[#1e293b] text-[#1e293b] font-bold rounded hover:bg-[#1e293b] hover:text-white transition-all duration-200 shadow-sm">
        Apply
      </button>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap items-center gap-3">
      <button 
        v-for="s in statusFilters" 
        :key="s.value"
        @click="$emit('update:statusFilter', s.value)"
        :class="[
          'px-6 py-2 rounded font-bold text-sm transition-all shadow-sm border',
          statusFilter === s.value 
            ? 'bg-[#103059] text-white border-[#103059]' 
            : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300'
        ]"
      >
        {{ s.label }}
        <span v-if="s.value && stats[s.stat] !== undefined" class="ml-2 text-[0.65rem] opacity-70">{{ stats[s.stat] }}</span>
      </button>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-lg shadow-sm border border-[#e2e8f0] overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b-2 border-[#333]">
              <th class="px-4 py-4 w-12 border-r border-slate-200">
                <input type="checkbox" :checked="allSelected" @change="toggleAll" class="w-4 h-4 text-[#103059] rounded border-slate-300 focus:ring-[#103059]" />
              </th>
              <th @click="toggleSort('submitted_at')" class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200 cursor-pointer hover:bg-slate-100 group">
                <div class="flex items-center gap-2">Date <SortIcon class="w-3 h-3 text-slate-400 group-hover:text-slate-800" /></div>
              </th>
              <th @click="toggleSort('name')" class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200 cursor-pointer hover:bg-slate-100 group">
                <div class="flex items-center gap-2">Name <SortIcon class="w-3 h-3 text-slate-400 group-hover:text-slate-800" /></div>
              </th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200">Documents</th>
              <th @click="toggleSort('status')" class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest border-r border-slate-200 cursor-pointer hover:bg-slate-100 group text-center">
                <div class="flex items-center justify-center gap-2">Status <SortIcon class="w-3 h-3 text-slate-400 group-hover:text-slate-800" /></div>
              </th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest text-center">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200">
            <tr v-if="loadingRequests" class="p-20 text-center text-slate-400">
              <td colspan="5" class="py-20 text-center italic">Loading request records...</td>
            </tr>
            <tr v-else-if="requests.length === 0" class="p-20 text-center text-slate-400">
              <td colspan="5" class="py-20 text-center italic">No requests found matching your filters.</td>
            </tr>
            <tr v-for="req in sortedRequests" :key="req.id" class="hover:bg-slate-50 transition-colors" :class="{ 'bg-red-50/30': isStale(req) }">
              <td class="px-4 py-5 border-r border-slate-100 text-center">
                <input type="checkbox" :value="req.id" v-model="selectedRequests" class="w-4 h-4 text-[#103059] rounded border-slate-300 focus:ring-[#103059]" />
              </td>
              <td class="px-6 py-5 text-[0.8rem] font-bold text-slate-500 border-r border-slate-100 whitespace-nowrap">{{ formatDate(req.submitted_at) }}</td>
              <td class="px-6 py-5 border-r border-slate-100">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded bg-slate-100 flex items-center justify-center text-[0.6rem] font-black text-slate-400 border">
                    {{ initials(req.first_name, req.last_name) }}
                  </div>
                  <div class="flex flex-col">
                    <div class="flex items-center gap-2">
                      <span class="px-2 py-0.5 bg-slate-100 text-[0.55rem] font-black text-slate-500 rounded uppercase tracking-tighter">{{ req.passkey }}</span>
                      <span class="text-[0.9rem] font-bold text-[#103059]">{{ req.first_name }} {{ req.last_name }}</span>
                      <component :is="AttachmentIcon" v-if="req.documents?.length > 0" class="w-3.5 h-3.5 text-amber-500" />
                    </div>
                    <span class="text-[0.7rem] text-slate-400 truncate max-w-[150px]">{{ req.email }}</span>
                  </div>
                </div>
              </td>
              <td class="px-6 py-5 border-r border-slate-100">
                <div class="flex flex-wrap gap-1">
                  <span v-for="f in req.requested_files" :key="f" class="text-[0.6rem] font-bold px-2 py-0.5 bg-slate-100 text-slate-600 rounded">
                    {{ f }}
                  </span>
                </div>
              </td>
              <td class="px-6 py-5 border-r border-slate-100 text-center">
                <div class="flex flex-col items-center justify-center gap-1">
                  <span class="px-3 py-1 rounded-full text-[0.65rem] font-black uppercase tracking-wider shadow-sm" :class="statusClass(req.status)">
                    {{ req.status }}
                  </span>
                  <span v-if="isStale(req)" class="text-[0.55rem] font-black text-red-500 bg-red-100 px-2 py-0.5 rounded uppercase tracking-widest flex items-center gap-1">
                    <AlertIcon class="w-3 h-3" /> Stale
                  </span>
                </div>
              </td>
              <td class="px-6 py-5 text-center">
                <button @click="$emit('open-modal', req)" class="px-6 py-1.5 bg-[#ffca28] border-2 border-[#1e293b] rounded font-bold text-xs text-[#103059] hover:bg-white hover:text-[#103059] transition-all shadow-sm uppercase tracking-wide">
                  Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { Search as SearchIcon, Paperclip as AttachmentIcon, X as XIcon, ArrowUpDown as SortIcon, AlertCircle as AlertIcon } from 'lucide-vue-next';

const props = defineProps({
  requests: Array,
  loadingRequests: Boolean,
  searchQuery: String,
  strandFilter: [String, Number],
  yearFilter: [String, Number],
  statusFilter: String,
  strands: Array,
  stats: Object,
  statusFilters: Array,
  formatDate: Function,
  initials: Function,
  statusClass: Function
});

const emit = defineEmits(['update:searchQuery', 'update:strandFilter', 'update:yearFilter', 'update:statusFilter', 'refresh', 'open-modal', 'bulk-action']);

// Bulk Actions
const selectedRequests = ref([]);

const allSelected = computed(() => {
  return props.requests.length > 0 && selectedRequests.value.length === props.requests.length;
});

function toggleAll(e) {
  if (e.target.checked) {
    selectedRequests.value = props.requests.map(r => r.id);
  } else {
    selectedRequests.value = [];
  }
}

// Clear selections when filters change
watch(() => [props.searchQuery, props.strandFilter, props.yearFilter, props.statusFilter], () => {
  selectedRequests.value = [];
});

// Sorting
const sortKey = ref('submitted_at');
const sortDesc = ref(true);

function toggleSort(key) {
  if (sortKey.value === key) {
    sortDesc.value = !sortDesc.value;
  } else {
    sortKey.value = key;
    sortDesc.value = false;
  }
}

const sortedRequests = computed(() => {
  if (!props.requests) return [];
  return [...props.requests].sort((a, b) => {
    let valA = a[sortKey.value];
    let valB = b[sortKey.value];

    // Handle compound sort keys
    if (sortKey.value === 'name') {
      valA = `${a.first_name} ${a.last_name}`.toLowerCase();
      valB = `${b.first_name} ${b.last_name}`.toLowerCase();
    } else if (sortKey.value === 'submitted_at') {
      valA = new Date(a.submitted_at).getTime();
      valB = new Date(b.submitted_at).getTime();
    }

    if (valA < valB) return sortDesc.value ? 1 : -1;
    if (valA > valB) return sortDesc.value ? -1 : 1;
    return 0;
  });
});

// Stale Requests (Pending for > 48 hours)
function isStale(req) {
  if (req.status !== 'Pending') return false;
  const submittedDate = new Date(req.submitted_at);
  const now = new Date();
  const diffHours = (now - submittedDate) / (1000 * 60 * 60);
  return diffHours > 48;
}
</script>
