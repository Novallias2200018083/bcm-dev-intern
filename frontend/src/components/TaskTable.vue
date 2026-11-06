<script setup>
import { computed } from 'vue'
import {
  Calendar,
  AlertCircle,
  Pencil,
  Trash2,
  CheckCircle2,
  Paperclip,
  Eye,
  Timer,
  PlayCircle,
  Clock,
} from 'lucide-vue-next'
import { formatIndonesianDateTime, parseLocalDate } from '../utils/dateFormatter'

const props = defineProps({
  tasks: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['toggle-status', 'change-status', 'edit', 'delete', 'view'])

const isOverdue = (task) => {
  if (!task.due_date || task.status === 'completed') return false
  const due = parseLocalDate(task.due_date)
  return due ? due < new Date() : false
}

const isCompletedLate = (task) => {
  if (task.status !== 'completed' || !task.due_date || !task.completed_at) return false
  const due = parseLocalDate(task.due_date)
  const completed = parseLocalDate(task.completed_at)
  return due && completed ? completed > due : false
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return formatIndonesianDateTime(dateStr, true)
}

const priorityBadge = (priority) => {
  switch (priority) {
    case 'high':
      return { text: 'Tinggi', classes: 'bg-rose-50 text-rose-700 border-rose-200' }
    case 'medium':
      return { text: 'Sedang', classes: 'bg-amber-50 text-amber-700 border-amber-200' }
    case 'low':
      return { text: 'Rendah', classes: 'bg-slate-100 text-slate-600 border-slate-200' }
    default:
      return { text: priority, classes: 'bg-slate-100 text-slate-600 border-slate-200' }
  }
}

const getStatusBadge = (task) => {
  if (task.status === 'completed') {
    if (isCompletedLate(task)) {
      return {
        text: 'Selesai Terlambat',
        icon: Timer,
        classes: 'bg-amber-50 text-amber-800 border-amber-300',
      }
    }
    return {
      text: 'Selesai Tepat Waktu',
      icon: CheckCircle2,
      classes: 'bg-emerald-50 text-emerald-800 border-emerald-300',
    }
  }

  if (task.status === 'in_progress') {
    return {
      text: 'Dikerjakan',
      icon: PlayCircle,
      classes: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    }
  }

  if (isOverdue(task)) {
    return {
      text: 'Lewat Tenggat',
      icon: AlertCircle,
      classes: 'bg-rose-50 text-rose-700 border-rose-300',
    }
  }

  return {
    text: 'Menunggu',
    icon: Clock,
    classes: 'bg-amber-50 text-amber-700 border-amber-200',
  }
}
</script>

<template>
  <div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden mb-6">
    <div class="overflow-x-auto">
      <table class="w-full text-left text-xs sm:text-sm text-slate-600 min-w-[720px]">
        <thead class="bg-slate-50/80 border-b border-slate-200 text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider">
          <tr>
            <th scope="col" class="w-12 px-3 sm:px-4 py-3 sm:py-3.5 text-center">Centang</th>
            <th scope="col" class="px-3 sm:px-4 py-3 sm:py-3.5">Judul & Deskripsi</th>
            <th scope="col" class="px-3 sm:px-4 py-3 sm:py-3.5">Status Pengerjaan</th>
            <th scope="col" class="px-3 sm:px-4 py-3 sm:py-3.5">Kategori</th>
            <th scope="col" class="px-3 sm:px-4 py-3 sm:py-3.5">Prioritas</th>
            <th scope="col" class="px-3 sm:px-4 py-3 sm:py-3.5">Tenggat Waktu (WIB)</th>
            <th scope="col" class="px-3 sm:px-4 py-3 sm:py-3.5 text-right">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="task in tasks"
            :key="task.id"
            :class="[
              'hover:bg-slate-50/60 transition-colors',
              task.status === 'completed'
                ? isCompletedLate(task)
                  ? 'bg-amber-50/15'
                  : 'bg-emerald-50/20'
                : ''
            ]"
          >
            <!-- Checkbox & Status toggle -->
            <td class="px-3 sm:px-4 py-3 sm:py-3.5 text-center">
              <button
                @click="emit('toggle-status', task)"
                type="button"
                :class="[
                  'w-5 h-5 rounded-lg border flex items-center justify-center transition-all mx-auto',
                  task.status === 'completed'
                    ? isCompletedLate(task)
                      ? 'bg-amber-600 border-amber-600 text-white'
                      : 'bg-emerald-600 border-emerald-600 text-white'
                    : 'border-slate-300 hover:border-emerald-600 text-transparent hover:text-slate-300'
                ]"
                :title="task.status === 'completed' ? 'Tandai belum selesai' : 'Tandai selesai'"
              >
                <CheckCircle2 class="w-3.5 h-3.5 stroke-[3]" />
              </button>
            </td>

            <!-- Title & Description -->
            <td class="px-3 sm:px-4 py-3 sm:py-3.5 cursor-pointer" @click="emit('view', task)">
              <div class="flex items-center gap-1.5 flex-wrap">
                <span
                  class="font-bold text-slate-900 hover:text-cimb-800 transition-colors"
                  :class="{ 'line-through text-slate-400': task.status === 'completed' }"
                >
                  {{ task.title }}
                </span>
                <span
                  v-if="task.attachment_url"
                  class="inline-flex items-center text-cimb-800"
                  title="Ada lampiran berkas"
                >
                  <Paperclip class="w-3.5 h-3.5" />
                </span>
              </div>
              <p v-if="task.description" class="text-xs text-slate-500 line-clamp-1 mt-0.5 max-w-md">
                {{ task.description }}
              </p>
            </td>

            <!-- Execution Status -->
            <td class="px-3 sm:px-4 py-3 sm:py-3.5 whitespace-nowrap">
              <span
                :class="[
                  'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold border',
                  getStatusBadge(task).classes
                ]"
              >
                <component :is="getStatusBadge(task).icon" class="w-3.5 h-3.5 shrink-0" />
                <span>{{ getStatusBadge(task).text }}</span>
              </span>
            </td>

            <!-- Category -->
            <td class="px-3 sm:px-4 py-3 sm:py-3.5 whitespace-nowrap">
              <span class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">
                {{ task.category || 'Umum' }}
              </span>
            </td>

            <!-- Priority -->
            <td class="px-3 sm:px-4 py-3 sm:py-3.5 whitespace-nowrap">
              <span
                :class="[
                  'inline-flex px-2.5 py-0.5 rounded-full text-xs font-bold border',
                  priorityBadge(task.priority).classes
                ]"
              >
                {{ priorityBadge(task.priority).text }}
              </span>
            </td>

            <!-- Due Date (WIB) -->
            <td class="px-3 sm:px-4 py-3 sm:py-3.5 text-xs whitespace-nowrap">
              <div v-if="task.due_date" class="flex items-center gap-1.5 font-medium">
                <component
                  :is="isOverdue(task) ? AlertCircle : Calendar"
                  :class="['w-3.5 h-3.5 shrink-0', isOverdue(task) ? 'text-rose-600' : 'text-slate-400']"
                />
                <span :class="isOverdue(task) ? 'text-rose-600 font-bold' : 'text-slate-600'">
                  {{ formatDate(task.due_date) }}
                </span>
              </div>
              <span v-else class="text-slate-400 italic">-</span>
            </td>

            <!-- Actions -->
            <td class="px-3 sm:px-4 py-3 sm:py-3.5 text-right whitespace-nowrap">
              <div class="inline-flex items-center gap-1">
                <button
                  @click="emit('view', task)"
                  class="p-1.5 text-slate-400 hover:text-cimb-800 hover:bg-cimb-50 rounded-lg transition-colors"
                  title="Lihat Detail"
                >
                  <Eye class="w-4 h-4" />
                </button>
                <button
                  @click="emit('edit', task)"
                  class="p-1.5 text-slate-400 hover:text-cimb-800 hover:bg-cimb-50 rounded-lg transition-colors"
                  title="Edit"
                >
                  <Pencil class="w-4 h-4" />
                </button>
                <button
                  @click="emit('delete', task)"
                  class="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                  title="Hapus"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
