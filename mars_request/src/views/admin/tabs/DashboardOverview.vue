<template>
  <div class="flex flex-col gap-10">
    <div class="flex flex-col gap-2">
      <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Admin Dashboard</h1>
      <p class="text-slate-500 text-sm">Overview of system performance and record requests.</p>
    </div>

    <!-- Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
      <div v-for="card in statCards" :key="card.label" 
           class="bg-white p-6 rounded-lg border border-slate-200 shadow-sm flex flex-col gap-2 relative overflow-hidden group hover:shadow-md transition-shadow">
        <div class="absolute top-0 right-0 w-24 h-24 -mr-8 -mt-8 opacity-5 transition-transform group-hover:scale-110" :style="{ color: card.color }">
          <component :is="card.icon" class="w-full h-full" />
        </div>
        <span class="text-xs font-bold text-slate-500 uppercase tracking-widest">{{ card.label }}</span>
        <div class="flex items-end gap-2">
          <span class="text-3xl font-black text-[#103059]">{{ card.value }}</span>
        </div>
        <div class="w-full h-1 mt-2 rounded-full bg-slate-100 overflow-hidden">
          <div class="h-full rounded-full transition-all duration-1000" :style="{ width: '100%', backgroundColor: card.color }"></div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-4">
      <!-- Monthly Trend Line Chart -->
      <div class="bg-white rounded-lg shadow-sm border border-slate-200 p-6 flex flex-col h-80">
        <h3 class="font-bold text-[#103059] text-sm uppercase tracking-wide mb-4">Requests Over Time (Last 6 Months)</h3>
        <div class="flex-grow flex items-center justify-center relative w-full h-full max-h-full">
          <div v-if="loadingStats" class="text-slate-400">Loading chart...</div>
          <div v-else-if="!monthlyChartData || monthlyChartData.labels.length === 0" class="text-slate-400 italic text-sm">No data available.</div>
          <Bar v-else :data="monthlyChartData" :options="chartOptions" class="w-full h-full" />
        </div>
      </div>

      <!-- Strand Breakdown Doughnut Chart -->
      <div class="bg-white rounded-lg shadow-sm border border-slate-200 p-6 flex flex-col h-80">
        <h3 class="font-bold text-[#103059] text-sm uppercase tracking-wide mb-4">Requests by Strand</h3>
        <div class="flex-grow flex items-center justify-center relative w-full h-full max-h-full">
          <div v-if="loadingStats" class="text-slate-400">Loading chart...</div>
          <div v-else-if="!strandChartData || strandChartData.labels.length === 0" class="text-slate-400 italic text-sm">No data available.</div>
          <Doughnut v-else :data="strandChartData" :options="pieOptions" class="w-full h-full" />
        </div>
      </div>
    </div>

    <!-- Bottom Row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Upcoming Pickup Slots (Moved to left since Strand Breakdown is now a chart) -->

      <!-- Upcoming Pickup Slots -->
      <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden flex flex-col">
        <div class="px-6 py-4 bg-slate-50 border-b flex justify-between items-center">
          <h3 class="font-bold text-[#103059] text-sm uppercase tracking-wide">Upcoming Pickups</h3>
          <button @click="$emit('change-view', 'pickup_scheduling')" class="text-[0.7rem] font-bold text-cyan-600 hover:underline px-2">Manage</button>
        </div>
        <div v-if="loadingStats" class="p-12 text-center text-slate-400">Loading schedule...</div>
        <div v-else-if="!stats.upcoming_slots?.length" class="p-12 text-center text-slate-400 italic text-sm">No upcoming slots scheduled.</div>
        <div v-else class="divide-y flex-grow">
          <div v-for="slot in stats.upcoming_slots" :key="slot.id" class="px-6 py-5 hover:bg-slate-50 transition-colors">
            <div class="flex justify-between items-start mb-2">
               <span class="font-bold text-[#103059] text-sm">{{ formatDateFull(slot.date) }}</span>
               <span class="text-[0.65rem] font-black text-slate-500">{{ slot.booked_slots }} / {{ slot.max_slots }}</span>
            </div>
            <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div class="h-full bg-amber-400 rounded-full transition-all duration-1000" :style="{ width: (Math.min((slot.booked_slots/slot.max_slots)*100, 100)) + '%' }"></div>
            </div>
          </div>
        </div>
        <div class="p-4 bg-amber-50 border-t mt-auto">
           <p class="text-[0.6rem] text-amber-700 font-bold text-center leading-tight">Note: Inform students to arrive 15 minutes before their chosen slot.</p>
        </div>
      </div>

      <!-- Popular Documents -->
      <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden flex flex-col">
        <div class="px-6 py-4 bg-slate-50 border-b flex justify-between items-center">
          <h3 class="font-bold text-[#103059] text-sm uppercase tracking-wide">Document Popularity</h3>
          <button @click="$emit('change-view', 'document_types')" class="text-[0.7rem] font-bold text-cyan-600 hover:underline px-2">Manage Types</button>
        </div>
        <div v-if="loadingStats" class="p-12 text-center text-slate-400">Loading document stats...</div>
        <div v-else class="overflow-x-auto flex-grow">
          <table class="w-full text-left text-sm">
            <thead>
              <tr class="bg-slate-50 border-b font-bold text-slate-600 uppercase text-[0.65rem] tracking-wider">
                <th class="px-6 py-3">Document</th>
                <th class="px-6 py-3 text-center">Requests</th>
                <th class="px-6 py-3">Revenue Est.</th>
              </tr>
            </thead>
            <tbody class="divide-y">
              <tr v-for="doc in stats.doc_breakdown" :key="doc.document" class="hover:bg-slate-50">
                <td class="px-6 py-3 font-bold text-slate-800 text-xs">{{ doc.document }}</td>
                <td class="px-6 py-3 text-center font-bold">{{ doc.count }}</td>
                <td class="px-6 py-3 text-right pr-6 font-mono text-xs text-green-600 font-bold">
                  ₱{{ (doc.count * (doc.price || 0)).toLocaleString() }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="p-3 bg-slate-50 border-t mt-auto">
           <p class="text-[0.6rem] text-slate-500 font-bold text-center">Total Estimated Revenue: <span class="text-green-600">₱{{ stats.doc_breakdown?.reduce((acc, d) => acc + (d.count * d.price), 0).toLocaleString() }}</span></p>
        </div>
      </div>

      <!-- Recent Requests -->
      <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden flex flex-col">
        <div class="px-6 py-4 bg-slate-50 border-b flex justify-between items-center">
          <h3 class="font-bold text-[#103059] text-sm uppercase tracking-wide">Recent Submissions</h3>
          <button @click="$emit('change-view', 'record_requests')" class="text-[0.7rem] font-bold text-cyan-600 hover:underline px-2">View All</button>
        </div>
        <div v-if="loadingStats" class="p-12 text-center text-slate-400">Loading requests...</div>
        <div v-else class="divide-y flex-grow">
          <div v-for="req in stats.recent_requests" :key="req.id" 
               @click="$emit('open-modal', req)"
               class="px-6 py-4 flex items-center justify-between hover:bg-slate-50 cursor-pointer transition-colors group">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-[#154252] text-white flex items-center justify-center font-bold text-xs ring-2 ring-slate-100">
                {{ initials(req.first_name, req.last_name) }}
              </div>
              <div class="flex flex-col">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-sm text-[#103059] group-hover:text-cyan-600 transition-colors">{{ req.first_name }} {{ req.last_name }}</span>
                  <component :is="AttachmentIcon" v-if="req.documents?.length > 0" class="w-3.5 h-3.5 text-amber-500" />
                </div>
                <span class="text-[0.7rem] text-slate-500 font-medium">{{ req.strand_display || req.strand || 'No Strand' }} \u00b7 {{ formatDate(req.submitted_at) }}</span>
              </div>
            </div>
            <span class="px-3 py-1 rounded-full text-[0.65rem] font-bold uppercase tracking-wider" :class="statusClass(req.status)">
              {{ req.status }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Paperclip as AttachmentIcon } from 'lucide-vue-next';
import { Bar, Doughnut } from 'vue-chartjs';
import {
  Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement
} from 'chart.js';

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

const props = defineProps({
  stats: Object,
  statCards: Array,
  loadingStats: Boolean,
  strandPercent: Function,
  formatDate: Function,
  formatDateFull: Function,
  initials: Function,
  statusClass: Function
});

defineEmits(['change-view', 'open-modal']);

// Chart configuration options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#103059',
      titleFont: { size: 13, weight: 'bold' },
      bodyFont: { size: 14, weight: 'bold' },
      padding: 12,
      cornerRadius: 8,
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#f1f5f9', drawBorder: false },
      ticks: { precision: 0, font: { weight: 'bold', color: '#64748b' } }
    },
    x: {
      grid: { display: false, drawBorder: false },
      ticks: { font: { weight: 'bold', color: '#64748b' } }
    }
  }
};

