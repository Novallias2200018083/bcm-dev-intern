<script setup>
import { computed } from 'vue'
import {
  Calendar,
  CheckCircle2,
  AlertCircle,
  Pencil,
  Trash2,
  Tag,
  Paperclip,
  Eye,
  ChevronDown,
} from 'lucide-vue-next'
import { formatIndonesianDateTime, parseLocalDate } from '../utils/dateFormatter'

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['toggle-status', 'change-status', 'edit', 'delete', 'view'])

// Determine if task is overdue
const isOverdue = computed(() => {
  if (!props.task.due_date || props.task.status === 'completed') return false
  const due = parseLocalDate(props.task.due_date)
  return due ? due < new Date() : false
})

// Determine if completed late or on time
const isCompletedLate = computed(() => {
  if (props.task.status !== 'completed' || !props.task.due_date || !props.task.completed_at) return false
  const due = parseLocalDate(props.task.due_date)
  const completed = parseLocalDate(props.task.completed_at)
  return due && completed ? completed > due : false
})

// Format due date in Indonesian with WIB
const formattedDueDate = computed(() => {
  if (!props.task.due_date) return null
  return formatIndonesianDateTime(props.task.due_date, true)
})

// Format completed date
const formattedCompletedDate = computed(() => {
  if (!props.task.completed_at) return null
  return formatIndonesianDateTime(props.task.completed_at, true)
})

const priorityBadge = computed(() => {
  switch (props.task.priority) {
    case 'high':
      return {
        text: 'Tinggi',
        classes: 'bg-rose-50 text-rose-700 border-rose-200/80',
      }
    case 'medium':
      return {
        text: 'Sedang',
        classes: 'bg-amber-50 text-amber-700 border-amber-200/80',
      }
    case 'low':
      return {
        text: 'Rendah',
        classes: 'bg-slate-100 text-slate-600 border-slate-200/80',
      }
    default:
      return {
        text: props.task.priority,
        classes: 'bg-slate-100 text-slate-600 border-slate-200',
      }
  }
})

// Status styling for the interactive pill selector
const statusBadge = computed(() => {
  if (props.task.status === 'completed') {
    if (isCompletedLate.value) {
      return {
        label: 'Selesai (Terlambat)',
        classes: 'bg-amber-50 text-amber-800 border-amber-300 hover:bg-amber-100/80',
      }
    }
    return {
      label: 'Selesai (Tepat Waktu)',
      classes: 'bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100/80',
    }
  }

  if (props.task.status === 'in_progress') {
    return {
      label: 'Dikerjakan',
      classes: 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100/80',
    }
  }

  if (isOverdue.value) {
    return {
      label: 'Lewat Deadline',
      classes: 'bg-rose-50 text-rose-700 border-rose-300 hover:bg-rose-100/80',
    }
  }

  return {
    label: 'Menunggu',
    classes: 'bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200/70',
  }
})
</script>

