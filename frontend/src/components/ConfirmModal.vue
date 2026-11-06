<script setup>
import { AlertTriangle, Loader2 } from 'lucide-vue-next'

defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: 'Hapus Tugas',
  },
  message: {
    type: String,
    default: 'Apakah Anda yakin ingin menghapus tugas ini? Tindakan ini tidak dapat dibatalkan.',
  },
  isDeleting: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['close', 'confirm'])
</script>

<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 overflow-y-auto bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4 transition-all"
    @click.self="$emit('close')"
  >
    <div class="relative bg-white rounded-2xl shadow-xl border border-slate-200/80 w-full max-w-md p-6 overflow-hidden transform transition-all animate-in fade-in zoom-in-95 duration-150">
      <div class="flex items-start gap-4">
        <div class="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center shrink-0">
          <AlertTriangle class="w-5 h-5 stroke-[2.2]" />
        </div>
        <div>
          <h3 class="text-base font-bold text-slate-900">{{ title }}</h3>
          <p class="text-xs sm:text-sm text-slate-500 mt-1.5 leading-relaxed">
            {{ message }}
          </p>
        </div>
      </div>

      <div class="mt-6 flex items-center justify-end gap-3">
        <button
          type="button"
          @click="$emit('close')"
          class="px-4 py-2 text-sm font-semibold text-slate-600 hover:bg-slate-100 rounded-xl transition-colors"
        >
          Batal
        </button>
        <button
          type="button"
          :disabled="isDeleting"
          @click="$emit('confirm')"
          class="inline-flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-sm font-semibold rounded-xl shadow-xs transition-all disabled:opacity-50"
        >
          <Loader2 v-if="isDeleting" class="w-4 h-4 animate-spin" />
          <span>Hapus Sekarang</span>
        </button>
      </div>
    </div>
  </div>
</template>

