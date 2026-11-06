<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Plus, ExternalLink, Calendar, Clock } from 'lucide-vue-next'
import { formatIndonesianDate, formatIndonesianClock } from '../utils/dateFormatter'

defineProps({
  stats: {
    type: Object,
    default: () => ({ total: 0, completed: 0, completion_rate: 0 }),
  },
})

defineEmits(['open-create'])

// Live Indonesian Clock
const now = ref(new Date())
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    now.value = new Date()
  }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const currentDateStr = computed(() => formatIndonesianDate(now.value))
const currentClockStr = computed(() => formatIndonesianClock(now.value))
</script>

<template>
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs backdrop-blur-md bg-white/95">
    <!-- Top CIMB Red Brand Accent Line (Solid) -->
    <div class="h-1.5 w-full bg-cimb-800"></div>

    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 sm:h-20">
        
        <!-- Logo & Brand CIMB NIAGA -->
        <div class="flex items-center space-x-2.5 sm:space-x-3.5 min-w-0">
          <!-- CIMB Logo Emblem (Solid Red) -->
          <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-cimb-800 flex items-center justify-center text-white shadow-xs shrink-0">
            <svg class="w-5 h-5 sm:w-6 sm:h-6" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 17L12 4L20 17H4Z" fill="white" fill-opacity="0.2"/>
              <path d="M7 17.5L12 7.5L17 17.5H7Z" fill="white"/>
              <circle cx="12" cy="14" r="2" fill="#7E1322"/>
            </svg>
          </div>

          <!-- Brand Text & Subtitle -->
          <div class="min-w-0">
            <div class="flex items-center flex-wrap gap-1 sm:gap-1.5">
              <span class="text-base sm:text-xl font-extrabold tracking-tight text-cimb-800">CIMB</span>
              <span class="text-base sm:text-xl font-bold tracking-tight text-slate-800">NIAGA</span>
              <span class="hidden md:inline-block h-4 w-px bg-slate-300 mx-1"></span>
              <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-semibold bg-cimb-50 text-cimb-800 border border-cimb-200/80">
                Daily Task
              </span>
            </div>
            
            <!-- Desktop Info: Bank & Live Indonesian Time -->
            <p class="text-xs text-slate-500 hidden md:flex items-center gap-1.5 mt-0.5 font-medium">
              <span>PT Bank CIMB Niaga Tbk</span>
              <span>•</span>
              <Calendar class="w-3.5 h-3.5 text-slate-400" />
              <span>{{ currentDateStr }}</span>
              <span>•</span>
              <Clock class="w-3.5 h-3.5 text-cimb-700" />
              <span class="font-bold text-slate-700">{{ currentClockStr }}</span>
            </p>
          </div>
        </div>

        <!-- Right Actions -->
        <div class="flex items-center space-x-2 sm:space-x-3 shrink-0">
          <!-- API Docs Swagger Link (Desktop) -->
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            class="hidden lg:inline-flex items-center gap-1.5 px-3 py-2 text-xs font-semibold text-slate-600 hover:text-cimb-800 bg-slate-100 hover:bg-cimb-50 border border-slate-200/80 hover:border-cimb-200 rounded-xl transition-all"
            title="Buka Dokumentasi Interaktif Swagger FastAPI"
          >
            <span>Swagger API</span>
            <ExternalLink class="w-3.5 h-3.5 text-slate-400" />
          </a>

          <!-- Primary Action Button (CIMB Red) -->
          <button
            @click="$emit('open-create')"
            class="inline-flex items-center gap-1.5 sm:gap-2 px-3.5 sm:px-5 py-2 sm:py-2.5 bg-cimb-800 hover:bg-cimb-900 active:bg-cimb-950 text-white text-xs sm:text-sm font-semibold rounded-xl shadow-sm hover:shadow-md shadow-cimb-800/25 transition-all active:scale-[0.98]"
          >
            <Plus class="w-4 h-4 stroke-[2.8]" />
            <span class="hidden xs:inline">Tambah Tugas</span>
            <span class="xs:hidden">Tugas Baru</span>
          </button>
        </div>
      </div>

      <!-- Mobile Sub-Header: Live Indonesian Clock (Visible only on mobile/tablet) -->
      <div class="md:hidden py-1.5 px-1 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500 font-medium">
        <div class="flex items-center gap-1 truncate">
          <Calendar class="w-3 h-3 text-slate-400 shrink-0" />
          <span class="truncate">{{ currentDateStr }}</span>
        </div>
        <div class="flex items-center gap-1 font-bold text-cimb-800 bg-cimb-50/80 px-2 py-0.5 rounded-md border border-cimb-200/60 shrink-0">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <Clock class="w-3 h-3 text-cimb-700" />
          <span>{{ currentClockStr }}</span>
        </div>
      </div>

    </div>
  </header>
</template>
