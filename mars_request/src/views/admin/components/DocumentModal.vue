<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div class="bg-white w-full max-w-md rounded-lg shadow-2xl border-4 border-[#103059] flex flex-col overflow-hidden">
        <div class="px-6 py-4 bg-[#103059] text-white flex justify-between items-center">
          <h2 class="font-black uppercase tracking-widest text-sm text-white">{{ editingId ? 'Edit Document Type' : 'Add New Document' }}</h2>
          <button @click="$emit('close')" class="text-white hover:opacity-70"><XIcon class="w-5 h-5" /></button>
        </div>
        <form @submit.prevent="$emit('submit')" class="p-6 flex flex-col gap-5">
          <div class="flex flex-col gap-1">
            <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Document Name</label>
            <input v-model="form.name" type="text" required placeholder="e.g. Diploma, Good Moral, Cert..." class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold text-[#103059]" />
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Description (Optional)</label>
            <textarea v-model="form.description" rows="3" placeholder="Describe the document or requirements..." class="border px-4 py-2.5 rounded focus:border-[#103059] outline-none text-sm"></textarea>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-1">
              <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Fee (₱)</label>
              <div class="relative">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 font-bold text-slate-400">₱</span>
                <input v-model.number="form.price" type="number" step="0.01" required class="w-full border pl-8 pr-4 py-2.5 rounded focus:border-[#103059] outline-none font-bold text-[#103059]" />
              </div>
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider text-center">Active?</label>
              <div class="flex items-center justify-center h-full">
                 <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="form.is_active" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                </label>
              </div>
            </div>
          </div>

          <button type="submit" :disabled="submitting" class="mt-2 py-3.5 bg-[#ffca28] text-[#103059] font-black uppercase tracking-widest rounded border-2 border-[#103059] hover:bg-white transition-all shadow-md active:scale-95 disabled:opacity-50">
            {{ submitting ? 'Saving...' : (editingId ? 'Update Document' : 'Add Document Type') }}
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
