<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="$emit('close')">
      <div class="bg-white w-full max-w-2xl rounded-lg shadow-2xl border-4 border-[#103059] flex flex-col max-h-[95vh] overflow-hidden">
        <!-- Modal Header -->
        <div class="px-8 py-6 bg-[#103059] text-white flex justify-between items-center relative overflow-hidden">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded bg-white text-[#103059] flex items-center justify-center font-black text-lg">
              {{ request?.first_name[0] }}{{ request?.last_name[0] }}
            </div>
            <div class="flex flex-col">
              <h2 class="text-xl font-black uppercase tracking-tight">{{ request?.first_name }} {{ request?.last_name }}</h2>
              <span class="text-[0.7rem] text-amber-300 font-bold uppercase tracking-widest">Student Portal Request</span>
            </div>
          </div>
          <button @click="$emit('close')" class="p-2 hover:bg-white/10 rounded-full transition-colors relative z-10">
            <XIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- Modal Body -->
        <div class="p-8 overflow-y-auto" v-if="request">
          <!-- Pickup Schedule Banner -->
          <div class="mb-8 p-4 bg-amber-50 rounded-lg border-2 border-dashed border-amber-200 flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="p-2 bg-amber-400 rounded text-amber-900"><ClockIcon class="w-6 h-6" /></div>
              <div>
                <h4 class="text-[0.6rem] font-black text-amber-600 uppercase tracking-widest">Preferred Pickup Schedule</h4>
                <p class="text-sm font-bold text-[#103059]">{{ formatDate(request.pickup_date) }} @ {{ request.pickup_time || 'No time set' }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Profile Information</h3>
              <div class="flex flex-col gap-2">
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Graduation Year:</span> <span class="text-sm font-bold text-[#103059]">{{ request.year_graduated }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Strand:</span> <span class="text-sm font-bold text-[#103059]">{{ request.strand }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">LRN:</span> <span class="text-sm font-bold text-[#103059]">{{ request.lrn_number || '\u2014' }}</span></div>
              </div>
            </div>
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Contact Info</h3>
              <div class="flex flex-col gap-2">
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Email:</span> <span class="text-sm font-bold text-[#103059]">{{ request.email }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Phone:</span> <span class="text-sm font-bold text-[#103059]">{{ request.phone_number }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Date Applied:</span> <span class="text-sm font-bold text-[#103059]">{{ formatDate(request.submitted_at) }}</span></div>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-4 mb-10">
            <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Requested Documents</h3>
            <div class="flex flex-col gap-3">
              <div v-for="f in request.requested_files" :key="f" 
                   class="p-4 bg-slate-50 border border-slate-200 rounded-lg">
                <div class="flex items-center justify-between mb-3 border-b border-dashed pb-2 border-slate-200">
                  <span class="text-[#103059] font-black text-xs uppercase tracking-wider">{{ f }}</span>
                  <div class="flex gap-2">
                    <span v-if="request.student_record?.documents?.find(d => d.document_type === f)"
                          class="text-[0.55rem] font-black uppercase px-2 py-0.5 bg-blue-100 text-blue-600 rounded-full border border-blue-200">In Record</span>
                    <span v-else class="text-[0.55rem] font-black uppercase px-2 py-0.5 bg-orange-100 text-orange-600 rounded-full border border-orange-200 animate-pulse">Missing Master</span>
                    <span v-if="request.processed_documents?.find(d => d.document_type === f)"
                          class="text-[0.55rem] font-black uppercase px-2 py-0.5 bg-green-100 text-green-600 rounded-full border border-green-200">Ready</span>
                    <span v-else class="text-[0.55rem] font-black uppercase px-2 py-0.5 bg-slate-100 text-slate-400 rounded-full border border-slate-200">Processing</span>
                  </div>
                </div>

                <!-- Missing File Warning -->
                <div v-if="!request.student_record?.documents?.find(d => d.document_type === f)" 
                     class="mb-3 p-2 bg-orange-50 border border-orange-100 rounded text-[0.6rem] text-orange-700 flex items-center gap-2">
                  <AlertIcon class="w-3 h-3" />
                  <span>This document is not in the digital database. Manual physical search required.</span>
                </div>

                <div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
                  <!-- Student Scan -->
                  <div>
                    <p class="text-[0.55rem] font-bold text-slate-400 uppercase mb-1">Student Scan:</p>
                    <div v-if="request.documents?.find(d => d.document_type === f)">
                      <button @click="viewDoc(request.documents.find(d => d.document_type === f))"
                         class="inline-flex items-center gap-1.5 text-[0.6rem] font-bold text-amber-600 hover:text-white hover:bg-amber-600 transition-colors bg-white px-2 py-1 rounded border border-amber-200 shadow-sm">
                        <AttachmentIcon class="w-2.5 h-2.5" /> View Scan
                      </button>
                    </div>
                    <span v-else class="text-[0.55rem] font-bold text-slate-300 italic">None</span>
                  </div>

                  <!-- Master Record -->
                  <div>
                    <p class="text-[0.55rem] font-bold text-slate-400 uppercase mb-1">Database Record:</p>
                    <div v-if="request.student_record?.documents?.find(d => d.document_type === f)">
                      <button @click="viewDoc(request.student_record.documents.find(d => d.document_type === f))"
                         class="inline-flex items-center gap-1.5 text-[0.6rem] font-bold text-blue-600 hover:text-white hover:bg-blue-600 transition-colors bg-white px-2 py-1 rounded border border-blue-200 shadow-sm">
                        <FileIcon class="w-2.5 h-2.5" /> View Master
                      </button>
                    </div>
                    <span v-else class="text-[0.55rem] font-bold text-slate-300 italic">Not Found</span>
                  </div>

                  <!-- Processed/Ready Doc -->
                  <div>
                    <p class="text-[0.55rem] font-bold text-slate-400 uppercase mb-1">Ready Document:</p>
                    <div v-if="request.processed_documents?.find(d => d.document_type === f)">
                      <button @click="viewDoc(request.processed_documents.find(d => d.document_type === f))"
                         class="inline-flex items-center gap-1.5 text-[0.6rem] font-bold text-green-600 hover:text-white hover:bg-green-600 transition-colors bg-white px-2 py-1 rounded border border-green-200 shadow-sm">
                        <FileIcon class="w-2.5 h-2.5" /> View Ready
                      </button>
                    </div>
                    <span v-else class="text-[0.55rem] font-bold text-slate-300 italic">Not Uploaded</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- New Inline Document Viewer Panel -->
            <div v-if="viewingDoc" class="mt-8 flex flex-col border-2 border-[#103059] rounded-xl overflow-hidden shadow-lg animate-in fade-in slide-in-from-bottom-4 duration-300" style="min-height: 500px;">
              <div class="flex items-center justify-between px-4 py-3 bg-[#103059] text-white shrink-0">
                <div class="flex items-center gap-2">
                  <FileIcon class="w-4 h-4 text-amber-400" />
                  <span class="text-[0.7rem] font-black uppercase tracking-widest truncate">{{ viewingDoc.document_type }}</span>
                </div>
                <div class="flex items-center gap-3">
                  <button @click="printDocument(getFullUrl(viewingDoc.file))" class="text-[#ffca28] hover:text-white transition-colors text-[0.65rem] font-black uppercase flex items-center gap-1">
                    <PrinterIcon class="w-3.5 h-3.5" /> Print
                  </button>
                  <button @click="downloadDocument(getFullUrl(viewingDoc.file), viewingDoc.document_type)" class="text-[#ffca28] hover:text-white transition-colors text-[0.65rem] font-black uppercase flex items-center gap-1">
                    <DownloadIcon class="w-3.5 h-3.5" /> Download
                  </button>
                  <div class="h-4 w-[1px] bg-white/20 mx-1"></div>
                  <a :href="getFullUrl(viewingDoc.file)" target="_blank" rel="noopener noreferrer" class="text-white hover:text-amber-300 transition-colors text-[0.65rem] font-black uppercase">↗ Full Screen</a>
                  <button @click="viewingDoc = null" class="text-white opacity-70 hover:opacity-100 transition-opacity text-xs font-black uppercase ml-2">✕ Close</button>
                </div>
              </div>
              
              <div class="flex-1 bg-slate-100 relative">
                <!-- Loader -->
                <div class="absolute inset-0 flex items-center justify-center opacity-20 pointer-events-none">
                  <FileIcon class="w-20 h-20 text-[#103059] animate-pulse" />
                </div>
                
                <!-- Image viewer -->
                <img
                  v-if="viewingDoc.file && (viewingDoc.file.toLowerCase().endsWith('.jpg') || viewingDoc.file.toLowerCase().endsWith('.jpeg') || viewingDoc.file.toLowerCase().endsWith('.png'))"
                  :key="`img-${viewingDoc.id}`"
                  :src="getFullUrl(viewingDoc.file)"
                  class="w-full h-full object-contain relative z-10"
                  alt="Document Preview"
                />
                <!-- PDF viewer -->
                <div v-else class="w-full h-full relative z-10">
                  <object
                    :key="`pdf-obj-${viewingDoc.id}`"
                    :data="getFullUrl(viewingDoc.file)"
                    type="application/pdf"
                    class="w-full h-full"
                  >
                    <iframe
                      :key="`pdf-ifrm-${viewingDoc.id}`"
                      :src="getFullUrl(viewingDoc.file)"
                      class="w-full h-full border-none"
                    >
                      <div class="p-10 text-center flex flex-col items-center justify-center h-full">
                        <AlertIcon class="w-12 h-12 text-slate-300 mb-4" />
                        <p class="text-xs font-bold text-slate-500 mb-4 uppercase tracking-widest">PDF Preview not supported by browser</p>
                        <a :href="getFullUrl(viewingDoc.file)" target="_blank" class="px-6 py-2.5 bg-[#103059] text-white rounded-lg font-black text-[0.7rem] uppercase tracking-wider shadow-md hover:bg-[#1a4a8a] transition-colors">Download to View</a>
                      </div>
                    </iframe>
                  </object>
                </div>
              </div>
            </div>
          </div>

          <!-- Status Display (Read-Only for Admin) -->
          <div class="border-t pt-6 flex flex-col gap-3">
            <div class="flex items-center gap-3 px-4 py-3 bg-slate-50 rounded border border-dashed border-slate-200">
              <span class="text-xs font-bold text-slate-500 uppercase tracking-widest">Request Status:</span>
              <span class="px-4 py-1 rounded-full text-[0.7rem] font-black uppercase tracking-wider shadow-sm" :class="statusClass(request.status)">
                {{ request.status }}
              </span>
            </div>

            <div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg shadow-sm">
              <div class="w-8 h-8 bg-amber-400 rounded-full flex items-center justify-center shrink-0 text-white font-black text-sm shadow-inner">!</div>
              <p class="text-[0.78rem] font-semibold text-amber-800 leading-relaxed">
                Actions like <strong>Start Process, Approve, Complete,</strong> and <strong>Reject</strong> are reserved for <strong>Staff</strong> accounts. As an Admin, you have <strong>read-only</strong> access to request details.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { 
  X as XIcon, Clock as ClockIcon, Paperclip as AttachmentIcon, 
  FileText as FileIcon, AlertCircle as AlertIcon, Printer as PrinterIcon,
  Download as DownloadIcon
} from 'lucide-vue-next';
import { ref, watch } from 'vue';
import { getFullUrl } from '@/services/api';

const props = defineProps({
  show: Boolean,
  request: Object,
  formatDate: Function,
  statusClass: Function
});

const emit = defineEmits(['close']);

const viewingDoc = ref(null);

const viewDoc = (doc) => {
  viewingDoc.value = doc;
};

const printDocument = (url) => {
  if (!url) return;
  const printWindow = window.open(url, '_blank');
  if (printWindow) {
    printWindow.onload = () => {
      printWindow.print();
    };
  }
};

const downloadDocument = async (url, filename) => {
  try {
    const response = await fetch(url);
    const blob = await response.blob();
    const blobUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = blobUrl;
    
    // Extract extension from URL
    const extension = url.split('.').pop().split(/[?#]/)[0] || 'pdf';
    link.download = `${filename}.${extension}`;
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(blobUrl);
  } catch (error) {
    console.error('Download failed:', error);
    window.open(url, '_blank');
  }
};

watch(() => props.show, (val) => {
  if (!val) viewingDoc.value = null;
});
</script>
