<template>
  <span 
    :class="[
      'px-3 py-1 rounded-full text-[0.65rem] font-black uppercase tracking-wider',
      statusClass
    ]"
  >
    <slot>{{ status }}</slot>
  </span>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  status: { type: String, required: true }
});

const statusClass = computed(() => {
  const s = props.status;
  return {
    'bg-amber-100 text-amber-600 border border-amber-200': s === 'Pending',
    'bg-orange-100 text-orange-600 border border-orange-200': s === 'Needs Verification',
    'bg-green-100 text-green-600 border border-green-200': s === 'Approved',
    'bg-purple-100 text-purple-600 border border-purple-200': s === 'Completed',
    'bg-red-100 text-red-600 border border-red-200': s === 'Rejected',
  };
});
</script>
