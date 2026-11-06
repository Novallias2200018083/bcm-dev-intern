<script setup>
import { ref, computed } from 'vue'
import {
  X,
  Calendar,
  Clock,
  CheckCircle2,
  AlertCircle,
  Tag,
  Paperclip,
  Upload,
  FileText,
  Image as ImageIcon,
  Download,
  Trash2,
  ExternalLink,
  Pencil,
  Timer,
  PlayCircle,
} from 'lucide-vue-next'
import { formatIndonesianDateTime, parseLocalDate } from '../utils/dateFormatter'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  task: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits([
  'close',
  'edit',
  'toggle-status',
  'upload-attachment',
  'delete-attachment',
])

const fileInputRef = ref(null)
const uploadError = ref('')

const isOverdue = computed(() => {
  if (!props.task?.due_date || props.task?.status === 'completed') return false
  const due = parseLocalDate(props.task.due_date)
  return due ? due < new Date() : false
})

const isCompletedLate = computed(() => {
  if (props.task?.status !== 'completed' || !props.task?.due_date || !props.task?.completed_at) return false
  const due = parseLocalDate(props.task.due_date)
  const completed = parseLocalDate(props.task.completed_at)
  return due && completed ? completed > due : false
})

const isImage = computed(() => {
  if (!props.task?.attachment_url) return false
  const type = (props.task.attachment_type || '').toLowerCase()
  const name = (props.task.attachment_name || '').toLowerCase()
  return (
    type.startsWith('image/') ||
    name.endsWith('.png') ||
    name.endsWith('.jpg') ||
    name.endsWith('.jpeg') ||
    name.endsWith('.webp') ||
    name.endsWith('.gif') ||
    name.endsWith('.svg')
  )
})

// Ensures URL resolves cleanly whether via proxy or direct backend
const fileUrl = computed(() => {
  const url = props.task?.attachment_url
  if (!url) return ''
  if (url.startsWith('http')) return url
  return url
})

const formattedSize = computed(() => {
  const bytes = props.task?.attachment_size
  if (!bytes) return ''
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
})

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return formatIndonesianDateTime(dateStr, true)
}

const priorityBadge = computed(() => {
  switch (props.task?.priority) {
    case 'high':
      return { text: 'Tinggi (High)', classes: 'bg-rose-50 text-rose-700 border-rose-200' }
    case 'medium':
      return { text: 'Sedang (Medium)', classes: 'bg-amber-50 text-amber-700 border-amber-200' }
    case 'low':
      return { text: 'Rendah (Low)', classes: 'bg-slate-100 text-slate-600 border-slate-200' }
    default:
      return { text: props.task?.priority || '-', classes: 'bg-slate-100 text-slate-600' }
  }
})

const statusBadge = computed(() => {
  if (props.task?.status === 'completed') {
    if (isCompletedLate.value) {
      return {
        text: 'Selesai Terlambat',
        icon: Timer,
        classes: 'bg-amber-50 text-amber-800 border-amber-300',
        dot: 'bg-amber-500',
      }
    }
    return {
      text: 'Selesai Tepat Waktu',
      icon: CheckCircle2,
      classes: 'bg-emerald-50 text-emerald-800 border-emerald-300',
      dot: 'bg-emerald-500',
    }
  }

  if (props.task?.status === 'in_progress') {
    return {
      text: 'Sedang Dikerjakan',
      icon: PlayCircle,
      classes: 'bg-indigo-50 text-indigo-700 border-indigo-200',
      dot: 'bg-indigo-500',
    }
  }

  if (isOverdue.value) {
    return {
      text: 'Lewat Deadline',
      icon: AlertCircle,
      classes: 'bg-rose-50 text-rose-700 border-rose-300',
      dot: 'bg-rose-500',
    }
  }

  return {
    text: 'Menunggu',
    icon: Clock,
    classes: 'bg-amber-50 text-amber-700 border-amber-200',
    dot: 'bg-amber-500',
  }
})

