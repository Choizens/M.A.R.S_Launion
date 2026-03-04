<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex flex-col gap-2">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Student Directory</h1>
        <p class="text-slate-500 text-sm">Master database of all registered students.</p>
      </div>
      <button @click="$emit('open-student-modal')" class="px-6 py-2.5 bg-[#ffca28] text-[#0d324d] font-black rounded border-2 border-[#00334d] hover:bg-white transition-all shadow-md flex items-center gap-2">
        <component :is="StudentIcon" class="w-5 h-5" /> Add Master Record
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-[#e2e8f0] overflow-hidden">
      <div class="p-6 border-b border-slate-100 flex flex-col md:flex-row gap-4 items-center justify-between">
        <div class="relative w-full md:w-96">
          <input 
            :value="searchQuery" 
            @input="$emit('update:searchQuery', $event.target.value)"
            type="text" 
            placeholder="Search LRN, name or email..." 
            class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ffca28] font-medium" 
          />
          <SearchIcon class="absolute left-3 top-2.5 w-5 h-5 text-slate-400" />
        </div>
        <div class="flex gap-4">
          <select :value="strandFilter" @change="$emit('update:strandFilter', $event.target.value)" class="px-4 py-2 bg-white border border-slate-200 rounded text-xs font-bold uppercase outline-none">
            <option value="">All Strands</option>
            <option v-for="s in strands" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
          <select :value="yearFilter" @change="$emit('update:yearFilter', $event.target.value)" class="px-4 py-2 bg-white border border-slate-200 rounded text-xs font-bold uppercase outline-none">
            <option value="">All Batches</option>
            <option v-for="y in Array.from({length: 11}, (_, i) => 2020 + i)" :key="y" :value="y">{{ y }}</option>
          </select>
          
          <button 
            @click="$emit('update:missingDocsFilter', !missingDocsFilter)" 
            :class="missingDocsFilter ? 'bg-orange-100 text-orange-700 border-orange-300' : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50'"
            class="px-4 py-2 border rounded text-xs font-bold flex items-center gap-2 transition-colors"
          >
            <AlertIcon v-if="missingDocsFilter" class="w-4 h-4" />
            Missing Master Docs
          </button>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b-2 border-[#333]">
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest whitespace-nowrap">Student Name</th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest">LRN Number</th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest">Strand</th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest">Batch</th>
              <th class="px-6 py-4 text-[0.75rem] font-black text-slate-700 uppercase tracking-widest text-center">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200">
            <tr v-if="loadingStudents" class="p-20 text-center"><td colspan="5" class="py-20 italic text-slate-400">Loading student directory...</td></tr>
            <tr v-else-if="students.length === 0" class="p-20 text-center"><td colspan="5" class="py-20 italic text-slate-400">No student records found.</td></tr>
            <tr v-for="std in students" :key="std.id" class="hover:bg-slate-50 transition-colors">
              <td class="px-6 py-4 border-r border-slate-100">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-[#00334d] text-[#ffca28] flex items-center justify-center font-black text-xs">
                    {{ initials(std.first_name, std.last_name) }}
                  </div>
                  <div @click="$emit('open-profile', std)" class="flex flex-col cursor-pointer hover:underline group">
                    <div class="flex items-center gap-2">
                      <span class="font-bold text-[#00334d] group-hover:text-amber-600">{{ std.first_name }} {{ std.last_name }}</span>
                      <PaperclipIcon v-if="std.documents?.length > 0" class="w-3.5 h-3.5 text-amber-500" title="Has Scanned Documents" />
                    </div>
                    <span class="text-[0.65rem] text-slate-400 font-medium">{{ std.email }}</span>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm font-mono font-bold text-slate-600 border-r border-slate-100">{{ std.lrn_number }}</td>
              <td class="px-6 py-4 border-r border-slate-100">
                <span class="text-[0.7rem] font-black text-slate-500 uppercase tracking-tighter">{{ std.strand_display || 'N/A' }}</span>
              </td>
              <td class="px-6 py-4 text-sm font-black text-[#00334d] border-r border-slate-100">{{ std.year_graduated }}</td>
              <td class="px-6 py-4 text-center">
                <div class="flex items-center justify-center gap-3">
                  <button @click="$emit('open-profile', std)" class="px-4 py-1.5 bg-[#00334d] text-white font-bold text-xs rounded hover:bg-[#002233] transition-colors shadow-sm flex items-center gap-2">
                    <UserIcon class="w-3.5 h-3.5" /> View Profile
                  </button>
                  <button @click="$emit('delete-student', std.id)" class="p-1.5 text-red-500 hover:text-white hover:bg-red-500 rounded transition-colors shadow-sm border border-red-200 hover:border-red-500" title="Delete Record">
                    <XIcon class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  Search as SearchIcon, Users as StudentIcon, 
  Paperclip as PaperclipIcon, Settings as CogIcon, X as XIcon, UserCircle as UserIcon, AlertCircle as AlertIcon
} from 'lucide-vue-next';

defineProps({
  students: Array,
  loadingStudents: Boolean,
  searchQuery: String,
  strandFilter: [String, Number],
  yearFilter: [String, Number],
  missingDocsFilter: Boolean,
  strands: Array,
  initials: Function
});

defineEmits(['update:searchQuery', 'update:strandFilter', 'update:yearFilter', 'update:missingDocsFilter', 'open-student-modal', 'open-profile', 'delete-student']);
</script>
