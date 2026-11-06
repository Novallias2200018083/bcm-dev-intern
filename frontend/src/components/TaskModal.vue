<script setup>
import { ref, watch, computed } from 'vue'
import { X, Calendar, AlertCircle, Loader2, Paperclip } from 'lucide-vue-next'
import { toDateTimeLocalValue, fromDateTimeLocalValue } from '../utils/dateFormatter'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  task: {
    type: Object,
    default: null,
  },
  categories: {
    type: Array,
    default: () => [],
  },
  isSubmitting: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close', 'save'])

const isEditing = computed(() => !!props.task)

const defaultCategories = [
  'Umum',
  'Pekerjaan',
  'Rapat',
  'Proyek',
  'Pribadi',
  'Operasional',
  'Nasabah',
]

const allCategories = computed(() => {
  const merged = [...defaultCategories, ...(props.categories || [])]
  return Array.from(new Set(merged.filter(Boolean)))
})

const selectedCategoryMode = ref('Umum')
const customCategoryText = ref('')

const form = ref({
  title: '',
  description: '',
  category: 'Umum',
  priority: 'medium',
  status: 'pending',
  due_date: '',
})

const selectedFile = ref(null)
const fileInputRef = ref(null)
const errors = ref({})

// Quick deadline helper
const setQuickDue = (hoursFromNow) => {
  const d = new Date()
  d.setHours(d.getHours() + hoursFromNow)
  form.value.due_date = toDateTimeLocalValue(d)
}

const onFileChanged = (e) => {
  const file = e.target.files?.[0]
  if (file) {
    if (file.size > 10 * 1024 * 1024) {
      errors.value.file = 'Ukuran berkas melebihi batas 10 MB'
      selectedFile.value = null
      return
    }
    errors.value.file = null
    selectedFile.value = file
  }
}

watch(
  () => props.isOpen,
  (val) => {
    if (val) {
      errors.value = {}
      selectedFile.value = null
      if (props.task) {
        const taskCat = props.task.category || 'Umum'
        if (allCategories.value.includes(taskCat)) {
          selectedCategoryMode.value = taskCat
          customCategoryText.value = ''
        } else {
          selectedCategoryMode.value = '__custom__'
          customCategoryText.value = taskCat
        }

        form.value = {
          title: props.task.title || '',
          description: props.task.description || '',
          category: taskCat,
          priority: props.task.priority || 'medium',
          status: props.task.status || 'pending',
          due_date: toDateTimeLocalValue(props.task.due_date),
        }
      } else {
        selectedCategoryMode.value = 'Umum'
        customCategoryText.value = ''
        form.value = {
          title: '',
          description: '',
          category: 'Umum',
          priority: 'medium',
          status: 'pending',
          due_date: '',
        }
      }
    }
  },
  { immediate: true }
)

const handleSubmit = () => {
  errors.value = {}
  if (!form.value.title.trim()) {
    errors.value.title = 'Judul tugas wajib diisi!'
    return
  }

  // Preserve exact local time without UTC offset drift
  const dueVal = fromDateTimeLocalValue(form.value.due_date)

  let finalCat = 'Umum'
  if (selectedCategoryMode.value === '__custom__') {
    finalCat = customCategoryText.value.trim() || 'Umum'
  } else {
    finalCat = selectedCategoryMode.value
  }

  const payload = {
    title: form.value.title.trim(),
    description: form.value.description.trim() || null,
    category: finalCat,
    priority: form.value.priority,
    status: form.value.status,
    due_date: dueVal,
  }

  emit('save', { payload, file: selectedFile.value })
}
</script>

