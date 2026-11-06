<script setup>
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-vue-next'

defineProps({
  toasts: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['remove'])
</script>

<template>
  <div class="fixed bottom-4 inset-x-3 sm:inset-x-auto sm:right-5 sm:bottom-5 z-50 flex flex-col gap-2 max-w-sm sm:w-full pointer-events-none">
    <transition-group
      enter-active-class="transform ease-out duration-300 transition"
      enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
      enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'pointer-events-auto flex items-center justify-between p-4 rounded-xl border shadow-lg backdrop-blur-md',
          toast.type === 'success'
            ? 'bg-emerald-50/95 border-emerald-200 text-emerald-900'
            : toast.type === 'error'
            ? 'bg-rose-50/95 border-rose-200 text-rose-900'
            : 'bg-blue-50/95 border-blue-200 text-blue-900'
        ]"
      >
        <div class="flex items-center gap-3">
          <CheckCircle2 v-if="toast.type === 'success'" class="w-5 h-5 text-emerald-600 shrink-0" />
          <AlertCircle v-else-if="toast.type === 'error'" class="w-5 h-5 text-rose-600 shrink-0" />
          <Info v-else class="w-5 h-5 text-blue-600 shrink-0" />
          <p class="text-xs sm:text-sm font-medium">{{ toast.message }}</p>
        </div>
        <button
          @click="$emit('remove', toast.id)"
          class="ml-3 text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-black/5 transition-colors"
        >
          <X class="w-4 h-4" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

