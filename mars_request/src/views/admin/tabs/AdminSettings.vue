<template>
  <div class="flex flex-col gap-10">
    <div class="flex flex-col gap-2">
      <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Admin Settings</h1>
      <p class="text-slate-500 text-sm">Manage your profile and system preferences.</p>
    </div>

    <div class="max-w-2xl bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden">
      <div class="h-32 bg-[#103059] flex items-end px-8 pb-4 relative">
        <div class="absolute -bottom-10 left-8 w-24 h-24 bg-white rounded-full p-1 shadow-lg">
          <div class="w-full h-full bg-amber-400 rounded-full flex items-center justify-center text-[#103059] font-black text-3xl">
            {{ user?.full_name?.[0] || 'A' }}
          </div>
        </div>
      </div>
      
      <div class="pt-16 pb-12 px-8">
        <div class="flex justify-between items-start mb-10">
          <div class="flex flex-col gap-1">
            <h2 class="text-2xl font-black text-[#103059]">{{ user?.full_name || 'Administrator' }}</h2>
            <span class="text-amber-600 font-bold uppercase tracking-widest text-xs">System {{ user?.is_admin ? 'Supervisor' : 'Staff' }}</span>
          </div>
          <button class="px-6 py-2 border-2 border-[#103059] text-[#103059] font-black uppercase tracking-widest rounded-md text-xs hover:bg-[#103059] hover:text-white transition-all">Edit Profile</button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="flex flex-col gap-1.5">
            <span class="text-[0.65rem] font-bold text-slate-400 uppercase tracking-widest">Username</span>
            <span class="text-sm font-bold text-[#103059] px-4 py-2.5 bg-slate-50 rounded border">@{{ user?.username }}</span>
          </div>
          <div class="flex flex-col gap-1.5">
            <span class="text-[0.65rem] font-bold text-slate-400 uppercase tracking-widest">Staff Identification</span>
            <span class="text-sm font-bold text-[#103059] px-4 py-2.5 bg-slate-50 rounded border">{{ user?.staff_id }}</span>
          </div>
          <div class="flex flex-col gap-1.5">
            <span class="text-[0.65rem] font-bold text-slate-400 uppercase tracking-widest">Department</span>
            <span class="text-sm font-bold text-[#103059] px-4 py-2.5 bg-slate-50 rounded border">{{ user?.department || 'Administration' }}</span>
          </div>
          <div class="flex flex-col gap-1.5">
            <span class="text-[0.65rem] font-bold text-slate-400 uppercase tracking-widest">System Role</span>
            <span class="text-sm font-bold text-[#103059] px-4 py-2.5 bg-slate-50 rounded border">Super Administrator / Overseer</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  user: Object
});
</script>
