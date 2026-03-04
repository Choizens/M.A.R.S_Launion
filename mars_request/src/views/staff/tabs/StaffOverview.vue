<template>
  <div class="flex flex-col gap-10">
    <div class="flex flex-col gap-2">
      <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Staff Dashboard</h1>
      <p class="text-slate-500 text-sm">System snapshot and recent activity overview.</p>
    </div>

    <!-- Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
      <div v-for="(card, i) in statCards" :key="card.label || i" 
           class="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex flex-col gap-4 hover:shadow-md transition-shadow relative overflow-hidden">
        
        <!-- Skeleton for Card -->
        <template v-if="loading">
          <div class="w-10 h-10 rounded-lg bg-slate-200 animate-pulse"></div>
          <div class="flex flex-col gap-2 mt-1">
            <div class="h-3 w-16 bg-slate-200 rounded animate-pulse"></div>
            <div class="h-8 w-12 bg-slate-200 rounded animate-pulse"></div>
          </div>
        </template>
        
        <!-- Actual Card -->
        <template v-else>
          <div class="w-10 h-10 rounded-lg flex items-center justify-center text-white" :style="{ backgroundColor: card.color }">
            <component :is="card.icon" class="w-6 h-6" />
          </div>
          <div class="flex flex-col">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-widest">{{ card.label }}</span>
            <span class="text-3xl font-black text-[#103059]">{{ card.value }}</span>
          </div>
        </template>
      </div>
    </div>

    <!-- Dashboard Content Rows -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Strand Distribution -->
      <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
        <div class="px-6 py-4 bg-slate-50 border-b">
          <h3 class="font-bold text-[#103059] text-sm uppercase tracking-wide">Requests by Strand</h3>
        </div>
        <div class="p-6">
          <div v-if="loading" class="space-y-5">
            <div v-for="i in 4" :key="i" class="flex flex-col gap-2">
              <div class="flex justify-between">
                <div class="h-3 w-24 bg-slate-200 rounded animate-pulse"></div>
                <div class="h-3 w-6 bg-slate-200 rounded animate-pulse"></div>
              </div>
              <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-slate-200 animate-pulse w-full"></div>
              </div>
            </div>
          </div>
          <div v-else class="space-y-4">
            <div v-for="row in stats.strand_breakdown" :key="row.strand_name" class="flex flex-col gap-1.5">
              <div class="flex justify-between text-xs font-bold">
                <span class="text-slate-700">{{ row.strand_name }}</span>
                <span class="text-slate-500">{{ row.count }}</span>
              </div>
              <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-amber-400" :style="{ width: strandPercent(row.count) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent High-Priority Requests -->
      <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
        <div class="px-6 py-4 bg-slate-50 border-b">
          <h3 class="font-bold text-[#103059] text-sm uppercase tracking-wide">Recent Submissions</h3>
        </div>
        <div class="divide-y relative min-h-[200px] flex flex-col">
          <template v-if="loading">
            <div v-for="i in 4" :key="i" class="px-6 py-4 flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded bg-slate-200 animate-pulse"></div>
                <div class="flex flex-col gap-2">
                  <div class="h-3 w-32 bg-slate-200 rounded animate-pulse"></div>
                  <div class="h-2 w-20 bg-slate-200 rounded animate-pulse"></div>
                </div>
              </div>
              <div class="h-6 w-16 bg-slate-200 rounded-full animate-pulse"></div>
            </div>
          </template>
          
          <div v-else-if="stats.recent_requests?.length === 0" class="absolute inset-0 flex items-center justify-center text-slate-400 italic text-sm">No recent requests</div>
          
          <template v-else>
            <div v-for="req in stats.recent_requests" :key="req.id" 
                 @click="$emit('open-request', req)"
                 class="px-6 py-4 flex items-center justify-between hover:bg-slate-50 cursor-pointer transition-colors group">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded bg-[#103059] text-white flex items-center justify-center font-bold text-xs uppercase">
                  {{ initials(req.first_name, req.last_name) }}
                </div>
                <div class="flex flex-col">
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-sm text-[#103059] group-hover:text-cyan-600">{{ req.first_name }} {{ req.last_name }}</span>
                    <AttachmentIcon v-if="req.documents?.length > 0" class="w-3.5 h-3.5 text-amber-500" />
                  </div>
                  <span class="text-[0.7rem] text-slate-500 font-medium">{{ formatDate(req.submitted_at) }}</span>
                </div>
              </div>
              <span class="px-3 py-1 rounded-full text-[0.6rem] font-black uppercase" :class="statusClass(req.status)">
                {{ req.status }}
              </span>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, markRaw } from 'vue';
import { adminService } from '@/services/api';
import { 
  FileText as FileIcon, Clock as ClockIcon, CheckCircle as CheckIcon,
  AlertCircle as AlertIcon, Paperclip as AttachmentIcon
} from 'lucide-vue-next';

const stats = ref({
  total: 0, pending: 0, needs_verification: 0, approved: 0, completed: 0, rejected: 0,
  strand_breakdown: [], recent_requests: []
});
const loading = ref(false);

const statCards = computed(() => [
  { label: 'Total', value: stats.value.total ?? 0, color: '#103059', icon: markRaw(FileIcon) },
  { label: 'Pending', value: stats.value.pending ?? 0, color: '#f59e0b', icon: markRaw(ClockIcon) },
  { label: 'Missing Record', value: stats.value.needs_verification ?? 0, color: '#f97316', icon: markRaw(AlertIcon) },
  { label: 'Approved', value: stats.value.approved ?? 0, color: '#10b981', icon: markRaw(CheckIcon) },
  { label: 'Completed', value: stats.value.completed ?? 0, color: '#8b5cf6', icon: markRaw(CheckIcon) },
  { label: 'Rejected', value: stats.value.rejected ?? 0, color: '#ef4444', icon: markRaw(AlertIcon) },
]);

const loadStats = async () => {
  loading.value = true;
  try {
    const res = await adminService.getStats();
    stats.value = res.data;
  } catch (err) { console.error('Stats error:', err); }
  finally { loading.value = false; }
};

const initials = (f, l) => {
  if (!f) return '?';
  return `${f[0]}${l?.[0] || ''}`.toUpperCase();
};
const formatDate = (dt) => dt ? new Date(dt).toLocaleDateString('en-PH', { year: 'numeric', month: 'short', day: 'numeric' }) : '—';
const strandPercent = (count) => stats.value.total ? Math.round((count / stats.value.total) * 100) : 0;
const statusClass = (s) => ({
  'bg-amber-100 text-amber-600 border border-amber-200': s === 'Pending',
  'bg-orange-100 text-orange-600 border border-orange-200': s === 'Needs Verification',
  'bg-green-100 text-green-600 border border-green-200': s === 'Approved',
  'bg-purple-100 text-purple-600 border border-purple-200': s === 'Completed',
  'bg-red-100 text-red-600 border border-red-200': s === 'Rejected',
});

onMounted(loadStats);
</script>