<template>
  <div
    :class="[
      'bg-white rounded-2xl border transition-all duration-200 flex flex-col justify-between p-4 sm:p-5 relative group shadow-xs hover:shadow-md',
      task.status === 'completed'
        ? isCompletedLate
          ? 'border-slate-200/80 hover:border-amber-300'
          : 'border-slate-200/80 hover:border-emerald-300'
        : isOverdue
        ? 'border-rose-300/80 bg-rose-50/15'
        : 'border-slate-200/80 hover:border-cimb-300'
    ]"
  >
    <!-- Top Header: Category & Priority on left, Status selector on right -->
    <div>
      <div class="flex items-center justify-between gap-2 pb-3 mb-3 border-b border-slate-100">
        <!-- Badges (Category & Priority) neatly aligned on one line -->
        <div class="flex items-center gap-1.5 sm:gap-2 min-w-0">
          <span
            class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] sm:text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200 truncate max-w-[120px]"
          >
            <Tag class="w-3 h-3 text-slate-400 shrink-0" />
            <span class="truncate">{{ task.category || 'Umum' }}</span>
          </span>

          <span
            :class="[
              'inline-flex items-center px-2 sm:px-2.5 py-0.5 rounded-full text-[11px] sm:text-xs font-bold border',
              priorityBadge.classes
            ]"
          >
            {{ priorityBadge.text }}
          </span>
        </div>

        <!-- Single Unified Status Selector & Badge -->
        <div class="relative shrink-0">
          <select
            :value="task.status"
            @change="emit('change-status', task.id, $event.target.value)"
            :class="[
              'text-[11px] sm:text-xs font-bold pl-2.5 pr-6 py-1 rounded-full border cursor-pointer focus:outline-none appearance-none transition-colors shadow-2xs',
              statusBadge.classes
            ]"
            title="Klik untuk mengubah status pengerjaan tugas"
          >
            <option value="pending">Menunggu</option>
            <option value="in_progress">Dikerjakan</option>
            <option value="completed">
              {{ isCompletedLate ? 'Selesai (Terlambat)' : 'Selesai (Tepat Waktu)' }}
            </option>
          </select>
          <ChevronDown class="w-3.5 h-3.5 text-current opacity-70 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>
      </div>

      <!-- Main Content: Checkbox + Title + Description -->
      <div class="flex items-start gap-3 mt-1">
        <!-- Checkbox Button -->
        <button
          @click.stop="emit('toggle-status', task)"
          type="button"
          :class="[
            'mt-0.5 w-5 h-5 rounded-lg border flex items-center justify-center transition-all shrink-0',
            task.status === 'completed'
              ? isCompletedLate
                ? 'bg-amber-600 border-amber-600 text-white shadow-xs'
                : 'bg-emerald-600 border-emerald-600 text-white shadow-xs'
              : 'border-slate-300 hover:border-cimb-800 text-transparent hover:bg-cimb-50/50'
          ]"
          :title="task.status === 'completed' ? 'Tandai belum selesai' : 'Tandai selesai'"
        >
          <CheckCircle2 class="w-3.5 h-3.5 stroke-[3]" />
        </button>

        <!-- Title & Description (Clickable to open Detail Modal) -->
        <div class="flex-1 min-w-0 cursor-pointer" @click="emit('view', task)">
          <h3
            :class="[
              'text-sm sm:text-base font-bold tracking-tight text-slate-900 group-hover:text-cimb-900 transition-colors leading-snug',
              task.status === 'completed' ? 'line-through text-slate-400 font-semibold' : ''
            ]"
          >
            {{ task.title }}
          </h3>

          <p
            v-if="task.description"
            :class="[
              'mt-1 text-xs sm:text-sm text-slate-500 leading-relaxed whitespace-pre-line line-clamp-2',
              task.status === 'completed' ? 'text-slate-400' : ''
            ]"
          >
            {{ task.description }}
          </p>

          <!-- Attachment Pill Indicator -->
          <div v-if="task.attachment_url" class="mt-2.5 flex items-center gap-1.5">
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-[11px] font-semibold bg-cimb-50 text-cimb-800 border border-cimb-200/80">
              <Paperclip class="w-3 h-3 shrink-0" />
              <span class="truncate max-w-[150px] sm:max-w-[200px]">{{ task.attachment_name || 'Lampiran Berkas' }}</span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Card Footer -->
    <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] sm:text-xs text-slate-500">
      <!-- Date Indicator -->
      <div class="flex items-center gap-1.5 min-w-0 cursor-pointer" @click="emit('view', task)">
        <template v-if="task.status === 'completed'">
          <div class="inline-flex items-center gap-1 text-slate-500 font-medium truncate">
            <CheckCircle2 :class="['w-3.5 h-3.5 shrink-0', isCompletedLate ? 'text-amber-600' : 'text-emerald-600']" />
            <span class="truncate">Selesai: {{ formattedCompletedDate || formattedDueDate }}</span>
          </div>
        </template>
        <template v-else-if="task.due_date">
          <div
            :class="[
              'inline-flex items-center gap-1 px-2 py-0.5 rounded-lg font-medium truncate',
              isOverdue
                ? 'bg-rose-50 text-rose-700 font-semibold'
                : 'text-slate-500 bg-slate-50'
            ]"
          >
            <component
              :is="isOverdue ? AlertCircle : Calendar"
              :class="['w-3.5 h-3.5 shrink-0', isOverdue ? 'text-rose-600' : 'text-slate-400']"
            />
            <span class="truncate">{{ formattedDueDate }}</span>
          </div>
        </template>
        <template v-else>
          <span class="text-slate-400 italic">Tanpa tenggat</span>
        </template>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center space-x-0.5 sm:space-x-1 shrink-0 ml-2">
        <button
          @click="emit('view', task)"
          class="p-1.5 text-slate-400 hover:text-cimb-800 hover:bg-cimb-50 rounded-lg transition-colors"
          title="Lihat Detail Tugas"
        >
          <Eye class="w-4 h-4 sm:w-3.5 sm:h-3.5" />
        </button>
        <button
          @click="emit('edit', task)"
          class="p-1.5 text-slate-400 hover:text-cimb-800 hover:bg-cimb-50 rounded-lg transition-colors"
          title="Edit Tugas"
        >
          <Pencil class="w-4 h-4 sm:w-3.5 sm:h-3.5" />
        </button>
        <button
          @click="emit('delete', task)"
          class="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
          title="Hapus Tugas"
        >
          <Trash2 class="w-4 h-4 sm:w-3.5 sm:h-3.5" />
        </button>
      </div>
    </div>
  </div>
</template>