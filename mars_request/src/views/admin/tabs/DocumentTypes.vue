<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex flex-col gap-2">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Document Types</h1>
        <p class="text-slate-500 text-sm">Configure available documents, descriptions, and processing fees.</p>
      </div>
      <button @click="$emit('open-doc-modal')" class="px-6 py-2.5 bg-[#004d66] text-white font-bold rounded hover:bg-[#003d52] transition-colors shadow-md flex items-center gap-2">
        <component :is="DocsIcon" class="w-5 h-5" /> Add New Document
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="doc in docTypes" :key="doc.id" 
           class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col group hover:shadow-md transition-all">
        <div class="p-6 flex-grow">
          <div class="flex justify-between items-start mb-4">
            <div class="p-3 bg-[#00334d]/5 rounded-lg text-[#00334d]">
              <component :is="DocsIcon" class="w-6 h-6" />
            </div>
            <span :class="[
              'px-2 py-1 rounded text-[0.6rem] font-black uppercase tracking-widest border',
              doc.is_active ? 'bg-green-50 text-green-600 border-green-100' : 'bg-red-50 text-red-600 border-red-100'
            ]">
              {{ doc.is_active ? 'Active' : 'Disabled' }}
            </span>
          </div>
          <h3 class="font-black text-[#00334d] text-lg mb-2 uppercase tracking-tight">{{ doc.name }}</h3>
          <p class="text-slate-500 text-xs leading-relaxed mb-4 line-clamp-2 italic">{{ doc.description || 'No description provided.' }}</p>
          
          <div class="flex items-center gap-2 mt-auto">
            <component :is="MoneyIcon" class="w-4 h-4 text-green-600" />
            <span class="font-black text-xl text-[#00334d]">\u20b1{{ parseFloat(doc.price).toLocaleString() }}</span>
          </div>
        </div>
        <div class="px-6 py-4 bg-slate-50 border-t flex justify-end gap-2">
          <button @click="$emit('edit-doc', doc)" class="p-2 text-cyan-600 hover:bg-cyan-100 rounded transition-colors" title="Edit">
            <component :is="CogIcon" class="w-5 h-5" />
          </button>
          <button @click="$emit('delete-doc', doc.id)" class="p-2 text-red-600 hover:bg-red-100 rounded transition-colors" title="Delete">
            <component :is="XIcon" class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FileStack as DocsIcon, DollarSign as MoneyIcon, Settings as CogIcon, X as XIcon } from 'lucide-vue-next';

defineProps({
  docTypes: Array
});

defineEmits(['open-doc-modal', 'edit-doc', 'delete-doc']);
</script>
