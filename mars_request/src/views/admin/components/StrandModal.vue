<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div class="bg-white w-full max-w-md rounded-lg shadow-2xl border-4 border-[#103059] flex flex-col overflow-hidden">
        <div class="px-6 py-4 bg-[#103059] text-white flex justify-between items-center">
          <h2 class="font-black uppercase tracking-widest">{{ editingId ? 'Edit Strand' : 'Add New Strand' }}</h2>
          <button @click="$emit('close')"><XIcon class="w-5 h-5" /></button>
        </div>
        <form @submit.prevent="$emit('submit')" class="p-6 flex flex-col gap-4">
          <div class="flex flex-col gap-1">
            <label class="text-[0.6rem] font-bold uppercase text-slate-500">Strand Name</label>
            <input v-model="form.name" type="text" required placeholder="e.g. STEM, ICT, ABM..." class="border px-4 py-2 rounded focus:border-[#103059] outline-none font-bold" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-[0.6rem] font-bold uppercase text-slate-500">Description</label>
            <textarea v-model="form.description" rows="3" placeholder="Brief description of the strand..." class="border px-4 py-2 rounded focus:border-[#103059] outline-none text-sm"></textarea>
          </div>
          <button type="submit" :disabled="submitting" class="mt-4 py-3 bg-[#ffca28] text-[#103059] font-black uppercase tracking-widest rounded border-2 border-[#103059] hover:bg-white transition-all shadow-md active:scale-95 disabled:opacity-50">
            {{ submitting ? 'Processing...' : (editingId ? 'Update Strand' : 'Add Strand') }}
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
