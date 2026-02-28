<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div class="bg-white w-full max-w-5xl rounded-lg shadow-2xl border-4 border-[#00334d] flex flex-col max-h-[95vh] overflow-hidden">
        
        <!-- Header -->
        <div class="px-6 py-4 bg-[#00334d] text-white flex justify-between items-center">
          <div class="flex flex-col">
             <h2 class="font-black uppercase tracking-widest text-sm text-white">Master Student Profile</h2>
             <p class="text-[0.6rem] text-amber-400 font-bold uppercase">{{ student?.lrn_number || 'New Record' }}</p>
          </div>
          <button @click="$emit('close')" class="text-white hover:opacity-70"><XIcon class="w-5 h-5" /></button>
        </div>

        <!-- Body -->
        <div class="flex flex-col md:flex-row flex-1 overflow-hidden">
          
          <!-- Left Column: Student Details -->
          <div class="w-full md:w-1/2 p-6 border-r border-slate-100 overflow-y-auto bg-slate-50 relative">
            
            <div class="flex items-center justify-between mb-6 border-b border-slate-200 pb-2">
              <h3 class="text-xs font-black text-slate-500 uppercase tracking-widest flex items-center gap-2">
                <UserIcon class="w-4 h-4"/> Personal Information
              </h3>
              <button @click="$emit('edit-student', student)" class="text-xs font-black text-cyan-600 bg-cyan-50 px-3 py-1 rounded hover:bg-cyan-100 flex items-center gap-1 transition-colors">
                <EditIcon class="w-3 h-3"/> Edit
              </button>
            </div>

            <div v-if="student" class="flex flex-col gap-6">
              <!-- Name identity -->
              <div class="flex items-center gap-4">
                 <div class="w-16 h-16 rounded-full bg-[#00334d] text-[#ffca28] flex items-center justify-center font-black text-xl shadow-inner border-2 border-slate-200">
                    {{ initials(student.first_name, student.last_name) }}
                  </div>
                  <div class="flex flex-col">
                    <span class="text-2xl font-black text-[#00334d]">{{ student.first_name }} {{ student.last_name }} {{ student.suffix }}</span>
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">{{ student.strand_display }} • Batch {{ student.year_graduated }}</span>
                  </div>
              </div>

              <!-- Data Grid -->
              <div class="grid grid-cols-2 gap-4">
                 <InfoItem label="First Name" :value="student.first_name" />
                 <InfoItem label="Last Name" :value="student.last_name" />
                 <InfoItem label="Middle Name" :value="student.middle_name || '—'" />
                 <InfoItem label="Sex" :value="student.sex" />
                 <InfoItem label="Birthdate" :value="formatDate(student.birthdate)" />
                 <InfoItem label="LRN Number" :value="student.lrn_number" isMono />
                 <InfoItem label="Email Space" :value="student.email" class="col-span-2" />
                 <InfoItem label="Phone" :value="student.phone_number" class="col-span-2" />
                 <InfoItem label="Permanent Address" :value="student.permanent_address" class="col-span-2" />
              </div>

            </div>
            
            <div v-else class="py-20 text-center italic text-slate-400">Loading student details...</div>

          </div>

          <!-- Right Column: Documents -->
          <div class="w-full md:w-1/2 p-6 flex flex-col bg-white overflow-y-auto">
            <h3 class="text-xs font-black text-slate-500 uppercase tracking-widest border-b border-slate-200 pb-2 mb-6 flex items-center gap-2">
              <FolderIcon class="w-4 h-4"/> Master Documents
            </h3>

            <!-- Upload Box -->
            <div class="bg-[#f8fafc] border-2 border-dashed border-[#cbd5e1] rounded-lg p-5 mb-6 hover:border-[#00334d] transition-colors relative group">
              <h4 class="text-[0.65rem] font-black text-[#00334d] uppercase mb-3 flex items-center gap-1">
                <UploadCloudIcon class="w-3.5 h-3.5" /> Upload Hardcopy Scan
              </h4>
              <div class="flex flex-col gap-3">
                <select :value="form.document_type" @change="$emit('update:document_type', $event.target.value)" class="w-full border-2 border-slate-200 px-3 py-2 rounded text-xs font-bold focus:border-[#00334d] outline-none bg-white">
                  <option value="" disabled>Select Document Type...</option>
                  <option v-for="doc in docTypes" :key="doc.id" :value="doc.name">{{ doc.name }}</option>
                </select>
                <div class="flex items-center gap-2">
                  <input ref="fileInput" type="file" @change="$emit('file-change', $event)" class="text-xs file:mr-4 file:py-1.5 file:px-4 file:rounded file:border-0 file:text-[0.65rem] file:font-black file:uppercase file:bg-slate-200 file:text-[#00334d] hover:file:bg-slate-300 transition-colors w-full cursor-pointer" />
                  <button @click="$emit('upload')" :disabled="uploading || !form.document_type" class="px-5 py-2 bg-[#ffca28] text-[#00334d] rounded border-2 border-[#00334d] font-black uppercase tracking-wider text-[0.65rem] hover:bg-white transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap">
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
              
              <div v-else class="grid grid-cols-1 gap-2 border-t border-slate-100 pt-2">
                <div v-for="doc in student.documents" :key="doc.id" class="flex items-center justify-between p-3 bg-white border border-slate-200 rounded-lg hover:border-slate-300 hover:shadow-sm transition-all group">
                  <div class="flex items-center gap-3">
                    <div class="p-2.5 bg-[#f1f5f9] rounded-lg text-[#00334d] group-hover:bg-[#00334d] group-hover:text-white transition-colors">
                       <FileIcon class="w-4 h-4" />
                    </div>
                    <div class="flex flex-col">
                      <span class="font-black text-[#00334d] text-xs uppercase">{{ doc.document_type }}</span>
                      <span class="text-[0.6rem] font-bold text-slate-400 uppercase tracking-widest">Added {{ formatDate(doc.uploaded_at) }}</span>
                    </div>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <a :href="doc.file" target="_blank" class="p-1.5 bg-slate-100 text-slate-600 rounded hover:bg-[#00334d] hover:text-white transition-colors" title="View Document">
                      <EyeIcon class="w-4 h-4" />
                    </a>
                    <button @click="$emit('delete-doc', doc.id)" class="p-1.5 bg-red-50 text-red-600 rounded hover:bg-red-500 hover:text-white transition-colors" title="Delete Document">
                      <TrashIcon class="w-4 h-4" />
                    </button>
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
  Eye as EyeIcon, Trash as TrashIcon, Edit as EditIcon
} from 'lucide-vue-next';
import { ref } from 'vue';

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
defineExpose({ fileInput });

const emit = defineEmits(['close', 'upload', 'file-change', 'update:document_type', 'delete-doc', 'edit-student']);
</script>

<script>
// Helper component for info grid
const InfoItem = {
  props: { label: String, value: [String, Number], isMono: Boolean },
  template: `
    <div class="flex flex-col gap-0.5">
      <span class="text-[0.6rem] font-black text-slate-400 uppercase tracking-widest">{{ label }}</span>
      <span class="text-sm font-bold text-[#002233]" :class="{'font-mono tracking-tight': isMono}">{{ value || '—' }}</span>
    </div>
  `
}
export default { components: { InfoItem } }
</script>
