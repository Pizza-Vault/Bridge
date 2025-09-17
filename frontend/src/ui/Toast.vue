<template>
  <div
    class="fixed bottom-5 right-5 z-50 flex items-center gap-3 rounded-xl px-4 py-3 border border-white/10 shadow-xl"
    :class="bgClass"
    role="status"
  >
    <span class="w-2 h-2 rounded-full" :class="dotClass"></span>
    <span class="text-sm">{{ message }}</span>
    <button class="ml-2 btn btn-ghost px-2 py-1" @click="$emit('close')">Schließen</button>
  </div>
</template>

<script setup>
import { computed } from "vue";
const props = defineProps({
  type: { type:String, default:"success" },
  message: { type:String, default:"" }
});
const bgClass = computed(()=> props.type === "error"
  ? "bg-red-600/20 text-red-100"
  : "bg-emerald-600/20 text-emerald-100");
const dotClass = computed(()=> props.type === "error" ? "bg-red-400" : "bg-emerald-400");
</script>
