<template>
  <div class="flex flex-col gap-6">
    <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">System Audit Logs</h1>
    <div class="bg-white rounded-lg shadow-sm border border-[#e2e8f0] overflow-hidden">
      <div class="h-[600px] overflow-y-auto">
        <table class="w-full text-left border-collapse">
          <thead class="sticky top-0 z-10">
            <tr class="bg-slate-50 border-b-2 border-[#333]">
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest w-[200px]">Timestamp</th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest w-[150px]">User</th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest w-[200px]">Action</th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest">Details</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200">
            <tr v-for="log in auditLogs" :key="log.id" class="text-sm hover:bg-slate-50 transition-colors">
              <td class="px-6 py-4 text-slate-500 font-mono text-[0.75rem]">{{ formatDateTime(log.timestamp) }}</td>
              <td class="px-6 py-4 font-bold text-[#00334d]">{{ log.user_name || 'System' }}</td>
              <td class="px-6 py-4"><span class="px-2 py-1 bg-slate-100 rounded text-[0.65rem] font-bold uppercase tracking-wide">{{ log.action }}</span></td>
              <td class="px-6 py-4 text-slate-600 text-[0.8rem]">{{ log.details }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  auditLogs: Array,
  formatDateTime: Function
});
</script>
