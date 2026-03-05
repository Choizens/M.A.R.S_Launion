<template>
  <div class="flex flex-col gap-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex flex-col gap-1">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#103059] tracking-tight">Pickup Scheduling</h1>
        <p class="text-slate-500 text-sm font-medium italic">Manage student pickup slots and holiday blockouts.</p>
      </div>
      <button
        @click="openSlotModal()"
        class="px-6 py-2.5 bg-[#ffca28] text-[#103059] font-black rounded border-2 border-[#103059] hover:bg-white transition-all shadow-md flex items-center gap-2 active:scale-95"
      >
        <ClockIcon class="w-5 h-5" /> Add New Slot
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-24 bg-white/50 rounded-2xl border-2 border-dashed border-slate-200">
      <div class="flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-[#103059] border-t-transparent rounded-full animate-spin"></div>
        <span class="text-xs font-black text-[#103059] uppercase tracking-widest">Loading Schedule...</span>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 xl:grid-cols-3 gap-8">
      <!-- Calendar Visualizer -->
      <div class="xl:col-span-2 bg-white rounded-2xl shadow-sm border-2 border-slate-100 p-6 lg:p-8">
        <div class="flex items-center justify-between mb-8">
          <h3 class="font-black text-[#103059] uppercase tracking-widest flex items-center gap-3">
            <div class="p-2 bg-amber-100 rounded-lg">
                <CalendarIcon class="w-5 h-5 text-amber-600" />
            </div>
            <span class="text-lg">{{ formatMonthLabel }}</span>
          </h3>
          <div class="flex gap-2">
            <button @click="prevMonth" class="p-2.5 bg-slate-50 hover:bg-slate-100 rounded-xl border-2 border-slate-100 transition-all shadow-sm active:scale-95 group" title="Previous Month">
              <ChevronLeftIcon class="w-5 h-5 text-[#103059] group-hover:-translate-x-0.5 transition-transform" />
            </button>
            <button @click="nextMonth" class="p-2.5 bg-slate-50 hover:bg-slate-100 rounded-xl border-2 border-slate-100 transition-all shadow-sm active:scale-95 group" title="Next Month">
              <ChevronRightIcon class="w-5 h-5 text-[#103059] group-hover:translate-x-0.5 transition-transform" />
            </button>
          </div>
        </div>

        <div class="grid grid-cols-7 gap-3">
          <!-- Weekday Headers -->
          <div v-for="day in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']" :key="day"
               class="text-center text-[0.7rem] font-black text-slate-400 uppercase pb-4 tracking-tighter">
            {{ day }}
          </div>

          <!-- Calendar Cells -->
          <div
            v-for="(date, idx) in calendarDays"
            :key="idx"
            @click="date.type === 'day' && !date.isWeekend && openSlotModal(date.slot || { date: date.date })"
            :class="[
              'min-h-[110px] p-3 rounded-2xl border-2 transition-all relative overflow-hidden flex flex-col group',
              date.type === 'padding' ? 'bg-slate-50 border-transparent opacity-30 select-none' : '',
              date.type === 'day' && !date.isWeekend ? 'cursor-pointer hover:shadow-lg hover:-translate-y-1' : 'cursor-not-allowed',
              date.isToday ? 'border-[#103059] shadow-md bg-white' : 'border-slate-50 bg-white shadow-sm',
              date.type === 'day' && !date.isWeekend ? 'hover:border-amber-400' : '',
              date.isWeekend ? 'bg-slate-50/80 opacity-60' : (date.slot?.is_blocked ? 'bg-red-50/50' : 'bg-white')
            ]"
          >
            <div class="flex justify-between items-start mb-auto">
              <span v-if="date.day" :class="[
                'text-sm font-black w-7 h-7 flex items-center justify-center rounded-lg transition-colors', 
                date.isToday ? 'text-white bg-[#103059]' : 'text-slate-400 group-hover:text-[#103059]'
              ]">
                {{ date.day }}
              </span>
              <span v-if="date.isWeekend" class="text-[0.5rem] font-black uppercase text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded-md border border-slate-200">Closed</span>
              <span v-else-if="date.slot?.is_virtual" class="text-[0.5rem] font-black uppercase text-amber-500 bg-amber-50 px-1.5 py-0.5 rounded-md border border-amber-100">Default</span>
            </div>

            <div v-if="date.slot" class="mt-4 flex flex-col gap-2 relative z-10">
              <div v-if="date.slot.is_blocked" class="bg-red-500 text-white text-[0.55rem] font-black uppercase px-2 py-1 rounded-lg leading-tight shadow-sm text-center">
                Blocked
              </div>
              <div v-else class="flex flex-col gap-2.5">
                <!-- Morning Slot UI -->
                <div class="flex flex-col gap-1">
                  <div class="flex justify-between text-[0.5rem] font-black text-slate-500 uppercase tracking-tighter">
                    <span>Morning</span>
                    <span :class="{'text-red-500': date.slot.booked_morning >= date.slot.morning_slots}">
                        {{ date.slot.booked_morning || 0 }}/{{ date.slot.morning_slots }}
                    </span>
                  </div>
                  <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div 
                        class="h-full bg-amber-400 transition-all duration-500" 
                        :style="{ width: Math.min(100, ((date.slot.booked_morning || 0) / date.slot.morning_slots) * 100) + '%' }"
                    ></div>
                  </div>
                </div>
                <!-- Afternoon Slot UI -->
                <div class="flex flex-col gap-1">
                  <div class="flex justify-between text-[0.5rem] font-black text-slate-500 uppercase tracking-tighter">
                    <span>Afternoon</span>
                    <span :class="{'text-red-500': date.slot.booked_afternoon >= date.slot.afternoon_slots}">
                        {{ date.slot.booked_afternoon || 0 }}/{{ date.slot.afternoon_slots }}
                    </span>
                  </div>
                  <div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div 
                        class="h-full bg-[#103059] transition-all duration-500" 
                        :style="{ width: Math.min(100, ((date.slot.booked_afternoon || 0) / date.slot.afternoon_slots) * 100) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else-if="date.isWeekend" class="mt-auto pb-1 text-center">
              <p class="text-[0.45rem] font-black text-slate-300 uppercase italic tracking-widest">Office Closed</p>
            </div>
            
            <!-- Hover Decoration -->
            <div v-if="!date.isWeekend && date.type === 'day'" class="absolute -right-2 -bottom-2 opacity-0 group-hover:opacity-10 transition-all">
                <ClockIcon class="w-12 h-12 text-[#103059]" />
            </div>
          </div>
        </div>

        <!-- Legend -->
        <div class="mt-8 flex flex-wrap gap-6 border-t border-slate-100 pt-6">
          <div class="flex items-center gap-3 text-[0.65rem] font-black text-slate-500 uppercase tracking-wider">
            <div class="w-4 h-4 rounded-md bg-white border-2 border-slate-200"></div> Available
          </div>
          <div class="flex items-center gap-3 text-[0.65rem] font-black text-slate-500 uppercase tracking-wider">
            <div class="w-4 h-4 rounded-md bg-red-50 border-2 border-red-200"></div> Blocked
          </div>
          <div class="flex items-center gap-3 text-[0.65rem] font-black text-slate-500 uppercase tracking-wider">
            <div class="w-4 h-4 rounded-md bg-slate-50 border-2 border-slate-200 opacity-60"></div> Closed
          </div>
          <div class="flex items-center gap-3 text-[0.65rem] font-black text-slate-500 uppercase tracking-wider">
            <div class="w-4 h-4 rounded-md bg-white border-2 border-[#103059]"></div> Today
          </div>
        </div>
      </div>

      <!-- Slot Records List Side Panel -->
      <div class="bg-white rounded-2xl shadow-sm border-2 border-slate-100 overflow-hidden flex flex-col">
        <div class="px-6 py-4 bg-slate-50 border-b-2 border-slate-100 flex items-center justify-between">
          <h3 class="font-black text-[#103059] text-xs uppercase tracking-widest">Record History</h3>
          <span class="bg-[#103059] text-white text-[0.6rem] font-black px-2 py-0.5 rounded-full">{{ pickupSlots.length }}</span>
        </div>
        <div class="overflow-y-auto max-h-[700px] flex-grow custom-scrollbar">
          <table class="w-full text-left">
            <thead class="sticky top-0 bg-slate-50 border-b font-black text-slate-400 uppercase text-[0.6rem] tracking-widest z-10">
              <tr>
                <th class="px-6 py-3">Pickup Date</th>
                <th class="px-6 py-3 text-center">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50 font-sans">
              <tr v-if="pickupSlots.length === 0">
                <td colspan="2" class="px-6 py-12 text-center text-slate-400 text-[0.7rem] font-bold uppercase italic tracking-widest bg-slate-50/30">No custom slots configured</td>
              </tr>
              <tr
                v-for="slot in pickupSlots"
                :key="slot.id"
                @click="openSlotModal(slot)"
                class="hover:bg-slate-50 cursor-pointer transition-colors group border-transparent hover:border-l-[#ffca28] border-l-4"
              >
                <td class="px-6 py-4">
                  <div class="flex flex-col gap-0.5">
                    <span class="font-bold text-[#103059] text-sm">{{ formatDate(slot.date) }}</span>
                    <span class="text-[0.6rem] text-slate-400 font-black uppercase tracking-tighter">
                        {{ (slot.booked_morning || 0) + (slot.booked_afternoon || 0) }} / {{ slot.morning_slots + slot.afternoon_slots }} Total Capacity
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 text-center">
                  <span :class="[
                    'px-2.5 py-1 rounded-lg text-[0.6rem] font-black uppercase tracking-widest border shadow-sm',
                    slot.is_blocked ? 'bg-red-50 text-red-500 border-red-100' : 'bg-green-50 text-green-600 border-green-100'
                  ]">
                    {{ slot.is_blocked ? 'Blocked' : 'Active' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Enhanced Slot Modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showSlotModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-[#103059]/40 backdrop-blur-sm" @click="showSlotModal = false"></div>
          
          <div class="bg-white w-full max-w-md rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.3)] border-4 border-[#103059] flex flex-col overflow-hidden relative z-10 animate-scale-up">
            <div class="px-8 py-6 bg-[#103059] text-white flex justify-between items-center">
              <div class="flex items-center gap-3">
                <div class="p-2 bg-white/10 rounded-xl">
                    <ClockIcon class="w-5 h-5 text-amber-300" />
                </div>
                <h2 class="font-black uppercase tracking-widest text-sm italic">{{ editingSlotId ? 'Modify Pickup Slot' : 'Initialize New Slot' }}</h2>
              </div>
              <button @click="showSlotModal = false" class="hover:rotate-90 transition-transform duration-300 bg-white/10 p-1.5 rounded-lg"><XIcon class="w-5 h-5" /></button>
            </div>

            <form @submit.prevent="handleSlotSubmit" class="p-8 flex flex-col gap-6">
              <div class="flex flex-col gap-2">
                <label class="text-[0.7rem] font-black uppercase text-slate-500 tracking-widest ml-1">Proposed Pickup Date</label>
                <div class="relative">
                    <input v-model="slotForm.date" type="date" required class="w-full border-2 border-slate-100 px-5 py-3 rounded-2xl focus:border-[#103059] outline-none font-black text-[#103059] bg-slate-50 text-base" />
                </div>
              </div>

              <div class="grid grid-cols-2 gap-6">
                <div class="flex flex-col gap-2">
                  <label class="text-[0.7rem] font-black uppercase text-slate-500 tracking-widest ml-1">Morning Limit</label>
                  <input v-model.number="slotForm.morning_slots" type="number" min="0" required class="w-full border-2 border-slate-100 px-5 py-3 text-base rounded-2xl focus:border-[#103059] outline-none font-black text-[#103059] bg-slate-50 shadow-inner" />
                </div>
                <div class="flex flex-col gap-2">
                  <label class="text-[0.7rem] font-black uppercase text-slate-500 tracking-widest ml-1">Afternoon Limit</label>
                  <input v-model.number="slotForm.afternoon_slots" type="number" min="0" required class="w-full border-2 border-slate-100 px-5 py-3 text-base rounded-2xl focus:border-[#103059] outline-none font-black text-[#103059] bg-slate-50 shadow-inner" />
                </div>
              </div>

              <div class="p-5 bg-slate-50 rounded-2xl border-2 border-slate-100 flex items-center justify-between group">
                <div class="flex flex-col">
                    <label class="text-[0.7rem] font-black uppercase text-[#103059] tracking-widest">Block Availability?</label>
                    <span class="text-[0.6rem] text-slate-400 font-bold">Prevent any requests for this date</span>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="slotForm.is_blocked" class="sr-only peer">
                  <div class="w-14 h-7 bg-slate-200 peer-focus:ring-4 peer-focus:ring-[#103059]/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[4px] after:left-[4px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-red-500 shadow-inner"></div>
                </label>
              </div>

              <div class="flex flex-col gap-2">
                <label class="text-[0.7rem] font-black uppercase text-slate-500 tracking-widest ml-1">Notification Context</label>
                <textarea v-model="slotForm.reason" rows="3" placeholder="Explain the block or specific instructions for this date..." class="w-full border-2 border-slate-100 px-5 py-3 rounded-2xl focus:border-[#103059] outline-none text-sm font-semibold text-slate-700 bg-slate-50 placeholder:italic placeholder:opacity-50"></textarea>
              </div>

              <div v-if="editingSlotId" class="flex gap-4 pt-4">
                <button type="submit" :disabled="submitting" class="flex-[3] py-4 bg-[#ffca28] text-[#103059] font-black uppercase tracking-widest rounded-2xl border-2 border-[#103059] hover:bg-white hover:shadow-xl transition-all active:scale-95 disabled:opacity-50 text-sm shadow-md">
                  {{ submitting ? 'Updating...' : 'Save Configuration' }}
                </button>
                <button type="button" @click="deleteSlot(editingSlotId)" :disabled="submitting" class="flex-1 py-4 bg-red-50 text-red-500 font-black uppercase tracking-widest rounded-2xl border-2 border-red-100 hover:bg-red-500 hover:text-white transition-all active:scale-95 disabled:opacity-50 flex items-center justify-center">
                  <XIcon class="w-5 h-5" />
                </button>
              </div>
              <button v-else type="submit" :disabled="submitting" class="py-4 bg-[#ffca28] text-[#103059] font-black uppercase tracking-widest rounded-2xl border-2 border-[#103059] hover:bg-white hover:shadow-xl transition-all active:scale-95 disabled:opacity-50 text-sm shadow-md mt-4">
                {{ submitting ? 'initializing...' : 'Activate Pickup Slot' }}
              </button>
            </form>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import {
  Clock as ClockIcon, Calendar as CalendarIcon,
  ChevronLeft as ChevronLeftIcon, ChevronRight as ChevronRightIcon,
  X as XIcon
} from 'lucide-vue-next';
import { adminService } from '@/services/api';

// ── State ────────────────────────────────────────────────────────────────────
const pickupSlots = ref([]);
const loading = ref(false);
const showSlotModal = ref(false);
const editingSlotId = ref(null);
const submitting = ref(false);
const currentMonth = ref(new Date());

const slotForm = reactive({
  date: '',
  morning_slots: 5,
  afternoon_slots: 5,
  is_blocked: false,
  reason: ''
});

// ── Calendar ─────────────────────────────────────────────────────────────────
const calendarDays = computed(() => {
  const year = currentMonth.value.getFullYear();
  const month = currentMonth.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const days = [];
  
  // Padding for start of month
  for (let i = 0; i < firstDay.getDay(); i++) {
    days.push({ date: null, type: 'padding' });
  }
  
  for (let d = 1; d <= lastDay.getDate(); d++) {
    const dateObj = new Date(year, month, d);
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    let slot = pickupSlots.value.find(s => s.date === dateStr);
    const dayOfWeek = dateObj.getDay();
    
    // Virtual slots for weekdays if not in DB
    if (!slot && dayOfWeek !== 0 && dayOfWeek !== 6) {
      slot = {
        date: dateStr,
        morning_slots: 5,
        afternoon_slots: 5,
        is_blocked: false,
        is_virtual: true,
        booked_morning: 0, 
        booked_afternoon: 0
      };
    }

    days.push({
      day: d, date: dateStr, type: 'day',
      isToday: new Date().toDateString() === dateObj.toDateString(),
      isWeekend: dayOfWeek === 0 || dayOfWeek === 6,
      slot
    });
  }
  return days;
});

const formatMonthLabel = computed(() =>
  currentMonth.value.toLocaleDateString('en-PH', { month: 'long', year: 'numeric' })
);

const prevMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1, 1);
};
const nextMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1, 1);
};

