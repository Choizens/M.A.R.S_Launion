<template>
  <div class="p-4 bg-slate-50 border border-slate-200 rounded-lg">
    <div class="flex items-center justify-between mb-3 border-b border-dashed pb-2 border-slate-200">
      <span class="text-[#103059] font-black text-sm">{{ filename }}</span>
      <div class="flex gap-2">
         <span v-if="hasMasterScan" class="text-[0.6rem] font-black uppercase px-2 py-0.5 bg-blue-100 text-blue-600 rounded-full border border-blue-200">In Record</span>
         <span v-else class="text-[0.6rem] font-black uppercase px-2 py-0.5 bg-orange-100 text-orange-600 rounded-full border border-orange-200 animate-pulse">Missing Master</span>
         <span v-if="hasProcessedDoc" class="text-[0.6rem] font-black uppercase px-2 py-0.5 bg-green-100 text-green-600 rounded-full border border-green-200">✓ Ready</span>
         <span v-else class="text-[0.6rem] font-black uppercase px-2 py-0.5 bg-amber-100 text-amber-600 rounded-full border border-amber-200">Pending</span>
      </div>
    </div>

    <div v-if="!hasMasterScan" class="mb-3 p-2 bg-orange-50 border border-orange-100 rounded text-[0.6rem] text-orange-700 flex items-center gap-2">
      <AlertIcon class="w-3.5 h-3.5" />
      <span>Document is not in digital database. Manual search required.</span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <p class="text-[0.6rem] font-bold text-slate-400 uppercase mb-1">Student Scan:</p>
        <div v-if="studentDoc">
          <button @click="downloadDocument('student', studentDoc)" class="flex items-center gap-1 text-[0.6rem] font-bold text-amber-600 bg-white px-2 py-1 rounded border border-amber-200 shadow-sm w-max hover:bg-amber-50 transition-colors">
            <AttachmentIcon class="w-3 h-3" /> View Scan
          </button>
        </div>
        <span v-else class="text-[0.55rem] font-bold text-slate-400 italic">No scan</span>
      </div>
      <div>
        <p class="text-[0.6rem] font-bold text-slate-400 uppercase mb-1">Staff Ready Doc:</p>
        <div v-if="processedDoc" class="flex items-center gap-2">
          <button @click="downloadDocument('processed', processedDoc)" class="flex items-center gap-1.5 text-[0.6rem] font-bold text-green-600 bg-white px-2 py-1 rounded border border-green-200 shadow-sm hover:bg-green-50 transition-colors">
            <FileIcon class="w-3 h-3" /> Download
          </button>
          <button @click="deleteDoc(processedDoc.id)" class="text-[0.6rem] font-bold text-red-500 px-2 py-1 rounded border border-red-200 hover:bg-red-50 transition-colors">X</button>
        </div>
        <div v-else class="mt-1">
          <label class="cursor-pointer px-3 py-1.5 bg-[#103059] text-white text-[0.6rem] font-black uppercase rounded hover:bg-[#103059] transition-colors inline-block" :class="{'opacity-50 cursor-not-allowed': loading}">
            <input type="file" class="hidden" @change="handleUpload" :disabled="loading" />
            {{ loading ? 'Uploading...' : '⬆ Upload' }}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { adminService, getFullUrl } from '@/services/api';
import { FileText as FileIcon, Paperclip as AttachmentIcon, AlertCircle as AlertIcon } from 'lucide-vue-next';

const props = defineProps(['filename', 'request']);
const emit = defineEmits(['refresh', 'loading']);

const loading = ref(false);

const studentDoc = computed(() => {
  return props.request.documents?.find(d => d.document_type === props.filename);
});

const hasMasterScan = computed(() => {
  return !!props.request.student_record?.documents?.find(d => d.document_type === props.filename);
});

const processedDoc = computed(() => {
  return props.request.processed_documents?.find(d => d.document_type === props.filename);
});

const hasProcessedDoc = computed(() => !!processedDoc.value);

const handleUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  loading.value = true;
  try {
    const fd = new FormData();
    fd.append('document_type', props.filename);
    fd.append('file', file);
    await adminService.uploadProcessedDocument(props.request.id, fd);
    emit('refresh');
  } catch (err) { 
    alert('Upload failed'); 
  } finally {
    loading.value = false;
    event.target.value = null; // reset input
  }
};

const deleteDoc = async (id) => {
  if (!confirm('Remove document?')) return;
  loading.value = true;
  try {
    await adminService.deleteProcessedDocument(id);
    emit('refresh');
  } catch (err) { 
    alert('Delete failed'); 
  } finally {
    loading.value = false;
  }
};

const downloadDocument = async (type, doc) => {
  if (!doc) return;
  loading.value = true;
  try {
    const url = adminService.getDownloadUrl(type, doc.id);
    const token = localStorage.getItem('token');
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Download failed (${response.status})`);
    }
    
    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = blobUrl;
    
    const filename = doc.document_type || props.filename;
    const extension = doc.file.split('.').pop().split(/[?#]/)[0] || 'pdf';
    link.download = `${filename}.${extension}`;
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(blobUrl);
  } catch (error) {
    console.error('Download failed:', error);
    alert(`Download Error: ${error.message}`);
    window.open(getFullUrl(doc.file), '_blank');
  } finally {
    loading.value = false;
  }
};
</script>