<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 overflow-y-auto bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4 transition-all"
    @click.self="emit('close')"
  >
    <div class="relative bg-white rounded-3xl shadow-2xl border border-slate-200/80 w-full max-w-lg overflow-hidden transform transition-all animate-in fade-in zoom-in-95 duration-150 my-auto">
      
      <!-- Top Red Brand Stripe (Solid) -->
      <div class="h-1.5 w-full bg-cimb-800"></div>

      <!-- Modal Header -->
      <div class="px-4 sm:px-6 py-3.5 sm:py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/70">
        <div class="flex items-center gap-2">
          <span class="text-[10px] sm:text-xs font-bold px-2 py-0.5 rounded bg-cimb-50 text-cimb-800 border border-cimb-200">
            CIMB NIAGA
          </span>
          <h3 class="text-sm sm:text-base font-bold text-slate-900">
            {{ isEditing ? 'Edit Tugas Harian' : 'Tambah Tugas Baru' }}
          </h3>
        </div>
        <button
          @click="emit('close')"
          type="button"
          class="text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100 transition-colors"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Modal Body (Responsive Scroll) -->
      <form @submit.prevent="handleSubmit" class="p-4 sm:p-6 space-y-3.5 sm:space-y-4 max-h-[75vh] overflow-y-auto">
        <!-- Title Input -->
        <div>
          <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
            Judul Tugas <span class="text-cimb-700">*</span>
          </label>
          <input
            v-model="form.title"
            type="text"
            spellcheck="false"
            placeholder="Contoh: Selesaikan laporan rekonsiliasi kas harian"
            :class="[
              'w-full px-3.5 py-2.5 rounded-xl border text-xs sm:text-sm transition-all focus:outline-none focus:ring-2',
              errors.title
                ? 'border-rose-300 ring-rose-500/20 text-rose-900 bg-rose-50/30'
                : 'border-slate-200 focus:ring-cimb-800/15 focus:border-cimb-700 bg-slate-50/50 focus:bg-white'
            ]"
            autofocus
          />
          <p v-if="errors.title" class="text-xs text-rose-600 mt-1 flex items-center gap-1 font-medium">
            <AlertCircle class="w-3.5 h-3.5" />
            {{ errors.title }}
          </p>
        </div>

        <!-- Category & Priority (2-col grid) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
          <!-- Category Select Dropdown -->
          <div>
            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Kategori
            </label>
            <select
              v-model="selectedCategoryMode"
              class="w-full px-3.5 py-2 sm:py-2.5 rounded-xl border border-slate-200 text-xs sm:text-sm bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 transition-all cursor-pointer"
            >
              <option v-for="cat in allCategories" :key="cat" :value="cat">
                {{ cat }}
              </option>
              <option value="__custom__">+ Kategori Lainnya...</option>
            </select>
            <input
              v-if="selectedCategoryMode === '__custom__'"
              v-model="customCategoryText"
              type="text"
              spellcheck="false"
              placeholder="Tuliskan nama kategori baru..."
              class="mt-2 w-full px-3 py-1.5 rounded-xl border border-slate-200 text-xs sm:text-sm bg-white focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 transition-all"
            />
          </div>

          <!-- Priority -->
          <div>
            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Prioritas
            </label>
            <select
              v-model="form.priority"
              class="w-full px-3.5 py-2 sm:py-2.5 rounded-xl border border-slate-200 text-xs sm:text-sm bg-slate-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 transition-all cursor-pointer"
            >
              <option value="low">Rendah (Low)</option>
              <option value="medium">Sedang (Medium)</option>
              <option value="high">Tinggi (High)</option>
            </select>
          </div>
        </div>

        <!-- Status & Due Date (2-col grid) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
          <!-- Status -->
          <div>
            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Status
            </label>
            <select
              v-model="form.status"
              class="w-full px-3.5 py-2 sm:py-2.5 rounded-xl border border-slate-200 text-xs sm:text-sm bg-slate-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 transition-all cursor-pointer"
            >
              <option value="pending">Menunggu (Pending)</option>
              <option value="in_progress">Dikerjakan (In Progress)</option>
              <option value="completed">Selesai (Completed)</option>
            </select>
          </div>

          <!-- Due Date Picker (WIB) -->
          <div>
            <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Tenggat Waktu (WIB)
            </label>
            <input
              v-model="form.due_date"
              type="datetime-local"
              class="w-full px-3.5 py-2 sm:py-2.5 rounded-xl border border-slate-200 text-xs sm:text-sm bg-slate-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 transition-all"
            />
          </div>
        </div>

        <!-- Quick Due Date Presets -->
        <div class="flex items-center flex-wrap gap-1.5 text-[11px] text-slate-500">
          <span class="text-slate-400">Pilihan cepat:</span>
          <button
            type="button"
            @click="setQuickDue(4)"
            class="px-2 py-0.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors"
          >
            +4 Jam
          </button>
          <button
            type="button"
            @click="setQuickDue(24)"
            class="px-2 py-0.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors"
          >
            Besok
          </button>
          <button
            type="button"
            @click="setQuickDue(72)"
            class="px-2 py-0.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors"
          >
            3 Hari
          </button>
          <button
            v-if="form.due_date"
            type="button"
            @click="form.due_date = ''"
            class="px-2 py-0.5 rounded-md text-cimb-700 hover:bg-cimb-50 transition-colors ml-auto"
          >
            Hapus
          </button>
        </div>

        <!-- Attachment Picker -->
        <div>
          <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center justify-between">
            <span>Lampiran Gambar / Dokumen</span>
            <span class="text-slate-400 text-[10px] sm:text-[11px] font-normal">Maks. 10 MB</span>
          </label>
          <div class="flex items-center gap-2">
            <input
              ref="fileInputRef"
              type="file"
              accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt"
              class="w-full text-xs text-slate-500 file:mr-2.5 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-[11px] file:font-bold file:bg-cimb-50 file:text-cimb-800 hover:file:bg-cimb-100 cursor-pointer border border-slate-200 rounded-xl p-1 bg-slate-50/40"
              @change="onFileChanged"
            />
            <button
              v-if="selectedFile"
              type="button"
              @click="selectedFile = null; if (fileInputRef) fileInputRef.value = ''"
              class="text-xs text-rose-600 hover:bg-rose-50 p-1.5 rounded-lg shrink-0"
              title="Batalkan pilihan berkas"
            >
              <X class="w-4 h-4" />
            </button>
          </div>
          <p v-if="task?.attachment_name && !selectedFile" class="text-[11px] text-slate-500 mt-1 flex items-center gap-1">
            <Paperclip class="w-3 h-3 text-cimb-800" />
            <span>Lampiran aktif: <strong>{{ task.attachment_name }}</strong></span>
          </p>
        </div>

        <!-- Description Textarea -->
        <div>
          <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
            Deskripsi / Catatan Tambahan
          </label>
          <textarea
            v-model="form.description"
            rows="3"
            spellcheck="false"
            placeholder="Tambahkan detail, checklist, link, atau catatan penting terkait tugas ini..."
            class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs sm:text-sm bg-slate-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 transition-all"
          ></textarea>
        </div>

        <!-- Modal Footer Actions -->
        <div class="pt-3 border-t border-slate-100 flex items-center justify-end gap-2.5">
          <button
            type="button"
            @click="emit('close')"
            class="px-4 py-2 text-xs sm:text-sm font-semibold text-slate-600 hover:bg-slate-100 rounded-xl transition-colors active:scale-[0.98]"
          >
            Batal
          </button>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="inline-flex items-center gap-2 px-5 py-2.5 bg-cimb-800 hover:bg-cimb-900 active:bg-cimb-950 text-white text-xs sm:text-sm font-bold rounded-xl shadow-sm hover:shadow-md shadow-cimb-800/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98]"
          >
            <Loader2 v-if="isSubmitting" class="w-4 h-4 animate-spin" />
            <span>{{ isEditing ? 'Simpan Perubahan' : 'Buat Tugas' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
