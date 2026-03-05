<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="$emit('close')">
      <div class="bg-white w-full max-w-2xl rounded-lg shadow-2xl border-4 border-[#103059] flex flex-col max-h-[95vh] overflow-hidden">
        <!-- Header -->
        <div class="px-8 py-6 bg-[#103059] text-white flex justify-between items-center shrink-0">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded bg-white text-[#103059] flex items-center justify-center font-black text-lg">
              {{ initials(request.first_name, request.last_name) }}
            </div>
            <div class="flex flex-col">
              <h2 class="text-xl font-black uppercase tracking-tight">{{ request.first_name }} {{ request.last_name }}</h2>
              <span class="text-[0.7rem] text-amber-300 font-bold uppercase tracking-widest">MARS Document Request</span>
            </div>
          </div>
          <button @click="$emit('close')" class="p-2 hover:bg-white/10 rounded-full transition-colors"><XIcon class="w-6 h-6" /></button>
        </div>

        <!-- Body -->
        <div class="p-8 overflow-y-auto">
          <!-- Schedule Alert -->
          <div class="mb-8 p-4 bg-amber-50 rounded-lg border-2 border-dashed border-amber-200 flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="p-2 bg-amber-400 rounded text-amber-900"><ClockIcon class="w-6 h-6" /></div>
              <div>
                <h4 class="text-[0.6rem] font-black text-amber-600 uppercase tracking-widest">Preferred Schedule</h4>
                <p class="text-sm font-bold text-[#103059]">{{ formatDate(request.pickup_date) }} @ {{ request.pickup_time || 'No time set' }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Academic Info</h3>
              <div class="flex flex-col gap-2">
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Graduation Year:</span> <span class="text-sm font-bold text-[#103059]">{{ request.year_graduated }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Strand:</span> <span class="text-sm font-bold text-[#103059]">{{ request.strand }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">LRN:</span> <span class="text-sm font-bold text-[#103059]">{{ request.lrn_number || '—' }}</span></div>
              </div>
            </div>
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Contact Info</h3>
              <div class="flex flex-col gap-2">
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Email:</span> <span class="text-sm font-bold text-[#103059] truncate max-w-[150px]">{{ request.email }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Phone:</span> <span class="text-sm font-bold text-[#103059]">{{ request.phone_number }}</span></div>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-4 mb-10">
            <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Requested Documents</h3>
            <div class="flex flex-col gap-3">
              <!-- Extracted Document row component -->
              <DocumentUploadRow 
                v-for="f in request.requested_files" 
                :key="f" 
                :filename="f" 
                :request="request" 
                @refresh="refreshRequestData" 
              />
            </div>
          </div>

          <div class="border-t pt-8 flex flex-col gap-6">
            <div class="flex items-center justify-between p-4 rounded-lg bg-slate-50 border border-slate-200">
               <div class="flex flex-col">
                  <h4 class="text-sm font-bold text-[#103059]">Accountability Clearance</h4>
                  <p class="text-[0.6rem] text-slate-500 italic uppercase">Verify student obligations</p>
               </div>
               <button @click="toggleAccountability" :class="['px-6 py-2 rounded-full text-[0.65rem] font-black uppercase transition-all border-2', request.no_accountabilities ? 'bg-green-500 border-green-600 text-white shadow-lg' : 'bg-white border-slate-300 text-slate-400 hover:border-red-400']">
                  {{ request.no_accountabilities ? 'Cleared' : 'Not Cleared' }}
               </button>
            </div>

            <div class="flex flex-col gap-4">
              <div class="bg-white border-2 border-[#103059] rounded-xl p-6">
                <!-- Status Logic (Simplified for Component) -->
                 <div v-if="!isVerifyingPasskey" class="flex gap-2">
                    <button v-if="request.status === 'Pending' || request.status === 'Needs Verification'" @click="updateStatus('Approved')" class="flex-1 py-4 bg-[#10b981] text-white font-black uppercase rounded-lg shadow-md hover:bg-emerald-600">Approve</button>
                    <button v-if="request.status === 'Approved'" @click="startCompletion" class="flex-1 py-4 bg-[#8b5cf6] text-white font-black uppercase rounded-lg shadow-md hover:bg-purple-600">Complete</button>
                    <button @click="updateStatus('Rejected')" class="px-6 py-4 bg-red-50 text-red-600 font-black uppercase rounded-lg border-2 border-red-200 hover:bg-red-100 transition-all">Reject</button>
                 </div>

                 <!-- Redesigned Verification for Completion (Mockup Style) -->
                 <div v-else class="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-purple-600/20 backdrop-blur-sm animate-in fade-in duration-200">
                    <div class="bg-[#fff9e6] w-full max-w-xl rounded-sm border-[3px] border-purple-400 p-8 relative flex flex-col gap-8 shadow-2xl">
                      <!-- Mockup Header -->
                      <div class="flex justify-between items-start">
                        <div>
                          <h2 class="text-3xl font-bold text-[#333] tracking-tight">Releasing a Document....</h2>
                          <p class="text-sm font-bold text-slate-500 mt-1">Enter the given Request Key of the Graduates.</p>
                        </div>
                        <button @click="isVerifyingPasskey = false" class="bg-[#f04e5d] text-white px-4 py-1.5 rounded font-black text-xs uppercase hover:bg-red-600 transition-colors">Close</button>
                      </div>

                      <!-- Large Input Box -->
                      <div class="flex flex-col gap-3">
                        <div class="bg-white border-[2px] border-slate-900 p-12 flex items-center justify-center">
                          <input 
                            v-model="enteredPasskey" 
                            type="text" 
                            placeholder="SHS-2026-XXXX / PASS-2026-XXXX" 
                            class="w-full text-center text-5xl font-black tracking-[0.2em] text-[#333] focus:outline-none placeholder:text-slate-200 uppercase bg-transparent"
                            autofocus
                          />
                        </div>
                        <p class="text-center font-bold text-slate-700 text-sm">Enter the Request key here</p>
                      </div>

                      <!-- Reminder Section -->
                      <div class="flex flex-col gap-2">
                        <h4 class="text-lg font-black text-[#f28e1c] uppercase tracking-wide">Reminder:</h4>
                        <div class="flex flex-col gap-3">
                          <p class="text-sm font-medium text-slate-800 leading-relaxed">
                            Please ensure all documents listed below are prepared and physically verified before finalizing the release. This action cannot be undone.
                          </p>
                          <!-- Document List inside Reminder area -->
                          <div class="flex flex-wrap gap-2">
                            <span v-for="f in request.requested_files" :key="f" class="text-[0.65rem] font-black uppercase px-2 py-1 bg-white border border-slate-200 rounded text-slate-600">
                              {{ f }}
                            </span>
                          </div>
                        </div>
                      </div>

                      <!-- Action Buttons -->
                      <div class="grid grid-cols-2 gap-8 mt-4">
                        <button @click="isVerifyingPasskey = false" class="py-4 border-2 border-slate-900 bg-white text-slate-900 font-bold uppercase tracking-wider hover:bg-slate-50 transition-all">
                          Cancel
                        </button>
                        <button 
                          @click="handlePrintAndSave" 
                          :disabled="!isPasskeyValid"
                          :class="['py-4 font-black uppercase tracking-wider transition-all shadow-md', isPasskeyValid ? 'bg-[#0a4a6b] text-white hover:bg-[#083a54]' : 'bg-slate-300 text-slate-500 cursor-not-allowed opacity-50']"
                        >
                          Print & Save
                        </button>
                      </div>
                      
                      <!-- Error Floating -->
                      <p v-if="enteredPasskey.length >= 8 && !isPasskeyValid" class="absolute bottom-32 left-1/2 -translate-x-1/2 text-[0.6rem] font-black text-red-500 bg-red-50 px-3 py-1 rounded-full border border-red-100 shadow-sm uppercase tracking-tighter">
                         INVALID REQUEST KEY • CHECK LOGS
                      </p>
                    </div>
                 </div>

                 <button v-if="!isVerifyingPasskey && request.status === 'Pending'" @click="updateStatus('Needs Verification')" class="w-full mt-2 py-2.5 bg-orange-500 text-white font-black uppercase rounded-lg shadow-md hover:bg-orange-600">Notify: Missing Record</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue';
import { adminService } from '@/services/api';
import { X as XIcon, Clock as ClockIcon, Check as CheckIcon } from 'lucide-vue-next';
import DocumentUploadRow from './DocumentUploadRow.vue';
import html2pdf from 'html2pdf.js';

const props = defineProps(['request']);
const emit = defineEmits(['close', 'refresh']);

const isVerifyingPasskey = ref(false);
const enteredPasskey = ref('');
const passkeyError = ref('');

const isPasskeyValid = computed(() => {
  const entered = enteredPasskey.value.trim().toUpperCase();
  return entered === props.request.request_code?.toUpperCase() || 
         entered === props.request.passkey?.toUpperCase();
});

const startCompletion = () => {
  isVerifyingPasskey.value = true;
  enteredPasskey.value = '';
  passkeyError.value = '';
};

const handlePrintAndSave = async () => {
  if (!isPasskeyValid.value) {
    passkeyError.value = 'Passkey does not match.';
    return;
  }

  const docList = props.request.requested_files.map(f => `<li>${f}</li>`).join('');
  
  // Create shared HTML template
  const contentHtml = `
    <div style="font-family: sans-serif; padding: 40px; background: white;">
      <div style="text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px;">
        <h1>M.A.R.S DOCUMENT REQUEST</h1>
        <p>Request Key: ${props.request.request_code}</p>
      </div>
      <div style="margin-bottom: 30px; line-height: 1.6;">
        <p><b style="display: inline-block; width: 120px;">Student:</b> ${props.request.first_name} ${props.request.last_name}</p>
        <p><b style="display: inline-block; width: 120px;">LRN:</b> ${props.request.lrn_number || 'N/A'}</p>
        <p><b style="display: inline-block; width: 120px;">Date:</b> ${new Date().toLocaleDateString()}</p>
      </div>
      <div style="margin-top: 20px;">
        <h3>Documents Issued:</h3>
        <ul>${docList}</ul>
      </div>
      <div style="margin-top: 50px; font-size: 10px; border-top: 1px solid #ccc; padding-top: 10px; text-align: center; color: #666;">
        Processed via M.A.R.S System • ${new Date().toLocaleString()}
      </div>
    </div>
  `;

  // UI feedback during generation
  const originalBtnText = document.activeElement ? document.activeElement.innerText : 'PRINT & SAVE';
  if (document.activeElement) document.activeElement.innerText = 'GENERATING PDF...';

  // 1. Auto-download PDF using html2pdf
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = contentHtml;
  
  const opt = {
    margin:       0.5,
    filename:     `${props.request.last_name}_document.pdf`,
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2 },
    jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
  };
  
  try {
     // Generate PDF as base64 string
     const pdfBase64 = await html2pdf().set(opt).from(tempDiv).outputPdf('datauristring');
     
     // Strip the meta prefix to get pure base64
     const base64Data = pdfBase64.split(',')[1];
     const byteCharacters = atob(base64Data);
     const byteNumbers = new Array(byteCharacters.length);
     for (let i = 0; i < byteCharacters.length; i++) {
         byteNumbers[i] = byteCharacters.charCodeAt(i);
     }
     const byteArray = new Uint8Array(byteNumbers);
     
     // Create a blob and force download securely
     const blob = new Blob([byteArray], { type: 'application/pdf' });
     const blobUrl = URL.createObjectURL(blob);
     
     const downloadLink = document.createElement('a');
     downloadLink.href = blobUrl;
     downloadLink.download = `${props.request.last_name}_document.pdf`;
     document.body.appendChild(downloadLink);
     downloadLink.click();
     
     setTimeout(() => {
        document.body.removeChild(downloadLink);
        URL.revokeObjectURL(blobUrl);
     }, 1000);
     
     // Give the browser a moment to process the download click
     await new Promise(resolve => setTimeout(resolve, 800));
  } catch (err) {
     console.error('PDF Generation Failed', err);
     alert('PDF failed to generate. Continuing to Print preview.');
  }

  if (document.activeElement) document.activeElement.innerText = originalBtnText;

  // 2. Open physical print preview window
  const printWindow = window.open('', '_blank');
  if (printWindow) {
    printWindow.document.write(`
      <html>
        <head>
          <title>MARS - Request Summary [${props.request.request_code}]</title>
        </head>
        <body>
          ${contentHtml}
          <script>window.print(); window.onload = function() { setTimeout(function() { window.close(); }, 500); }${'</scr' + 'ipt>'}
        </body>
      </html>
    `);
  } else {
    alert("Pop-up blocker prevented the Print window from opening. The PDF was still saved.");
  }

  // 3. Update status in DB
  try {
    const res = await adminService.updateRequest(props.request.id, { status: 'Completed' });
    props.request.status = res.data.status;
    emit('refresh');
    isVerifyingPasskey.value = false;
  } catch (err) {
    alert('Failed to update status, but documents were generated.');
  }
};

const refreshRequestData = async () => {
  try {
    const res = await adminService.getRequest(props.request.id);
    Object.assign(props.request, res.data);
    emit('refresh');
  } catch (err) {
    console.error('Failed to manually refresh request data', err);
  }
};

const updateStatus = async (status) => {
  try {
    const res = await adminService.updateRequest(props.request.id, { status });
    props.request.status = res.data.status;
    emit('refresh');
  } catch (err) { alert('Update failed'); }
};

const toggleAccountability = async () => {
  try {
    const res = await adminService.updateRequest(props.request.id, { no_accountabilities: !props.request.no_accountabilities });
    props.request.no_accountabilities = res.data.no_accountabilities;
    emit('refresh');
  } catch (err) { alert('Update failed'); }
};

const initials = (f, l) => `${f?.[0] || ''}${l?.[0] || ''}`.toUpperCase();
const formatDate = (dt) => dt ? new Date(dt).toLocaleDateString('en-PH', { month: 'short', day: 'numeric', year: 'numeric' }) : '—';
</script>
