<template>
  <div class="flex flex-col gap-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex flex-col gap-1">
        <h1 class="text-2xl md:text-3xl font-extrabold text-[#333] tracking-tight">Pickup Scheduling</h1>
        <p class="text-slate-500 text-sm">Manage student pickup slots and holiday blockouts.</p>
      </div>
      <button
        @click="openSlotModal()"
        class="px-6 py-2.5 bg-[#ffca28] text-[#0d324d] font-black rounded border-2 border-[#00334d] hover:bg-white transition-all shadow-md flex items-center gap-2"
      >
        <ClockIcon class="w-5 h-5" /> Add New Slot
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-24">
      <div class="w-10 h-10 border-4 border-[#004d66] border-t-transparent rounded-full animate-spin"></div>
    </div>

    <div v-else class="grid grid-cols-1 xl:grid-cols-3 gap-8">
      <!-- Calendar Visualizer -->
      <div class="xl:col-span-2 bg-white rounded-lg shadow-sm border border-[#e2e8f0] p-6 lg:p-8">
        <div class="flex items-center justify-between mb-8">
          <h3 class="font-black text-[#00334d] uppercase tracking-widest flex items-center gap-2">
            <CalendarIcon class="w-5 h-5 text-amber-500" />
            {{ formatMonthLabel }}
          </h3>
          <div class="flex gap-2">
            <button @click="prevMonth" class="p-2 hover:bg-slate-100 rounded border transition-colors shadow-sm active:scale-95" title="Previous Month">
              <ChevronLeftIcon class="w-5 h-5 text-[#00334d]" />
            </button>
            <button @click="nextMonth" class="p-2 hover:bg-slate-100 rounded border transition-colors shadow-sm active:scale-95" title="Next Month">
              <ChevronRightIcon class="w-5 h-5 text-[#00334d]" />
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
            @click="date.type === 'day' && !date.isWeekend && openSlotModal(date.slot || { date: date.date })"
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
                <div class="flex flex-col gap-0.5">
                  <div class="flex justify-between text-[0.45rem] font-bold text-slate-500 uppercase tracking-tighter">
                    <span>Morning</span><span>{{ date.slot.booked_morning || 0 }}/{{ date.slot.morning_slots }}</span>
                  </div>
                  <div class="w-full h-1 bg-slate-100 rounded-full">
                    <div class="h-full bg-amber-400 rounded-full" :style="{ width: ((date.slot.booked_morning || 0) / date.slot.morning_slots) * 100 + '%' }"></div>
                  </div>
                </div>
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

      <!-- Slot Records List -->
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
              <tr v-if="pickupSlots.length === 0">
                <td colspan="2" class="px-6 py-8 text-center text-slate-400 text-xs">No slots configured yet.</td>
              </tr>
              <tr
                v-for="slot in pickupSlots"
                :key="slot.id"
                @click="openSlotModal(slot)"
                class="hover:bg-slate-50 cursor-pointer transition-colors"
              >
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

    <!-- Slot Modal -->
    <Teleport to="body">
      <div v-if="showSlotModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <div class="bg-white w-full max-w-md rounded-lg shadow-2xl border-4 border-[#00334d] flex flex-col overflow-hidden">
          <div class="px-6 py-4 bg-[#00334d] text-white flex justify-between items-center">
            <h2 class="font-black uppercase tracking-widest text-sm">{{ editingSlotId ? 'Edit Pickup Slot' : 'Add New Slot' }}</h2>
            <button @click="showSlotModal = false"><XIcon class="w-5 h-5" /></button>
          </div>
          <form @submit.prevent="handleSlotSubmit" class="p-6 flex flex-col gap-5">
            <div class="flex flex-col gap-1">
              <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Pickup Date</label>
              <input v-model="slotForm.date" type="date" required class="border px-4 py-2.5 rounded focus:border-[#00334d] outline-none font-bold text-[#00334d]" />
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div class="flex flex-col gap-1">
                <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Morning Max</label>
                <input v-model.number="slotForm.morning_slots" type="number" min="0" required class="border px-4 py-2.5 text-sm rounded focus:border-[#00334d] outline-none font-bold text-[#00334d]" />
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Afternoon Max</label>
                <input v-model.number="slotForm.afternoon_slots" type="number" min="0" required class="border px-4 py-2.5 text-sm rounded focus:border-[#00334d] outline-none font-bold text-[#00334d]" />
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider text-center">Block Date?</label>
                <div class="flex items-center justify-center h-full">
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="slotForm.is_blocked" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-red-500"></div>
                  </label>
                </div>
              </div>
            </div>

            <div class="flex flex-col gap-1">
              <label class="text-[0.65rem] font-black uppercase text-slate-500 tracking-wider">Reason / Announcement (Optional)</label>
              <textarea v-model="slotForm.reason" rows="2" placeholder="e.g. National Holiday, Staff Meeting..." class="border px-4 py-2.5 rounded focus:border-[#00334d] outline-none text-sm"></textarea>
            </div>

            <div v-if="editingSlotId" class="flex gap-3">
              <button type="submit" :disabled="submitting" class="flex-1 py-3.5 bg-[#ffca28] text-[#00334d] font-black uppercase tracking-widest rounded border-2 border-[#00334d] hover:bg-white transition-all shadow-md active:scale-95 disabled:opacity-50">
                {{ submitting ? 'Saving...' : 'Update Slot' }}
              </button>
              <button type="button" @click="deleteSlot(editingSlotId)" :disabled="submitting" class="px-4 py-3.5 bg-red-500 text-white font-black uppercase tracking-widest rounded border-2 border-red-600 hover:bg-red-600 transition-all shadow-md active:scale-95 disabled:opacity-50">
                Delete
              </button>
            </div>
            <button v-else type="submit" :disabled="submitting" class="py-3.5 bg-[#ffca28] text-[#00334d] font-black uppercase tracking-widest rounded border-2 border-[#00334d] hover:bg-white transition-all shadow-md active:scale-95 disabled:opacity-50">
              {{ submitting ? 'Saving...' : 'Create Pickup Slot' }}
            </button>
          </form>
        </div>
      </div>
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
  for (let i = 0; i < firstDay.getDay(); i++) {
    days.push({ date: null, type: 'padding' });
  }
  for (let d = 1; d <= lastDay.getDate(); d++) {
    const dateObj = new Date(year, month, d);
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    let slot = pickupSlots.value.find(s => s.date === dateStr);
    const dayOfWeek = dateObj.getDay();
    
    // If no slot in DB but it's a weekday, provide a virtual one for display
    if (!slot && dayOfWeek !== 0 && dayOfWeek !== 6) {
      slot = {
        date: dateStr,
        morning_slots: 5,
        afternoon_slots: 5,
        is_blocked: false,
        is_virtual: true, // Flag for UI
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
  return new Date(dt + 'T00:00:00').toLocaleDateString('en-PH', { year: 'numeric', month: 'short', day: 'numeric' });
};

// ── Data loading ──────────────────────────────────────────────────────────────
const loadSlots = async () => {
  loading.value = true;
  try {
    const res = await adminService.getSlots();
    pickupSlots.value = res.data;
  } catch (err) {
    console.error('Slots error:', err);
  } finally {
    loading.value = false;
  }
};

// ── Modal ─────────────────────────────────────────────────────────────────────
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
    alert('Error saving pickup slot. Please try again.');
    console.error(err);
  } finally {
    submitting.value = false;
  }
};

const deleteSlot = async (id) => {
  if (!confirm('Are you sure you want to delete this pickup slot?')) return;
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
