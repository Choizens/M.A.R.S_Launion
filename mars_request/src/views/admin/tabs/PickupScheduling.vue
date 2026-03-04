<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex flex-col gap-2">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Pickup Scheduling</h1>
        <p class="text-slate-500 text-sm">Manage student pickup slots and holiday blockouts.</p>
      </div>
      <button @click="$emit('open-slot-modal')" class="px-6 py-2.5 bg-[#ffca28] text-[#0d324d] font-black rounded border-2 border-[#00334d] hover:bg-white transition-all shadow-md flex items-center gap-2">
        <component :is="ClockIcon" class="w-5 h-5" /> Add New Slot
      </button>
    </div>

    <!-- ══════════════════ CALENDAR SECTION ══════════════════ -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
      <!-- Calendar Visualizer -->
      <div class="xl:col-span-2 bg-white rounded-lg shadow-sm border border-[#e2e8f0] p-6 lg:p-8">
        <div class="flex items-center justify-between mb-8">
          <h3 class="font-black text-[#00334d] uppercase tracking-widest flex items-center gap-2">
            <component :is="DashboardIcon" class="w-5 h-5 text-amber-500" />
            {{ formatMonthLabel }}
          </h3>
          <div class="flex gap-2">
            <button @click="$emit('prev-month')" class="p-2 hover:bg-slate-100 rounded border transition-colors shadow-sm active:scale-95" title="Previous Month">
              <component :is="ChevronLeftIcon" class="w-5 h-5 text-[#00334d]" />
            </button>
            <button @click="$emit('next-month')" class="p-2 hover:bg-slate-100 rounded border transition-colors shadow-sm active:scale-95" title="Next Month">
              <component :is="ChevronRightIcon" class="w-5 h-5 text-[#00334d]" />
            </button>
          </div>
        </div>

        <div class="grid grid-cols-7 gap-2">
          <!-- Weekday Headers -->
          <div v-for="day in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']" :key="day" 
               class="text-center text-[0.65rem] font-black text-slate-400 uppercase pb-4">
            {{ day }}
          </div>
          
          <!-- Calendar Cells -->
          <div 
            v-for="(date, idx) in calendarDays" 
            :key="idx"
            @click="date.type === 'day' && !date.isWeekend && $emit('open-slot-modal', date.slot || { date: date.date })"
            :class="[
              'min-h-[90px] p-2 rounded-lg border-2 transition-all relative overflow-hidden flex flex-col',
              date.type === 'padding' ? 'bg-slate-50 border-transparent opacity-30 select-none' : 'group',
              date.type === 'day' && !date.isWeekend ? 'cursor-pointer' : 'cursor-not-allowed',
              date.isToday ? 'border-[#00334d]' : 'border-slate-100',
              date.type === 'day' && !date.isWeekend ? 'hover:border-amber-300' : '',
              date.isWeekend ? 'bg-slate-100/50' : (date.slot?.is_blocked ? 'bg-red-50/50' : 'bg-white')
            ]"
          >
            <div class="flex justify-between items-start">
              <span v-if="date.day" :class="['text-xs font-black', date.isToday ? 'text-white bg-[#00334d] px-1.5 py-0.5 rounded' : 'text-slate-400']">
                {{ date.day }}
              </span>
              <span v-if="date.isWeekend" class="text-[0.45rem] font-black uppercase text-slate-400 border border-slate-200 px-1 rounded bg-white">Closed</span>
              <span v-else-if="date.slot?.is_virtual" class="text-[0.45rem] font-black uppercase text-amber-500 border border-amber-100 px-1 rounded bg-amber-50">Default</span>
            </div>
            
            <div v-if="date.slot" class="mt-2 flex flex-col gap-1.5">
              <div v-if="date.slot.is_blocked" class="bg-red-500 text-white text-[0.5rem] font-black uppercase px-1.5 py-0.5 rounded leading-tight">
                Blocked
              </div>
              <div v-else class="flex flex-col gap-2">
                <!-- Morning Slots -->
                <div class="flex flex-col gap-0.5">
                  <div class="flex justify-between text-[0.45rem] font-bold text-slate-500 uppercase tracking-tighter">
                    <span>Morning</span><span>{{ date.slot.booked_morning || 0 }}/{{ date.slot.morning_slots }}</span>
                  </div>
                  <div class="w-full h-1 bg-slate-100 rounded-full">
                    <div class="h-full bg-amber-400 rounded-full" :style="{ width: ((date.slot.booked_morning || 0) / date.slot.morning_slots) * 100 + '%' }"></div>
                  </div>
                </div>
                <!-- Afternoon Slots -->
                <div class="flex flex-col gap-0.5">
                  <div class="flex justify-between text-[0.45rem] font-bold text-slate-500 uppercase tracking-tighter">
                    <span>Afternoon</span><span>{{ date.slot.booked_afternoon || 0 }}/{{ date.slot.afternoon_slots }}</span>
                  </div>
                  <div class="w-full h-1 bg-slate-100 rounded-full">
                    <div class="h-full bg-blue-400 rounded-full" :style="{ width: ((date.slot.booked_afternoon || 0) / date.slot.afternoon_slots) * 100 + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else-if="date.isWeekend" class="mt-auto pb-1 text-center">
               <p class="text-[0.5rem] font-bold text-slate-300 uppercase italic leading-tight">Office Closed</p>
            </div>
          </div>
        </div>

        <!-- Legend -->
        <div class="mt-8 flex flex-wrap gap-6 border-t pt-6">
          <div class="flex items-center gap-2 text-[0.65rem] font-bold text-slate-500 uppercase">
            <div class="w-3 h-3 rounded bg-white border-2 border-slate-200"></div> Available
          </div>
          <div class="flex items-center gap-2 text-[0.65rem] font-bold text-slate-500 uppercase">
            <div class="w-3 h-3 rounded bg-red-100 border-2 border-red-300"></div> Blocked / Holiday
          </div>
          <div class="flex items-center gap-2 text-[0.65rem] font-bold text-slate-500 uppercase">
            <div class="w-3 h-3 rounded bg-slate-100 border-2 border-slate-200"></div> Weekend / Closed
          </div>
          <div class="flex items-center gap-2 text-[0.65rem] font-bold text-slate-500 uppercase">
            <div class="w-3 h-3 rounded bg-white border-2 border-[#00334d]"></div> Today
          </div>
        </div>
      </div>

      <!-- List Side (Quick Reference) -->
      <div class="bg-white rounded-lg shadow-sm border border-[#e2e8f0] overflow-hidden flex flex-col">
        <div class="px-6 py-4 bg-slate-50 border-b">
           <h3 class="font-bold text-[#00334d] text-sm uppercase tracking-wide">Slot Records</h3>
        </div>
        <div class="overflow-y-auto max-h-[600px] flex-grow">
          <table class="w-full text-left text-sm">
            <thead class="sticky top-0 bg-slate-50 border-b font-bold text-slate-600 uppercase text-[0.6rem] tracking-widest z-10">
              <tr>
                <th class="px-6 py-3">Date</th>
                <th class="px-6 py-3 text-center">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y">
               <tr v-for="slot in pickupSlots" :key="slot.id" 
                   @click="$emit('open-slot-modal', slot)"
                   class="hover:bg-slate-50 cursor-pointer transition-colors group">
                 <td class="px-6 py-4">
                   <div class="flex flex-col">
                     <span class="font-bold text-[#00334d]">{{ formatDate(slot.date) }}</span>
                     <span class="text-[0.6rem] text-slate-400 font-bold uppercase">{{ (slot.booked_morning || 0) + (slot.booked_afternoon || 0) }} Booked Total</span>
                   </div>
                 </td>
                 <td class="px-6 py-4 text-center">
                    <span :class="[
                      'px-2 py-0.5 rounded-full text-[0.55rem] font-black uppercase tracking-widest border',
                      slot.is_blocked ? 'bg-red-50 text-red-500 border-red-100' : 'bg-green-50 text-green-500 border-green-100'
                    ]">
                      {{ slot.is_blocked ? 'Blocked' : 'Open' }}
                    </span>
                 </td>
               </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  Clock as ClockIcon, LayoutDashboard as DashboardIcon, 
  ChevronLeft as ChevronLeftIcon, ChevronRight as ChevronRightIcon 
} from 'lucide-vue-next';

defineProps({
  pickupSlots: Array,
  calendarDays: Array,
  formatMonthLabel: String,
  formatDate: Function
});

defineEmits(['open-slot-modal', 'prev-month', 'next-month']);
</script>
