<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div class="bg-white w-full max-w-5xl rounded-lg shadow-2xl border-4 border-[#103059] flex flex-col max-h-[95vh] overflow-hidden">
        
        <!-- Header -->
        <div class="px-6 py-4 bg-[#103059] text-white flex justify-between items-center">
          <div class="flex flex-col">
             <h2 class="font-black uppercase tracking-widest text-sm text-white">Master Student Profile</h2>
             <p class="text-[0.6rem] text-amber-400 font-bold uppercase">{{ student?.lrn_number || 'New Record' }}</p>
          </div>
          <button @click="$emit('close')" class="text-white hover:opacity-70"><XIcon class="w-5 h-5" /></button>
        </div>

        <!-- Body -->
        <div class="flex flex-col md:flex-row flex-1 overflow-y-auto custom-scrollbar">
          
          <!-- Left Column: Student Details -->
          <div class="w-full md:w-1/2 p-6 border-r border-slate-100 bg-white relative">
            
            <div v-if="student" class="flex flex-col gap-5">
              <!-- Minimalist Profile Header -->
              <div class="flex items-center gap-4 bg-[#f8fafc] p-3 rounded-lg border border-slate-200 shadow-sm">
                 <div class="w-12 h-12 rounded-full bg-[#103059] text-[#ffca28] flex items-center justify-center font-black text-base shadow-inner border-2 border-slate-100 shrink-0">
                    {{ initials(student.first_name, student.last_name) }}
                  </div>
                  <div class="flex flex-col min-w-0">
                    <h4 class="text-[0.6rem] font-bold text-amber-600 uppercase tracking-widest leading-none mb-0.5">RECORD ID: #{{ student.id }}</h4>
                    <span class="text-lg font-black text-[#103059] leading-none truncate uppercase">{{ student.first_name }} {{ student.last_name }}</span>
                    <span class="text-[0.6rem] font-bold text-slate-400 uppercase tracking-widest mt-1">{{ student.strand_display }} • GRADUATED {{ student.year_graduated }}</span>
                  </div>
              </div>

              <!-- Compact Information Display -->
              <div class="grid grid-cols-2 gap-x-4 gap-y-3 px-1">
                
                <!-- LRN -->
                <div class="flex flex-col">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">LRN Number</span>
                  <span class="text-[0.75rem] font-bold text-[#103059] font-mono select-all">{{ student.lrn_number }}</span>
                </div>

                <!-- Gender -->
                <div class="flex flex-col">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">Gender / Sex</span>
                  <span class="text-[0.75rem] font-bold text-[#103059]">{{ student.sex || 'Not Specified' }}</span>
                </div>

                <!-- Name Details -->
                <div class="flex flex-col">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">First Name</span>
                  <span class="text-[0.75rem] font-bold text-[#103059]">{{ student.first_name }}</span>
                </div>
                <div class="flex flex-col">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">Last Name</span>
                  <span class="text-[0.75rem] font-bold text-[#103059]">{{ student.last_name }}</span>
                </div>
                <div class="flex flex-col">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">Middle Name</span>
                  <span class="text-[0.75rem] font-bold text-[#103059]">{{ student.middle_name || '—' }}</span>
                </div>
                <div class="flex flex-col">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">Suffix</span>
                  <span class="text-[0.75rem] font-bold text-[#103059]">{{ student.suffix || '—' }}</span>
                </div>

                <!-- Academic -->
                <div class="flex flex-col">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">Strand / Track</span>
                  <span class="text-[0.75rem] font-bold text-[#103059]">{{ student.strand_display }}</span>
                </div>
                <div class="flex flex-col">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">Batch Year</span>
                  <span class="text-[0.75rem] font-bold text-[#103059]">{{ student.year_graduated }}</span>
                </div>

                <!-- Contact Info - Compacted -->
                <div class="flex flex-col col-span-2">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">Email Address</span>
                  <span class="text-[0.75rem] font-bold text-[#103059] truncate">{{ student.email }}</span>
                </div>
                <div class="flex flex-col col-span-2">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">Phone Number</span>
                  <span class="text-[0.75rem] font-bold text-[#103059]">{{ student.phone_number }}</span>
                </div>
                <div class="flex flex-col col-span-2">
                  <span class="text-[0.55rem] font-black text-slate-400 uppercase tracking-wider">Permanent Address</span>
                  <span class="text-[0.7rem] font-bold text-[#103059] leading-tight">{{ student.permanent_address }}</span>
                </div>

                <!-- Footer Meta - Very Minimal -->
                <div class="col-span-2 pt-3 mt-1 border-t border-slate-100 flex items-center justify-between text-[0.55rem] font-bold text-slate-300 uppercase tracking-widest">
                    <span>RECORD CREATED</span>
                    <span>{{ formatDate(student.created_at) }}</span>
                </div>
              </div>
            </div>
            
            <div v-else class="py-20 text-center italic text-slate-400">Loading student details...</div>

          </div>

          <!-- Right Column: Documents -->
          <div class="w-full md:w-1/2 p-6 flex flex-col bg-white">
            <h3 class="text-xs font-black text-slate-500 uppercase tracking-widest border-b border-slate-200 pb-2 mb-6 flex items-center gap-2">
              <FolderIcon class="w-4 h-4"/> Master Documents
            </h3>

            <!-- Upload Box -->
            <div class="bg-[#f8fafc] border-2 border-dashed border-[#cbd5e1] rounded-lg p-5 mb-6 hover:border-[#103059] transition-colors relative group">
              <h4 class="text-[0.65rem] font-black text-[#103059] uppercase mb-3 flex items-center gap-1">
                <UploadCloudIcon class="w-3.5 h-3.5" /> Upload Hardcopy Scan
              </h4>
              <div class="flex flex-col gap-3">
                <select :value="form.document_type" @change="$emit('update:document_type', $event.target.value)" class="w-full border-2 border-slate-200 px-3 py-2 rounded text-xs font-bold focus:border-[#103059] outline-none bg-white">
                  <option value="" disabled>Select Document Type...</option>
                  <option v-for="doc in docTypes" :key="doc.id" :value="doc.name">{{ doc.name }}</option>
                </select>
                <div class="flex items-center gap-2">
                  <input ref="fileInput" type="file" accept=".pdf,.jpg,.jpeg,.png" @change="$emit('file-change', $event)" class="text-xs file:mr-4 file:py-1.5 file:px-4 file:rounded file:border-0 file:text-[0.65rem] file:font-black file:uppercase file:bg-slate-200 file:text-[#103059] hover:file:bg-slate-300 transition-colors w-full cursor-pointer" />
                  <button @click="$emit('upload')" :disabled="uploading || !form.document_type" class="px-5 py-2 bg-[#ffca28] text-[#103059] rounded border-2 border-[#103059] font-black uppercase tracking-wider text-[0.65rem] hover:bg-white transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap">
                     {{ uploading ? 'Uploading...' : 'Save File' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Documents List -->
            <div class="flex flex-col gap-2 flex-1">
              <div v-if="!student?.documents || student.documents.length === 0" class="py-12 flex flex-col items-center justify-center text-center opacity-50">
                <FolderIcon class="w-12 h-12 text-slate-300 mb-2" />
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest">No Documents on File</p>
                <p class="text-[0.65rem] text-slate-400 mt-1 max-w-[250px]">Upload scanned master records here to permanently attach them to the student's profile.</p>
              </div>
              
              <div v-else class="flex flex-col gap-3 flex-1 overflow-hidden">
                <!-- Document Cards -->
                <div class="flex overflow-x-auto gap-4 border-t border-slate-100 pt-4 pb-2 custom-scrollbar">
                  <div v-for="doc in student.documents" :key="doc.id" class="flex-shrink-0 w-64 flex flex-col justify-between p-4 bg-[#f8fafc] border-2 border-slate-200 rounded-xl hover:border-[#103059] hover:bg-white hover:shadow-md transition-all group">
                    <div class="flex items-center gap-3 mb-3">
                      <div class="p-2.5 bg-white border border-slate-200 rounded-lg text-[#103059] group-hover:bg-[#103059] group-hover:text-white transition-colors shadow-sm">
                        <FileIcon class="w-4 h-4" />
                      </div>
                      <div class="flex flex-col min-w-0">
                        <span class="font-black text-[#103059] text-[0.75rem] uppercase leading-tight truncate">{{ doc.document_type }}</span>
                        <span class="text-[0.6rem] font-bold text-slate-400 uppercase tracking-widest mt-0.5">Added {{ formatDate(doc.uploaded_at) }}</span>
                      </div>
                    </div>
                    <div class="flex items-center justify-end gap-2">
                      <button
                        @click="viewDoc(doc)"
                        class="flex-1 flex items-center justify-center gap-1.5 p-2 bg-white border border-slate-200 text-slate-600 rounded-lg hover:bg-[#103059] hover:text-white hover:border-[#103059] transition-all shadow-sm text-[0.65rem] font-black uppercase"
                        title="View Document"
                      >
                        <EyeIcon class="w-3.5 h-3.5" />
                        VIEW
                      </button>
                      <button @click="$emit('delete-doc', doc.id)" class="p-2 bg-white border border-red-100 text-red-500 rounded-lg hover:bg-red-500 hover:text-white hover:border-red-500 transition-all shadow-sm" title="Delete Document">
                        <TrashIcon class="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>

                  <!-- Document Viewer Panel with Click-to-Open -->
                  <div 
                    v-if="viewingDoc" 
                    class="flex-1 flex flex-col border-2 border-[#103059] rounded-xl overflow-hidden group/preview relative" 
                    style="min-height: 420px;"
                  >
                    <div class="flex items-center justify-between px-4 py-2 bg-[#103059] text-white shrink-0 relative z-20">
                      <span class="text-[0.65rem] font-black uppercase tracking-widest truncate">📄 {{ viewingDoc.document_type }}</span>
                      <div class="flex items-center gap-3">
                        <button @click="printDocument(getFullUrl(viewingDoc.file))" class="text-[#ffca28] hover:text-white transition-colors text-[0.65rem] font-black uppercase flex items-center gap-1">
                          <PrinterIcon class="w-3 h-3" /> Print
                        </button>
                        <button @click="downloadDocument(getFullUrl(viewingDoc.file), viewingDoc.document_type)" class="text-[#ffca28] hover:text-white transition-colors text-[0.65rem] font-black uppercase flex items-center gap-1">
                          <DownloadIcon class="w-3 h-3" /> Download
                        </button>
                        <div class="h-3 w-[1px] bg-white/20 mx-1"></div>
                        <a :href="getFullUrl(viewingDoc.file)" target="_blank" rel="noopener noreferrer" class="text-white hover:text-amber-300 transition-colors text-[0.65rem] font-black uppercase">↗ Full Screen</a>
                        <button @click="viewingDoc = null" class="text-white opacity-70 hover:opacity-100 transition-opacity text-xs font-black uppercase ml-2">✕ Close</button>
                      </div>
                    </div>

                    <!-- Clickable Preview Area -->
                    <div 
                      class="flex-1 w-full bg-slate-50 relative cursor-pointer overflow-hidden"
                      @click="window.open(getFullUrl(viewingDoc.file), '_blank')"
                      title="Click to open in new tab"
                    >
                      <!-- Hover Overlay -->
                      <div class="absolute inset-0 bg-[#103059]/0 group-hover/preview:bg-[#103059]/5 transition-colors z-10 flex items-center justify-center">
                        <div class="opacity-0 group-hover/preview:opacity-100 transition-opacity bg-white/90 text-[#103059] px-4 py-2 rounded-full shadow-lg font-black text-[0.6rem] uppercase tracking-widest flex items-center gap-2">
                          <EyeIcon class="w-3 h-3" /> Click to View Full Screen
                        </div>
                      </div>

                      <!-- Image viewer -->
                      <img
                        v-if="viewingDoc.file && (viewingDoc.file.toLowerCase().endsWith('.jpg') || viewingDoc.file.toLowerCase().endsWith('.jpeg') || viewingDoc.file.toLowerCase().endsWith('.png'))"
                        :key="`img-${viewingDoc.id}`"
                        :src="getFullUrl(viewingDoc.file)"
                        class="w-full h-full object-contain pointer-events-none"
                        style="min-height: 380px;"
                        alt="Document Preview"
                      />
                      <!-- PDF viewer (Standardized iframe) -->
                      <div v-else class="w-full h-full flex flex-col" style="min-height: 380px;">
                        <iframe
                          :key="`pdf-ifrm-${viewingDoc.id}`"
                          :src="getFullUrl(viewingDoc.file)"
                          class="w-full h-full border-none pointer-events-none"
                        >
                        </iframe>
                      </div>
                    </div>
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
import { 
  X as XIcon, User as UserIcon, Folder as FolderIcon,
  UploadCloud as UploadCloudIcon, FileText as FileIcon,
  Eye as EyeIcon, Trash as TrashIcon, Printer as PrinterIcon,
  Download as DownloadIcon
} from 'lucide-vue-next';
import { ref, watch } from 'vue';
import { getFullUrl } from '@/services/api';

const props = defineProps({
  show: Boolean,
  student: Object,
  form: Object,
  docTypes: Array,
  uploading: Boolean,
  formatDate: Function,
  initials: Function
});

const fileInput = ref(null);
const viewingDoc = ref(null);
defineExpose({ fileInput });

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
    // Fallback if fetch fails (e.g. CORS)
    window.open(url, '_blank');
  }
};

const viewDoc = (doc) => {
  viewingDoc.value = doc;
};

const emit = defineEmits(['close', 'upload', 'file-change', 'update:document_type', 'delete-doc', 'edit-student']);

// Reset viewer when modal is closed
watch(() => props.show, (val) => {
  if (!val) viewingDoc.value = null;
});
</script>

<script>
export default {
  // Any legacy Options API if needed, but currently empty
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #103059;
}
</style>
