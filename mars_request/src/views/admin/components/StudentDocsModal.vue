<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div class="bg-white w-full max-w-2xl rounded-lg shadow-2xl border-4 border-[#103059] flex flex-col max-h-[90vh] overflow-hidden">
        <div class="px-6 py-4 bg-[#103059] text-white flex justify-between items-center">
          <div class="flex flex-col">
             <h2 class="font-black uppercase tracking-widest text-sm text-white">Student Document Portal</h2>
             <p class="text-[0.6rem] text-amber-400 font-bold uppercase">{{ student?.first_name }} {{ student?.last_name }}</p>
          </div>
          <button @click="$emit('close')" class="text-white hover:opacity-70"><XIcon class="w-5 h-5" /></button>
        </div>
        
        <div class="p-6 overflow-y-auto flex flex-col gap-6">
          <!-- Upload Section -->
          <div class="bg-slate-50 border border-slate-200 rounded-lg p-4">
            <h3 class="text-[0.65rem] font-black text-slate-500 uppercase tracking-widest mb-4">Upload New Master Document</h3>
            <div class="flex flex-col md:flex-row gap-3">
              <select :value="form.document_type" @change="$emit('update:document_type', $event.target.value)" class="flex-1 border px-3 py-2 rounded text-sm focus:border-[#103059] outline-none bg-white">
                <option value="" disabled>Select Document Type</option>
                <option v-for="doc in docTypes" :key="doc.id" :value="doc.name">{{ doc.name }}</option>
              </select>
              <input ref="fileInput" type="file" @change="$emit('file-change', $event)" class="text-xs self-center" />
              <button @click="$emit('upload')" :disabled="uploading" class="px-4 py-2 bg-[#103059] text-[#ffca28] rounded font-black uppercase text-xs hover:bg-[#004466] disabled:opacity-50">
                 {{ uploading ? 'Uploading...' : 'Upload' }}
              </button>
            </div>
          </div>

          <!-- List Section -->
          <div class="flex flex-col gap-2">
            <h3 class="text-[0.65rem] font-black text-slate-500 uppercase tracking-widest">Available Documents</h3>
            <div v-if="!student?.documents || student.documents.length === 0" class="py-10 text-center italic text-slate-400 text-sm">
              No documents uploaded for this student yet.
            </div>
            <div v-else class="grid grid-cols-1 gap-2">
              <div v-for="doc in student.documents" :key="doc.id" class="flex items-center justify-between p-3 bg-white border border-slate-100 rounded-lg hover:shadow-sm transition-shadow">
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-amber-100 rounded text-amber-600">
                     <FileIcon class="w-4 h-4" />
                  </div>
                  <div class="flex flex-col">
                    <span class="font-bold text-[#103059] text-sm">{{ doc.document_type }}</span>
                    <span class="text-[0.6rem] text-slate-400">{{ formatDate(doc.uploaded_at) }}</span>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <a :href="getFullUrl(doc.file)" target="_blank" class="px-3 py-1 bg-slate-100 text-slate-600 text-[0.6rem] font-black uppercase rounded hover:bg-slate-200">View</a>
                  <button @click="$emit('delete-doc', doc.id)" class="p-1 px-2 bg-red-50 text-red-600 rounded hover:bg-red-100"><XIcon class="w-4 h-4" /></button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { X as XIcon, FileText as FileIcon } from 'lucide-vue-next';
import { ref } from 'vue';
import { getFullUrl } from '@/services/api';

defineProps({
  show: Boolean,
  student: Object,
  form: Object,
  docTypes: Array,
  uploading: Boolean,
  formatDate: Function
});

const fileInput = ref(null);
defineExpose({ fileInput });

defineEmits(['close', 'upload', 'file-change', 'update:document_type', 'delete-doc']);
</script>
