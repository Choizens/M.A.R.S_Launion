<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div class="bg-white w-full max-w-4xl rounded-lg shadow-2xl border-4 border-[#103059] flex flex-col max-h-[95vh] overflow-hidden">
        <div class="px-6 py-4 bg-[#103059] text-white flex justify-between items-center">
          <h2 class="font-black uppercase tracking-widest text-sm text-white">{{ editingId ? 'Edit Student Record' : 'Add Master Record' }}</h2>
          <button @click="$emit('close')" class="text-white hover:opacity-70"><XIcon class="w-5 h-5" /></button>
        </div>
        <form @submit.prevent="$emit('submit')" class="p-8 overflow-y-auto flex flex-col gap-8">
          <!-- Form Sections -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Identity -->
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Personal Identity</h3>
              <div class="flex flex-col gap-1">
                <label class="text-[0.6rem] font-black uppercase text-slate-500">LRN Number</label>
                <input v-model="form.lrn_number" type="text" required placeholder="12-digit Learner Reference Number" class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold text-[#103059]" />
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div class="flex flex-col gap-1">
                  <label class="text-[0.6rem] font-black uppercase text-slate-500">First Name</label>
                  <input v-model="form.first_name" type="text" required class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-[0.6rem] font-black uppercase text-slate-500">Last Name</label>
                  <input v-model="form.last_name" type="text" required class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold" />
                </div>
              </div>
              <div class="grid grid-cols-3 gap-3">
                <div class="flex flex-col gap-1">
                  <label class="text-[0.6rem] font-black uppercase text-slate-500">Middle Name</label>
                  <input v-model="form.middle_name" type="text" class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-[0.6rem] font-black uppercase text-slate-500">Suffix</label>
                  <input v-model="form.suffix" type="text" placeholder="Jr., III..." class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-[0.6rem] font-black uppercase text-slate-500">Sex</label>
                  <select v-model="form.sex" required class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold">
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Academic -->
            <div class="flex flex-col gap-4">
              <h3 class="text-[0.7rem] font-black text-slate-400 uppercase tracking-widest border-b pb-1">Academic Info</h3>
              <div class="flex flex-col gap-1">
                <label class="text-[0.6rem] font-black uppercase text-slate-500">Year Graduated</label>
                <select v-model="form.year_graduated" required class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold">
                  <option v-for="y in Array.from({length: 11}, (_, i) => 2020 + i)" :key="y" :value="y">{{ y }}</option>
                </select>
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-[0.6rem] font-black uppercase text-slate-500">Strand Type</label>
                <select v-model="form.strand_type" required class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold">
                  <option v-for="s in strands" :key="s.id" :value="s.id">{{ s.name }}</option>
                </select>
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-[0.6rem] font-black uppercase text-slate-500">Email Address</label>
                <input v-model="form.email" type="email" required class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold" />
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-[0.6rem] font-black uppercase text-slate-500">Phone Number</label>
                <input v-model="form.phone_number" type="text" required class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold" />
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-[0.6rem] font-black uppercase text-slate-500">Permanent Address</label>
            <textarea v-model="form.permanent_address" rows="2" required class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none text-sm"></textarea>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t">
             <button type="button" @click="$emit('close')" class="px-8 py-3 font-bold uppercase text-slate-500 hover:text-[#103059] transition-colors">Cancel</button>
             <button type="submit" :disabled="submitting" class="px-12 py-3 bg-[#ffca28] text-[#103059] font-black uppercase tracking-widest rounded border-2 border-[#103059] hover:bg-white transition-all shadow-md active:scale-95 disabled:opacity-50">
              {{ submitting ? 'Processing...' : (editingId ? 'Update Master Record' : 'Create Master Record') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { X as XIcon } from 'lucide-vue-next';

defineProps({
  show: Boolean,
  editingId: [Number, String, null],
  form: Object,
  submitting: Boolean,
  strands: Array
});

defineEmits(['close', 'submit']);
</script>
