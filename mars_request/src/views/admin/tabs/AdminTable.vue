<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Administrator Management</h1>
      <button @click="$emit('open-modal')" class="px-6 py-2.5 bg-[#103059] text-white font-bold rounded hover:bg-[#003d52] transition-colors shadow-md flex items-center gap-2">
        <component :is="ShieldIcon" class="w-5 h-5" /> Add Admin
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-[#e2e8f0] overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-50 border-b-2 border-[#333]">
            <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest">Full Name</th>
            <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest">Username</th>
            <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest">Email</th>
            <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest">Department</th>
            <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest">Last Login</th>
            <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest text-center">Status</th>
            <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest text-center">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200">
          <tr v-if="adminList.length === 0" class="p-20 text-center">
            <td colspan="7" class="py-20 italic text-slate-400">No administrators found.</td>
          </tr>
          <tr v-for="adm in adminList" :key="adm.id" class="hover:bg-slate-50 transition-colors" :class="{'opacity-60': !adm.is_active}">
            <td class="px-6 py-4 font-bold text-[#103059]">
              <div class="flex flex-col">
                <div class="flex items-center gap-2">
                  <span>{{ adm.full_name }}</span>
                  <span class="px-1.5 py-0.5 bg-amber-100 text-amber-700 text-[0.55rem] font-black uppercase rounded border border-amber-200">Admin</span>
                </div>
                <span class="text-[0.6rem] font-mono text-slate-400 uppercase tracking-wider">{{ adm.staff_id || 'NO-ID' }}</span>
              </div>
            </td>
            <td class="px-6 py-4 text-sm text-slate-600">@{{ adm.username }}</td>
            <td class="px-6 py-4 text-sm text-slate-500 italic">{{ adm.email || 'no email' }}</td>
            <td class="px-6 py-4 text-sm font-semibold text-slate-500">{{ adm.department }}</td>
            <td class="px-6 py-4 text-[0.7rem] font-mono text-slate-500">{{ formatDateTime(adm.last_login) || 'Never logged in' }}</td>
            <td class="px-6 py-4 text-center">
              <button 
                @click="$emit('toggle-status', adm)" 
                class="px-3 py-1 text-[0.65rem] font-black uppercase tracking-wider rounded-full shadow-sm transition-all"
                :class="adm.is_active ? 'bg-green-100 text-green-700 hover:bg-green-200' : 'bg-slate-200 text-slate-500 hover:bg-slate-300'"
              >
                {{ adm.is_active ? 'Active' : 'Inactive' }}
              </button>
            </td>
            <td class="px-6 py-4 text-center flex justify-center gap-2">
              <button @click="$emit('edit', adm)" class="p-2 text-cyan-600 hover:bg-cyan-50 rounded transition-colors" title="Edit Admin">
                <component :is="CogIcon" class="w-5 h-5" />
              </button>
              <button @click="$emit('delete', adm.id)" class="p-2 text-red-600 hover:bg-red-50 rounded transition-colors" title="Delete Admin">
                <component :is="XIcon" class="w-5 h-5" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ShieldAlert as ShieldIcon, Settings as CogIcon, X as XIcon } from 'lucide-vue-next';

defineProps({
  adminList: Array,
  formatDateTime: Function
});

defineEmits(['open-modal', 'edit', 'delete', 'toggle-status']);
</script>
