<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="$emit('close')">
      <div class="bg-white w-full max-w-2xl rounded-lg shadow-2xl border-4 border-[#00334d] flex flex-col max-h-[95vh] overflow-hidden">
        <!-- Modal Header -->
        <div class="px-8 py-6 bg-[#00334d] text-white flex justify-between items-center relative overflow-hidden">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded bg-white text-[#00334d] flex items-center justify-center font-black text-lg">
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
                <p class="text-sm font-bold text-[#00334d]">{{ formatDate(request.pickup_date) }} @ {{ request.pickup_time || 'No time set' }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Profile Information</h3>
              <div class="flex flex-col gap-2">
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Graduation Year:</span> <span class="text-sm font-bold text-[#00334d]">{{ request.year_graduated }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Strand:</span> <span class="text-sm font-bold text-[#00334d]">{{ request.strand }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">LRN:</span> <span class="text-sm font-bold text-[#00334d]">{{ request.lrn_number || '\u2014' }}</span></div>
              </div>
            </div>
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Contact Info</h3>
              <div class="flex flex-col gap-2">
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Email:</span> <span class="text-sm font-bold text-[#00334d]">{{ request.email }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Phone:</span> <span class="text-sm font-bold text-[#00334d]">{{ request.phone_number }}</span></div>
                <div class="flex justify-between items-center"><span class="text-xs font-bold text-slate-500">Date Applied:</span> <span class="text-sm font-bold text-[#00334d]">{{ formatDate(request.submitted_at) }}</span></div>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-4 mb-10">
            <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Requested Documents</h3>
            <div class="flex flex-col gap-3">
              <div v-for="f in request.requested_files" :key="f" 
                   class="p-4 bg-slate-50 border border-slate-200 rounded-lg">
                <div class="flex items-center justify-between mb-3 border-b border-dashed pb-2 border-slate-200">
                  <span class="text-[#00334d] font-black text-xs uppercase tracking-wider">{{ f }}</span>
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
                      <a :href="'http://127.0.0.1:8000' + request.documents.find(d => d.document_type === f).file" 
                         target="_blank"
                         class="inline-flex items-center gap-1.5 text-[0.6rem] font-bold text-amber-600 hover:text-amber-700 bg-white px-2 py-1 rounded border border-amber-200 shadow-sm">
                        <AttachmentIcon class="w-2.5 h-2.5" /> View Scan
                      </a>
                    </div>
                    <span v-else class="text-[0.55rem] font-bold text-slate-300 italic">None</span>
                  </div>

                  <!-- Master Record -->
                  <div>
                    <p class="text-[0.55rem] font-bold text-slate-400 uppercase mb-1">Database Record:</p>
                    <div v-if="request.student_record?.documents?.find(d => d.document_type === f)">
                      <a :href="'http://127.0.0.1:8000' + request.student_record.documents.find(d => d.document_type === f).file" 
                         target="_blank"
                         class="inline-flex items-center gap-1.5 text-[0.6rem] font-bold text-blue-600 hover:text-blue-700 bg-white px-2 py-1 rounded border border-blue-200 shadow-sm">
                        <FileIcon class="w-2.5 h-2.5" /> View Master
                      </a>
                    </div>
                    <span v-else class="text-[0.55rem] font-bold text-slate-300 italic">Not Found</span>
                  </div>

                  <!-- Processed/Ready Doc -->
                  <div>
                    <p class="text-[0.55rem] font-bold text-slate-400 uppercase mb-1">Ready Document:</p>
                    <div v-if="request.processed_documents?.find(d => d.document_type === f)">
                      <a :href="'http://127.0.0.1:8000' + request.processed_documents.find(d => d.document_type === f).file" 
                         target="_blank"
                         class="inline-flex items-center gap-1.5 text-[0.6rem] font-bold text-green-600 hover:text-green-700 bg-white px-2 py-1 rounded border border-green-200 shadow-sm">
                        <FileIcon class="w-2.5 h-2.5" /> Download
                      </a>
                    </div>
                    <span v-else class="text-[0.55rem] font-bold text-slate-300 italic">Not Uploaded</span>
                  </div>
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

            <div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <div class="w-8 h-8 bg-amber-400 rounded-full flex items-center justify-center shrink-0 text-white font-black text-sm">!</div>
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
import { X as XIcon, Clock as ClockIcon, Paperclip as AttachmentIcon, FileText as FileIcon, AlertCircle as AlertIcon } from 'lucide-vue-next';

defineProps({
  show: Boolean,
  request: Object,
  formatDate: Function,
  statusClass: Function
});

defineEmits(['close']);
</script>
