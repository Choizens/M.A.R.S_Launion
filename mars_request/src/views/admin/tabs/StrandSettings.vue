<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex flex-col gap-2">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Strand Settings</h1>
        <p class="text-slate-500 text-sm">Manage academic strands available for student records.</p>
      </div>
      <button @click="$emit('open-strand-modal')" class="px-6 py-2.5 bg-[#004d66] text-white font-bold rounded hover:bg-[#003d52] transition-colors shadow-md flex items-center gap-2">
        <component :is="DocsIcon" class="w-5 h-5" /> Add New Strand
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="s in strands" :key="s.id" 
           class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col group hover:shadow-md transition-all">
        <div class="p-6 flex-grow text-center">
          <div class="w-16 h-16 rounded-full bg-cyan-50 text-cyan-600 flex items-center justify-center font-black text-xl mx-auto mb-4 border-2 border-cyan-100 shadow-sm">
            {{ s.name[0] }}
          </div>
          <h3 class="font-black text-[#00334d] text-lg mb-2 uppercase tracking-tight">{{ s.name }}</h3>
          <p class="text-slate-500 text-xs leading-relaxed mb-4 line-clamp-2 italic">{{ s.description || 'No description provided.' }}</p>
        </div>
        <div class="px-6 py-4 bg-slate-50 border-t flex justify-end gap-2 text-center">
          <button @click="$emit('edit-strand', s)" class="p-2 text-cyan-600 hover:bg-cyan-100 rounded transition-colors" title="Edit">
            <component :is="CogIcon" class="w-5 h-5" />
          </button>
          <button @click="$emit('delete-strand', s.id)" class="p-2 text-red-600 hover:bg-red-100 rounded transition-colors" title="Delete">
            <component :is="XIcon" class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FileStack as DocsIcon, Settings as CogIcon, X as XIcon } from 'lucide-vue-next';

defineProps({
  strands: Array
});

defineEmits(['open-strand-modal', 'edit-strand', 'delete-strand']);
</script>
