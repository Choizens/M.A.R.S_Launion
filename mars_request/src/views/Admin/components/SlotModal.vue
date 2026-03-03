<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div class="bg-white w-full max-w-md rounded-lg shadow-2xl border-4 border-[#00334d] flex flex-col overflow-hidden">
        <div class="px-6 py-4 bg-[#00334d] text-white flex justify-between items-center">
          <h2 class="font-black uppercase tracking-widest text-sm">{{ editingId ? 'Edit Pickup Slot' : 'Add New Slot' }}</h2>
          <button @click="$emit('close')"><XIcon class="w-5 h-5" /></button>
        </div>
        <form @submit.prevent="$emit('submit')" class="p-6 flex flex-col gap-5">
          <div class="flex flex-col gap-1">
            <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Pickup Date</label>
            <input v-model="form.date" type="date" required class="border px-4 py-2.5 rounded focus:border-[#00334d] outline-none font-bold text-[#00334d]" />
          </div>
          
          <div class="grid grid-cols-3 gap-4">
            <div class="flex flex-col gap-1">
              <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Morning Max</label>
              <input v-model.number="form.morning_slots" type="number" required class="border px-4 py-2.5 text-sm rounded focus:border-[#00334d] outline-none font-bold text-[#00334d]" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Afternoon Max</label>
              <input v-model.number="form.afternoon_slots" type="number" required class="border px-4 py-2.5 text-sm rounded focus:border-[#00334d] outline-none font-bold text-[#00334d]" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider text-center">Block Date?</label>
              <div class="flex items-center justify-center h-full">
                 <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="form.is_blocked" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-red-500"></div>
                </label>
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Reason / Announcement (Optional)</label>
            <textarea v-model="form.reason" rows="2" placeholder="e.g. National Holiday, Staff Meeting..." class="border px-4 py-2.5 rounded focus:border-[#00334d] outline-none text-sm"></textarea>
          </div>

          <button type="submit" :disabled="submitting" class="mt-2 py-3.5 bg-[#ffca28] text-[#00334d] font-black uppercase tracking-widest rounded border-2 border-[#00334d] hover:bg-white transition-all shadow-md active:scale-95 disabled:opacity-50">
            {{ submitting ? 'Saving...' : (editingId ? 'Update Slot' : 'Create Pickup Slot') }}
          </button>
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
  submitting: Boolean
});

defineEmits(['close', 'submit']);
</script>
