<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div class="bg-white w-full max-w-md rounded-lg shadow-2xl border-4 border-[#103059] flex flex-col overflow-hidden">
        <div class="px-6 py-4 bg-[#103059] text-white flex justify-between items-center">
          <h2 class="font-black uppercase tracking-widest">{{ editingId ? 'Edit Staff' : 'Add New Staff' }}</h2>
          <button @click="$emit('close')"><XIcon class="w-5 h-5" /></button>
        </div>
        <form @submit.prevent="$emit('submit')" class="p-6 flex flex-col gap-4">
          <div class="flex flex-col gap-1">
            <label class="text-[0.6rem] font-bold uppercase text-slate-500">Full Name</label>
            <input v-model="form.full_name" type="text" required class="border px-4 py-2 rounded focus:border-[#103059] outline-none" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-[0.6rem] font-bold uppercase text-slate-500">Username</label>
            <input v-model="form.username" type="text" required class="border px-4 py-2 rounded focus:border-[#103059] outline-none" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-[0.6rem] font-bold uppercase text-slate-500">Email Address (for notifications)</label>
            <input v-model="form.email" type="email" required placeholder="e.g. staff@gmail.com" class="border px-4 py-2 rounded focus:border-[#103059] outline-none" />
          </div>
          <div v-if="!editingId" class="flex flex-col gap-1">
            <label class="text-[0.6rem] font-bold uppercase text-slate-500">Password</label>
            <input v-model="form.password" type="password" required class="border px-4 py-2 rounded focus:border-[#103059] outline-none" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-1">
              <label class="text-[0.6rem] font-bold uppercase text-slate-500">Staff ID</label>
              <input v-model="form.staff_id" type="text" required class="border px-4 py-2 rounded focus:border-[#103059] outline-none" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-[0.6rem] font-bold uppercase text-slate-500">Department</label>
              <input v-model="form.department" type="text" required class="border px-4 py-2 rounded focus:border-[#103059] outline-none" />
            </div>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-[0.6rem] font-bold uppercase text-slate-500">Account Type (Automatic)</label>
            <div class="px-4 py-2 bg-slate-50 border rounded font-bold text-[#103059]">
              {{ form.is_superuser ? 'Administrator' : 'Staff Member' }}
            </div>
          </div>
          <button type="submit" :disabled="submitting" class="mt-4 py-3 bg-[#ffca28] text-[#103059] font-black uppercase tracking-widest rounded border-2 border-[#103059] hover:bg-white transition-all">
            {{ submitting ? 'Processing...' : (editingId ? 'Update Account' : 'Create Account') }}
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
