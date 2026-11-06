<script setup>
import { computed } from 'vue'
import {
  ListTodo,
  Clock,
  PlayCircle,
  CheckCircle2,
  AlertTriangle,
  Timer,
} from 'lucide-vue-next'

const props = defineProps({
  stats: {
    type: Object,
    default: () => ({
      total: 0,
      pending: 0,
      in_progress: 0,
      completed: 0,
      completed_on_time: 0,
      completed_late: 0,
      overdue: 0,
      completion_rate: 0,
    }),
  },
  activeStatus: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['filter-status', 'filter-overdue'])

// Calculated percentage for on-time and late completion
const onTimeRate = computed(() => {
  if (!props.stats.completed) return 0
  return Math.round((props.stats.completed_on_time / props.stats.completed) * 100)
})

const lateRate = computed(() => {
  if (!props.stats.completed) return 0
  return Math.round((props.stats.completed_late / props.stats.completed) * 100)
})
</script>

<template>
  <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5 sm:gap-3.5 mb-5 sm:mb-6">
    <!-- Card 1: Total Tugas (CIMB Burgundy Red Accent) -->
    <div
      @click="emit('filter-status', '')"
      :class="[
        'bg-white rounded-2xl p-3.5 sm:p-4 border shadow-xs transition-all cursor-pointer group active:scale-[0.98]',
        activeStatus === '' ? 'border-cimb-800 ring-2 ring-cimb-800/20 shadow-sm' : 'border-slate-200/80 hover:border-cimb-300'
      ]"
    >
      <div class="flex items-center justify-between">
        <span class="text-xs sm:text-sm font-semibold text-slate-500">Total Tugas</span>
        <div class="w-8 h-8 rounded-xl bg-slate-100 group-hover:bg-cimb-50 text-slate-600 group-hover:text-cimb-800 flex items-center justify-center transition-colors shrink-0">
          <ListTodo class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-2.5 flex items-baseline justify-between">
        <span class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">{{ stats.total }}</span>
        <span class="text-[11px] text-slate-400 font-medium">Semua</span>
      </div>
    </div>

    <!-- Card 2: Pending Tasks -->
    <div
      @click="emit('filter-status', 'pending')"
      :class="[
        'bg-white rounded-2xl p-3.5 sm:p-4 border shadow-xs transition-all cursor-pointer group active:scale-[0.98]',
        activeStatus === 'pending' ? 'border-amber-500 ring-2 ring-amber-500/20 shadow-sm' : 'border-slate-200/80 hover:border-amber-300'
      ]"
    >
      <div class="flex items-center justify-between">
        <span class="text-xs sm:text-sm font-semibold text-slate-500">Menunggu</span>
        <div class="w-8 h-8 rounded-xl bg-amber-50 text-amber-600 group-hover:bg-amber-100 flex items-center justify-center transition-colors shrink-0">
          <Clock class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-2.5 flex items-baseline justify-between">
        <span class="text-2xl sm:text-3xl font-extrabold text-amber-600 tracking-tight">{{ stats.pending }}</span>
        <span class="text-[11px] text-amber-600/70 font-semibold">Antrean</span>
      </div>
    </div>

    <!-- Card 3: In Progress Tasks -->
    <div
      @click="emit('filter-status', 'in_progress')"
      :class="[
        'bg-white rounded-2xl p-3.5 sm:p-4 border shadow-xs transition-all cursor-pointer group active:scale-[0.98]',
        activeStatus === 'in_progress' ? 'border-indigo-500 ring-2 ring-indigo-500/20 shadow-sm' : 'border-slate-200/80 hover:border-indigo-300'
      ]"
    >
      <div class="flex items-center justify-between">
        <span class="text-xs sm:text-sm font-semibold text-slate-500">Dikerjakan</span>
        <div class="w-8 h-8 rounded-xl bg-indigo-50 text-indigo-600 group-hover:bg-indigo-100 flex items-center justify-center transition-colors shrink-0">
          <PlayCircle class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-2.5 flex items-baseline justify-between">
        <span class="text-2xl sm:text-3xl font-extrabold text-indigo-600 tracking-tight">{{ stats.in_progress }}</span>
        <span class="text-[11px] text-indigo-600/70 font-semibold">Proses</span>
      </div>
    </div>

    <!-- Card 4: Selesai Tepat Waktu (On Time) -->
    <div
      @click="emit('filter-status', 'completed_on_time')"
      :class="[
        'bg-white rounded-2xl p-3.5 sm:p-4 border shadow-xs transition-all cursor-pointer group active:scale-[0.98]',
        activeStatus === 'completed_on_time' ? 'border-emerald-500 ring-2 ring-emerald-500/20 shadow-sm' : 'border-slate-200/80 hover:border-emerald-300'
      ]"
    >
      <div class="flex items-center justify-between">
        <span class="text-xs sm:text-sm font-semibold text-emerald-800">Tepat Waktu</span>
        <div class="w-8 h-8 rounded-xl bg-emerald-50 text-emerald-600 group-hover:bg-emerald-100 flex items-center justify-center transition-colors shrink-0">
          <CheckCircle2 class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-2.5 flex items-baseline justify-between">
        <span class="text-2xl sm:text-3xl font-extrabold text-emerald-600 tracking-tight">{{ stats.completed_on_time }}</span>
        <span class="text-[10px] sm:text-[11px] font-bold px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700">
          {{ onTimeRate }}%
        </span>
      </div>
      <!-- Mini Progress bar -->
      <div class="w-full bg-slate-100 rounded-full h-1 mt-2.5 overflow-hidden">
        <div
          class="bg-emerald-500 h-1 rounded-full transition-all duration-500"
          :style="{ width: `${onTimeRate}%` }"
        ></div>
      </div>
    </div>

    <!-- Card 5: Selesai Terlambat (Late) -->
    <div
      @click="emit('filter-status', 'completed_late')"
      :class="[
        'col-span-2 sm:col-span-1 bg-white rounded-2xl p-3.5 sm:p-4 border shadow-xs transition-all cursor-pointer group active:scale-[0.98]',
        activeStatus === 'completed_late' ? 'border-amber-500 ring-2 ring-amber-500/20 shadow-sm' : 'border-slate-200/80 hover:border-amber-300'
      ]"
    >
      <div class="flex items-center justify-between">
        <span class="text-xs sm:text-sm font-semibold text-amber-800">Selesai Terlambat</span>
        <div class="w-8 h-8 rounded-xl bg-amber-50 text-amber-600 group-hover:bg-amber-100 flex items-center justify-center transition-colors shrink-0">
          <Timer class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-2.5 flex items-baseline justify-between">
        <span class="text-2xl sm:text-3xl font-extrabold text-amber-600 tracking-tight">{{ stats.completed_late }}</span>
        <span class="text-[10px] sm:text-[11px] font-bold px-1.5 py-0.5 rounded bg-amber-50 text-amber-700">
          {{ lateRate }}%
        </span>
      </div>
      <!-- Mini Progress bar -->
      <div class="w-full bg-slate-100 rounded-full h-1 mt-2.5 overflow-hidden">
        <div
          class="bg-amber-500 h-1 rounded-full transition-all duration-500"
          :style="{ width: `${lateRate}%` }"
        ></div>
      </div>
    </div>
  </div>

  <!-- Overdue Banner (Visible if any uncompleted task is overdue) -->
  <div
    v-if="stats.overdue > 0"
    class="mb-5 sm:mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 px-4 py-3 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs sm:text-sm shadow-xs"
  >
    <div class="flex items-center gap-2.5">
      <AlertTriangle class="w-4 h-4 sm:w-5 sm:h-5 text-rose-600 shrink-0" />
      <span>
        Perhatian: Terdapat <strong>{{ stats.overdue }} tugas</strong> yang belum selesai dan telah melewati batas tenggat waktu!
      </span>
    </div>
    <button
      @click="emit('filter-overdue')"
      class="text-xs font-bold text-rose-700 hover:text-rose-900 underline underline-offset-2 self-start sm:self-auto shrink-0"
    >
      Lihat Tugas Terlambat →
    </button>
  </div>
</template>