const triggerFileInput = () => {
  if (fileInputRef.value) {
    fileInputRef.value.click()
  }
}

const handleFileSelected = (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  uploadError.value = ''

  if (file.size > 10 * 1024 * 1024) {
    uploadError.value = 'Ukuran berkas melebihi batas maksimal 10 MB'
    return
  }

  emit('upload-attachment', props.task.id, file)
  e.target.value = ''
}
</script>

<template>
  <div
    v-if="isOpen && task"
    class="fixed inset-0 z-50 overflow-y-auto bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4 transition-all"
    @click.self="emit('close')"
  >
    <div class="relative bg-white rounded-3xl shadow-2xl border border-slate-200 w-full max-w-2xl overflow-hidden transform transition-all animate-in fade-in zoom-in-95 duration-150 my-auto">
      
      <!-- Top Red Brand Stripe (Solid Color, No Gradients) -->
      <div class="h-1.5 w-full bg-cimb-800"></div>

      <!-- Modal Header -->
      <div class="px-5 sm:px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
        <div class="flex items-center gap-2">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] sm:text-xs font-bold bg-cimb-50 text-cimb-800 border border-cimb-200">
            CIMB NIAGA
          </span>
          <span class="text-xs font-semibold text-slate-300">•</span>
          <span class="text-xs font-semibold text-slate-500">ID Tugas #{{ task.id }}</span>
        </div>
        <button
          @click="emit('close')"
          type="button"
          class="text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-200/60 transition-colors"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Modal Body (Responsive Scroll) -->
      <div class="p-5 sm:p-6 space-y-5 max-h-[72vh] sm:max-h-[75vh] overflow-y-auto">
        
        <!-- Status & Tags Row -->
        <div class="flex flex-wrap items-center gap-2">
          <!-- Status Badge -->
          <span :class="['inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border', statusBadge.classes]">
            <component :is="statusBadge.icon" class="w-3.5 h-3.5 shrink-0" />
            <span>{{ statusBadge.text }}</span>
          </span>

          <!-- Priority Badge -->
          <span :class="['inline-flex items-center px-3 py-1 rounded-full text-xs font-bold border', priorityBadge.classes]">
            Prioritas: {{ priorityBadge.text }}
          </span>

          <!-- Category Badge -->
          <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
            <Tag class="w-3 h-3 text-slate-400 shrink-0" />
            {{ task.category || 'Umum' }}
          </span>
        </div>

        <!-- Task Title -->
        <div>
          <h2 class="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 leading-snug">
            {{ task.title }}
          </h2>
        </div>

        <!-- Description Section -->
        <div class="bg-slate-50 rounded-2xl p-4 sm:p-5 border border-slate-200/80">
          <h4 class="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">
            Deskripsi & Rincian Tugas
          </h4>
          <p
            v-if="task.description"
            class="text-xs sm:text-sm text-slate-700 leading-relaxed whitespace-pre-line"
          >
            {{ task.description }}
          </p>
          <p v-else class="text-xs sm:text-sm text-slate-400 italic">
            Tidak ada deskripsi tambahan untuk tugas ini.
          </p>
        </div>

        <!-- Key Info Grid (Responsive 1-col on mobile, 2-col on sm) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-600">
          <!-- Due Date (WIB) -->
          <div class="p-3.5 rounded-xl border border-slate-200 bg-white">
            <span class="text-slate-400 font-medium block mb-1">Tenggat Waktu (WIB)</span>
            <div class="flex items-center gap-1.5 font-bold" :class="isOverdue ? 'text-rose-600' : 'text-slate-800'">
              <component :is="isOverdue ? AlertCircle : Calendar" class="w-4 h-4 shrink-0" />
              <span>{{ formatDate(task.due_date) }}</span>
              <span v-if="isOverdue" class="ml-1 text-[10px] px-1.5 py-0.2 rounded bg-rose-100 text-rose-700 font-bold">
                Terlambat
              </span>
            </div>
          </div>

          <!-- Completed At / Created At (WIB) -->
          <div class="p-3.5 rounded-xl border border-slate-200 bg-white">
            <span class="text-slate-400 font-medium block mb-1">
              {{ task.status === 'completed' ? 'Waktu Diselesaikan (WIB)' : 'Waktu Dibuat (WIB)' }}
            </span>
            <div class="flex items-center gap-1.5 font-bold text-slate-800 flex-wrap">
              <Clock class="w-4 h-4 text-slate-400 shrink-0" />
              <span>{{ formatDate(task.status === 'completed' ? task.completed_at : task.created_at) }}</span>
              <template v-if="task.status === 'completed'">
                <span
                  v-if="isCompletedLate"
                  class="ml-1 text-[10px] px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold border border-amber-300"
                >
                  Selesai Terlambat
                </span>
                <span
                  v-else
                  class="ml-1 text-[10px] px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold border border-emerald-300"
                >
                  Selesai Tepat Waktu
                </span>
              </template>
            </div>
          </div>
        </div>

        <!-- Attachment Section -->
        <div class="border-t border-slate-200 pt-5">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <Paperclip class="w-4 h-4 text-cimb-800" />
              <h4 class="text-xs sm:text-sm font-bold text-slate-900">
                Dokumen & Gambar Pendukung
              </h4>
            </div>
            
            <button
              v-if="!task.attachment_url"
              type="button"
              @click="triggerFileInput"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-cimb-800 bg-cimb-50 hover:bg-cimb-100 border border-cimb-200 rounded-xl transition-all"
            >
              <Upload class="w-3.5 h-3.5" />
              <span>Unggah Berkas</span>
            </button>
          </div>

          <!-- Hidden File Input -->
          <input
            ref="fileInputRef"
            type="file"
            class="hidden"
            accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.zip"
            @change="handleFileSelected"
          />

          <!-- Upload error if any -->
          <p v-if="uploadError" class="text-xs text-rose-600 mb-2 flex items-center gap-1 font-medium">
            <AlertCircle class="w-3.5 h-3.5" />
            {{ uploadError }}
          </p>

          <!-- CASE 1: Attachment Exists (Single Clean Unified Card) -->
          <div v-if="task.attachment_url" class="rounded-2xl border border-slate-200 bg-slate-50 p-4 space-y-3">
            
            <!-- File Info Header Bar -->
            <div class="flex items-center justify-between gap-3">
              <div class="flex items-center gap-3 min-w-0">
                <div class="w-10 h-10 rounded-xl bg-cimb-800 text-white flex items-center justify-center shrink-0 shadow-xs">
                  <component :is="isImage ? ImageIcon : FileText" class="w-5 h-5" />
                </div>
                <div class="min-w-0">
                  <p class="text-xs sm:text-sm font-bold text-slate-900 truncate">
                    {{ task.attachment_name || 'Lampiran Berkas' }}
                  </p>
                  <p class="text-[11px] text-slate-500 mt-0.5 truncate">
                    {{ formattedSize }} <span v-if="task.attachment_type">• {{ task.attachment_type }}</span>
                  </p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex items-center gap-1.5 shrink-0">
                <a
                  :href="fileUrl"
                  :download="task.attachment_name"
                  target="_blank"
                  class="p-2 text-slate-600 hover:text-cimb-800 hover:bg-white rounded-xl transition-colors border border-transparent hover:border-slate-200"
                  title="Unduh / Buka Berkas"
                >
                  <Download class="w-4 h-4" />
                </a>
                <button
                  type="button"
                  @click="triggerFileInput"
                  class="p-2 text-slate-600 hover:text-blue-600 hover:bg-white rounded-xl transition-colors border border-transparent hover:border-slate-200"
                  title="Ganti Berkas"
                >
                  <Upload class="w-4 h-4" />
                </button>
                <button
                  type="button"
                  @click="emit('delete-attachment', task.id)"
                  class="p-2 text-slate-400 hover:text-rose-600 hover:bg-white rounded-xl transition-colors border border-transparent hover:border-slate-200"
                  title="Hapus Lampiran"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Image Preview Box (Clean, Solid, No Gradient Overlays) -->
            <div v-if="isImage" class="pt-3 border-t border-slate-200/80">
              <div class="bg-white rounded-xl border border-slate-200 p-2 overflow-hidden flex flex-col items-center">
                <a :href="fileUrl" target="_blank" title="Klik untuk membuka ukuran penuh">
                  <img
                    :src="fileUrl"
                    :alt="task.attachment_name || 'Lampiran tugas'"
                    class="max-h-64 object-contain rounded-lg hover:opacity-95 transition-opacity"
                  />
                </a>
                <a
                  :href="fileUrl"
                  target="_blank"
                  class="inline-flex items-center gap-1.5 text-xs font-semibold text-cimb-800 hover:text-cimb-900 mt-2.5 transition-colors"
                >
                  <ExternalLink class="w-3.5 h-3.5" />
                  <span>Buka gambar di tab baru</span>
                </a>
              </div>
            </div>

          </div>

          <!-- CASE 2: No Attachment Yet (Clean Solid Dropzone) -->
          <div
            v-else
            @click="triggerFileInput"
            class="border-2 border-dashed border-slate-200 hover:border-cimb-700 rounded-2xl p-6 text-center cursor-pointer transition-colors bg-slate-50 hover:bg-cimb-50/40 group"
          >
            <div class="w-10 h-10 rounded-xl bg-slate-200 group-hover:bg-cimb-100 text-slate-500 group-hover:text-cimb-800 flex items-center justify-center mx-auto mb-2 transition-colors">
              <Upload class="w-5 h-5" />
            </div>
            <p class="text-xs sm:text-sm font-bold text-slate-700 group-hover:text-cimb-800 transition-colors">
              Klik untuk menambahkan gambar atau dokumen pendukung
            </p>
            <p class="text-[11px] text-slate-400 mt-1">
              Mendukung gambar (PNG, JPG, WEBP) dan dokumen (PDF, Word, Excel, TXT) maks. 10 MB
            </p>
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="px-5 sm:px-6 py-4 border-t border-slate-100 bg-slate-50 flex flex-col-reverse sm:flex-row sm:items-center justify-between gap-2.5">
        <!-- Status Toggle Quick Action -->
        <button
          type="button"
          @click="emit('toggle-status', task)"
          :class="[
            'w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-4 py-2.5 sm:py-2 rounded-xl text-xs font-bold border transition-all active:scale-[0.98]',
            task.status === 'completed'
              ? 'bg-amber-50 hover:bg-amber-100 text-amber-700 border-amber-200'
              : 'bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border-emerald-200'
          ]"
        >
          <CheckCircle2 class="w-4 h-4" />
          <span>{{ task.status === 'completed' ? 'Buka Kembali Tugas' : 'Tandai Sebagai Selesai' }}</span>
        </button>

        <div class="flex items-center justify-end gap-2.5 w-full sm:w-auto">
          <!-- Edit Button -->
          <button
            type="button"
            @click="emit('edit', task)"
            class="flex-1 sm:flex-none inline-flex items-center justify-center gap-1.5 px-4 py-2.5 sm:py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-colors active:scale-[0.98]"
          >
            <Pencil class="w-3.5 h-3.5" />
            <span>Edit Tugas</span>
          </button>

          <!-- Close Button (Solid CIMB Red) -->
          <button
            type="button"
            @click="emit('close')"
            class="flex-1 sm:flex-none px-5 py-2.5 sm:py-2 bg-cimb-800 hover:bg-cimb-900 active:bg-cimb-950 text-white text-xs font-bold rounded-xl transition-colors shadow-xs active:scale-[0.98]"
          >
            Tutup
          </button>
        </div>
      </div>

    </div>
  </div>
</template>