const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'right', labels: { font: { weight: 'bold', size: 11 }, padding: 20 } },
    tooltip: { backgroundColor: '#103059', padding: 12, cornerRadius: 8 }
  },
  cutout: '65%'
};

// Computed property to format data for the Bar Chart
const monthlyChartData = computed(() => {
  if (!props.stats || !props.stats.monthly_trend) return null;
  
  // The API returns the data ordered by most recent month first, we want chronological order for the chart
  const orderedData = [...props.stats.monthly_trend].reverse();
  
  return {
    labels: orderedData.map(item => {
      const date = new Date(item.month);
      return date.toLocaleDateString('default', { month: 'short', year: 'numeric' });
    }),
    datasets: [
      {
        label: 'Total Requests',
        backgroundColor: '#ffca28', // Yellow
        hoverBackgroundColor: '#e6b520',
        borderRadius: 6,
        data: orderedData.map(item => item.count)
      }
    ]
  };
});

// Vibrant colors for the pie chart
const strandColors = [
  '#103059', // Dark Blue
  '#006080', // Mid Blue
  '#0099cc', // Light Blue
  '#ffca28', // Yellow
  '#ff8f00', // Amber
  '#c62828', // Red
  '#388e3c', // Green
];

// Computed property to format data for the Doughnut Chart
const strandChartData = computed(() => {
  if (!props.stats || !props.stats.strand_breakdown) return null;
  
  return {
    labels: props.stats.strand_breakdown.map(item => item.strand_name || 'Not Specified'),
    datasets: [
      {
        backgroundColor: strandColors,
        borderWidth: 0,
        hoverOffset: 4,
        data: props.stats.strand_breakdown.map(item => item.count)
      }
    ]
  };
});
</script>