// ── Helpers ───────────────────────────────────────────────────────────────────
const formatDate = (dt) => {
  if (!dt) return '—';
  // Standardize browser date handling
  return new Date(dt + 'T00:00:00').toLocaleDateString('en-PH', { year: 'numeric', month: 'short', day: 'numeric' });
};

// ── Data loading ──────────────────────────────────────────────────────────────
const loadSlots = async () => {
  loading.value = true;
  try {
    const res = await adminService.getSlots();
    pickupSlots.value = res.data || [];
  } catch (err) {
    console.error('Slots error:', err);
  } finally {
    loading.value = false;
  }
};

// ── Modal Handlers ─────────────────────────────────────────────────────────────
const openSlotModal = (slot = null) => {
  if (slot && slot.id) {
    editingSlotId.value = slot.id;
    slotForm.date = slot.date;
    slotForm.morning_slots = slot.morning_slots;
    slotForm.afternoon_slots = slot.afternoon_slots;
    slotForm.is_blocked = slot.is_blocked;
    slotForm.reason = slot.reason || '';
  } else {
    editingSlotId.value = null;
    slotForm.date = slot?.date || '';
    slotForm.morning_slots = 5;
    slotForm.afternoon_slots = 5;
    slotForm.is_blocked = false;
    slotForm.reason = '';
  }
  showSlotModal.value = true;
};

const handleSlotSubmit = async () => {
  submitting.value = true;
  try {
    if (editingSlotId.value) {
      await adminService.updateSlot(editingSlotId.value, slotForm);
    } else {
      await adminService.createSlot(slotForm);
    }
    showSlotModal.value = false;
    await loadSlots();
  } catch (err) {
    const errorMsg = err.response?.data ? Object.values(err.response.data).flat().join(' ') : 'Failed to save pickup slot. Check your connection and try again.';
    alert(errorMsg);
    console.error(err);
  } finally {
    submitting.value = false;
  }
};

const deleteSlot = async (id) => {
  if (!confirm('Permanently remove this pickup slot? Existing bookings will not be deleted but new ones will use default settings.')) return;
  submitting.value = true;
  try {
    await adminService.deleteSlot(id);
    showSlotModal.value = false;
    await loadSlots();
  } catch (err) {
    alert('Failed to delete slot.');
  } finally {
    submitting.value = false;
  }
};

onMounted(loadSlots);
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #cbd5e1; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.animate-scale-up { animation: scaleUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes scaleUp {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>
