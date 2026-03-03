<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="$emit('close')">
      <div class="bg-white w-full max-w-2xl rounded-lg shadow-2xl border-4 border-[#00334d] flex flex-col max-h-[95vh] overflow-hidden">
        <!-- Header -->
        <div class="px-8 py-6 bg-[#00334d] text-white flex justify-between items-center shrink-0">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded bg-white text-[#00334d] flex items-center justify-center font-black text-lg">
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
                <p class="text-sm font-bold text-[#00334d]">{{ formatDate(request.pickup_date) }} @ {{ request.pickup_time || 'No time set' }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Academic Info</h3>
              <div class="flex flex-col gap-2">
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Graduation Year:</span> <span class="text-sm font-bold text-[#00334d]">{{ request.year_graduated }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Strand:</span> <span class="text-sm font-bold text-[#00334d]">{{ request.strand }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">LRN:</span> <span class="text-sm font-bold text-[#00334d]">{{ request.lrn_number || '—' }}</span></div>
              </div>
            </div>
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Contact Info</h3>
              <div class="flex flex-col gap-2">
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Email:</span> <span class="text-sm font-bold text-[#00334d] truncate max-w-[150px]">{{ request.email }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Phone:</span> <span class="text-sm font-bold text-[#00334d]">{{ request.phone_number }}</span></div>
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
                  <h4 class="text-sm font-bold text-[#00334d]">Accountability Clearance</h4>
                  <p class="text-[0.6rem] text-slate-500 italic uppercase">Verify student obligations</p>
               </div>
               <button @click="toggleAccountability" :class="['px-6 py-2 rounded-full text-[0.65rem] font-black uppercase transition-all border-2', request.no_accountabilities ? 'bg-green-500 border-green-600 text-white shadow-lg' : 'bg-white border-slate-300 text-slate-400 hover:border-red-400']">
                  {{ request.no_accountabilities ? 'Cleared' : 'Not Cleared' }}
               </button>
            </div>

            <div class="flex flex-col gap-4">
              <div class="bg-white border-2 border-[#00334d] rounded-xl p-6">
                <!-- Status Logic (Simplified for Component) -->
                 <div class="flex gap-2">
                    <button v-if="request.status === 'Pending' || request.status === 'Needs Verification'" @click="updateStatus('Approved')" class="flex-1 py-4 bg-[#10b981] text-white font-black uppercase rounded-lg shadow-md hover:bg-emerald-600">Approve</button>
                    <button v-if="request.status === 'Approved'" @click="updateStatus('Completed')" class="flex-1 py-4 bg-[#8b5cf6] text-white font-black uppercase rounded-lg shadow-md hover:bg-purple-600">Complete</button>
                    <button @click="updateStatus('Rejected')" class="px-6 py-4 bg-red-50 text-red-600 font-black uppercase rounded-lg border-2 border-red-200 hover:bg-red-100 transition-all">Reject</button>
                 </div>
                 <button v-if="request.status === 'Pending'" @click="updateStatus('Needs Verification')" class="w-full mt-2 py-2.5 bg-orange-500 text-white font-black uppercase rounded-lg shadow-md hover:bg-orange-600">Notify: Missing Record</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { adminService } from '@/services/api';
import { X as XIcon, Clock as ClockIcon } from 'lucide-vue-next';
import DocumentUploadRow from './DocumentUploadRow.vue';

const props = defineProps(['request']);
const emit = defineEmits(['close', 'refresh']);

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
  if (status === 'Completed' && !confirm('Mark as COMPLETED?')) return;
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
