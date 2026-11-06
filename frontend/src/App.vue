<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  ListPlus,
  Loader2,
  RefreshCw,
  Download,
  Inbox,
} from 'lucide-vue-next'
import { formatIndonesianDateTime } from './utils/dateFormatter'

import Navbar from './components/Navbar.vue'
import StatsCards from './components/StatsCards.vue'
import FilterBar from './components/FilterBar.vue'
import TaskCard from './components/TaskCard.vue'
import TaskTable from './components/TaskTable.vue'
import TaskModal from './components/TaskModal.vue'
import TaskDetailModal from './components/TaskDetailModal.vue'
import ConfirmModal from './components/ConfirmModal.vue'
import Toast from './components/Toast.vue'

import taskService from './services/taskService'

// Main state
const tasks = ref([])
const stats = ref({
  total: 0,
  pending: 0,
  in_progress: 0,
  completed: 0,
  completed_on_time: 0,
  completed_late: 0,
  overdue: 0,
  completion_rate: 0,
})
const categories = ref([])
const isLoading = ref(true)

// Filters & View state
const search = ref('')
const selectedStatus = ref('')
const selectedPriority = ref('')
const selectedCategory = ref('')
const isOverdueFilter = ref(false)
const sortBy = ref('created_at')
const order = ref('desc')
const viewMode = ref('grid')

const statusFilterLabel = computed(() => {
  switch (selectedStatus.value) {
    case 'completed_on_time':
      return 'Selesai Tepat Waktu'
    case 'completed_late':
      return 'Selesai Terlambat'
    case 'completed':
      return 'Selesai (Semua)'
    case 'in_progress':
      return 'Dikerjakan'
    case 'pending':
      return 'Menunggu'
    default:
      return ''
  }
})

// Modals state
const isModalOpen = ref(false)
const editingTask = ref(null)
const isSubmitting = ref(false)

const isDetailOpen = ref(false)
const detailTask = ref(null)

const isConfirmOpen = ref(false)
const taskToDelete = ref(null)
const isDeleting = ref(false)

// Toast notifications
const toasts = ref([])
let toastIdCounter = 0

const addToast = (message, type = 'success') => {
  const id = ++toastIdCounter
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    removeToast(id)
  }, 4000)
}

const removeToast = (id) => {
  toasts.value = toasts.value.filter((t) => t.id !== id)
}

// Fetch all data
const fetchTasks = async () => {
  isLoading.value = true
  try {
    const params = {
      sort_by: sortBy.value,
      order: order.value,
    }
    if (search.value.trim()) params.search = search.value.trim()
    if (selectedStatus.value) params.status = selectedStatus.value
    if (selectedPriority.value) params.priority = selectedPriority.value
    if (selectedCategory.value) params.category = selectedCategory.value
    if (isOverdueFilter.value) params.is_overdue = true

    const data = await taskService.getTasks(params)
    tasks.value = data

    // If detail modal is open, keep detailTask updated
    if (detailTask.value) {
      const updated = data.find((t) => t.id === detailTask.value.id)
      if (updated) detailTask.value = updated
    }
  } catch (err) {
    addToast(err.message || 'Gagal memuat daftar tugas', 'error')
  } finally {
    isLoading.value = false
  }
}

const fetchStats = async () => {
  try {
    const data = await taskService.getStats()
    stats.value = data
  } catch (err) {
    console.error('Failed to fetch stats:', err)
  }
}

const fetchCategories = async () => {
  try {
    const data = await taskService.getCategories()
    categories.value = data
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

const refreshAll = async () => {
  await Promise.all([fetchTasks(), fetchStats(), fetchCategories()])
}

// Debounce timer for search
let searchDebounceTimer = null
watch(search, () => {
  clearTimeout(searchDebounceTimer)
  searchDebounceTimer = setTimeout(() => {
    fetchTasks()
  }, 300)
})

watch(
  [selectedStatus, selectedPriority, selectedCategory, isOverdueFilter, sortBy, order],
  () => {
    fetchTasks()
  }
)

// Actions
const handleToggleStatus = async (task) => {
  const newStatus = task.status === 'completed' ? 'pending' : 'completed'
  try {
    const updated = await taskService.updateStatus(task.id, newStatus)
    addToast(
      newStatus === 'completed'
        ? `Tugas "${task.title}" diselesaikan! 🎉`
        : `Tugas "${task.title}" dibuka kembali.`
    )
    if (detailTask.value && detailTask.value.id === task.id) {
      detailTask.value = updated
    }
    refreshAll()
  } catch (err) {
    addToast(err.message || 'Gagal mengubah status tugas', 'error')
  }
}

const handleChangeStatus = async (taskId, newStatus) => {
  try {
    const updated = await taskService.updateStatus(taskId, newStatus)
    addToast('Status tugas berhasil diperbarui')
    if (detailTask.value && detailTask.value.id === taskId) {
      detailTask.value = updated
    }
    refreshAll()
  } catch (err) {
    addToast(err.message || 'Gagal mengubah status', 'error')
  }
}

const handleViewTask = (task) => {
  detailTask.value = task
  isDetailOpen.value = true
}

const handleOpenCreate = () => {
  editingTask.value = null
  isModalOpen.value = true
}

const handleOpenEdit = (task) => {
  editingTask.value = task
  isModalOpen.value = true
}

const handleSaveTask = async ({ payload, file }) => {
  isSubmitting.value = true
  try {
    let saved
    if (editingTask.value) {
      saved = await taskService.updateTask(editingTask.value.id, payload)
      addToast('Tugas berhasil diperbarui!')
    } else {
      saved = await taskService.createTask(payload)
      addToast('Tugas baru berhasil ditambahkan!')
    }

    // If an attachment file was selected in the form, upload it now
    if (file && saved?.id) {
      try {
        saved = await taskService.uploadAttachment(saved.id, file)
        addToast('Berkas lampiran berhasil diunggah!')
      } catch (uploadErr) {
        addToast(`Tugas tersimpan, namun upload berkas gagal: ${uploadErr.message}`, 'error')
      }
    }

    if (detailTask.value && saved && detailTask.value.id === saved.id) {
      detailTask.value = saved
    }

    isModalOpen.value = false
    refreshAll()
  } catch (err) {
    addToast(err.message || 'Gagal menyimpan tugas', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleUploadAttachment = async (taskId, file) => {
  try {
    const updated = await taskService.uploadAttachment(taskId, file)
    addToast('Berkas lampiran berhasil diunggah!')
    if (detailTask.value && detailTask.value.id === taskId) {
      detailTask.value = updated
    }
    refreshAll()
  } catch (err) {
    addToast(err.message || 'Gagal mengunggah lampiran', 'error')
  }
}

const handleDeleteAttachment = async (taskId) => {
  try {
    const updated = await taskService.deleteAttachment(taskId)
    addToast('Lampiran tugas berhasil dihapus')
    if (detailTask.value && detailTask.value.id === taskId) {
      detailTask.value = updated
    }
    refreshAll()
  } catch (err) {
    addToast(err.message || 'Gagal menghapus lampiran', 'error')
  }
}

const handleOpenDelete = (task) => {
  taskToDelete.value = task
  isConfirmOpen.value = true
}

const handleConfirmDelete = async () => {
  if (!taskToDelete.value) return
  isDeleting.value = true
  try {
    await taskService.deleteTask(taskToDelete.value.id)
    addToast(`Tugas "${taskToDelete.value.title}" berhasil dihapus.`)
    isConfirmOpen.value = false
    if (detailTask.value && detailTask.value.id === taskToDelete.value.id) {
      isDetailOpen.value = false
      detailTask.value = null
    }
    taskToDelete.value = null
    refreshAll()
  } catch (err) {
    addToast(err.message || 'Gagal menghapus tugas', 'error')
  } finally {
    isDeleting.value = false
  }
}

const handleFilterStatus = (statusVal) => {
  isOverdueFilter.value = false
  selectedStatus.value = statusVal || ''
}

const handleFilterOverdue = () => {
  selectedStatus.value = ''
  isOverdueFilter.value = true
}

const handleResetFilters = () => {
  search.value = ''
  selectedStatus.value = ''
  selectedPriority.value = ''
  selectedCategory.value = ''
  isOverdueFilter.value = false
  sortBy.value = 'created_at'
  order.value = 'desc'
}

// Export tasks to CSV
const exportToCSV = () => {
  if (tasks.value.length === 0) {
    addToast('Tidak ada data tugas untuk diekspor', 'info')
    return
  }

  const headers = ['ID', 'Judul', 'Kategori', 'Prioritas', 'Status', 'Tenggat Waktu (WIB)', 'Lampiran', 'Deskripsi']
  const rows = tasks.value.map((t) => [
    t.id,
    `"${(t.title || '').replace(/"/g, '""')}"`,
    `"${(t.category || '').replace(/"/g, '""')}"`,
    t.priority,
    t.status,
    t.due_date ? `"${formatIndonesianDateTime(t.due_date, true)}"` : '-',
    `"${(t.attachment_name || '-').replace(/"/g, '""')}"`,
    `"${(t.description || '').replace(/"/g, '""')}"`,
  ])

  const csvContent =
    'data:text/csv;charset=utf-8,\uFEFF' +
    [headers.join(','), ...rows.map((e) => e.join(','))].join('\n')

  const encodedUri = encodeURI(csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', `daftar_tugas_cimb_niaga_${new Date().toISOString().slice(0, 10)}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  addToast('Data tugas berhasil diekspor ke format CSV!')
}

onMounted(() => {
  refreshAll()
})
</script>

<template>
  <div class="min-h-screen flex flex-col bg-slate-50 text-slate-800">
    <!-- Navbar Header -->
    <Navbar :stats="stats" @open-create="handleOpenCreate" />

    <!-- Main Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-8">
      
      <!-- Stats Dashboard -->
      <StatsCards
        :stats="stats"
        :active-status="selectedStatus"
        @filter-status="handleFilterStatus"
        @filter-overdue="handleFilterOverdue"
      />

      <!-- Action & Filter Bar -->
      <FilterBar
        v-model:search="search"
        v-model:selectedStatus="selectedStatus"
        v-model:selectedPriority="selectedPriority"
        v-model:selectedCategory="selectedCategory"
        v-model:sortBy="sortBy"
        v-model:order="order"
        v-model:viewMode="viewMode"
        :categories="categories"
        @reset-filters="handleResetFilters"
      />

      <!-- Content Area Header (Count & Export) -->
      <div class="flex items-center justify-between mb-4 px-1">
        <div class="flex items-center gap-2 text-xs sm:text-sm text-slate-500 font-medium flex-wrap">
          <span>Menampilkan <strong>{{ tasks.length }}</strong> tugas</span>
          <span
            v-if="statusFilterLabel"
            class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-cimb-50 text-cimb-800 border border-cimb-200 text-xs font-semibold"
          >
            <span>Filter: {{ statusFilterLabel }}</span>
            <button
              @click="selectedStatus = ''"
              class="hover:text-cimb-950 font-bold ml-0.5 text-xs text-cimb-600"
              title="Hapus filter status"
            >
              ✕
            </button>
          </span>
          <span
            v-if="isOverdueFilter"
            class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-700 text-xs font-semibold"
          >
            <span>Filter: Lewat Deadline</span>
            <button
              @click="isOverdueFilter = false"
              class="hover:text-rose-950 font-bold ml-0.5 text-xs text-rose-600"
              title="Hapus filter deadline"
            >
              ✕
            </button>
          </span>
        </div>

        <div class="flex items-center gap-2">
          <!-- Refresh Button -->
          <button
            @click="refreshAll"
            class="p-2 text-slate-500 hover:text-cimb-800 hover:bg-cimb-50 rounded-xl transition-colors"
            title="Refresh Data"
          >
            <RefreshCw :class="['w-4 h-4', isLoading ? 'animate-spin' : '']" />
          </button>

          <!-- Export CSV Button -->
          <button
            @click="exportToCSV"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-medium rounded-xl shadow-xs transition-colors"
            title="Ekspor ke Excel / CSV"
          >
            <Download class="w-3.5 h-3.5" />
            <span class="hidden sm:inline">Ekspor CSV</span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="py-20 flex flex-col items-center justify-center">
        <Loader2 class="w-8 h-8 text-cimb-800 animate-spin" />
        <p class="text-sm text-slate-500 mt-3 font-medium">Memuat tugas harian...</p>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="tasks.length === 0"
        class="bg-white border border-slate-200/80 rounded-2xl p-12 text-center shadow-xs my-6"
      >
        <div class="w-14 h-14 bg-cimb-50 text-cimb-800 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <Inbox class="w-7 h-7 stroke-[1.8]" />
        </div>
        <h3 class="text-base font-bold text-slate-900">Belum Ada Tugas Yang Sesuai</h3>
        <p class="text-xs sm:text-sm text-slate-500 max-w-sm mx-auto mt-1 leading-relaxed">
          {{
            search || selectedStatus || selectedPriority || selectedCategory || isOverdueFilter
              ? 'Tidak ditemukan tugas dengan kriteria filter saat ini. Coba reset filter atau ubah kata kunci pencarian.'
              : 'Daftar tugas harian Anda masih kosong. Mulai rencanakan hari Anda dengan menambahkan tugas pertama!'
          }}
        </p>
        <div class="mt-5 flex items-center justify-center gap-3">
          <button
            v-if="search || selectedStatus || selectedPriority || selectedCategory || isOverdueFilter"
            @click="handleResetFilters"
            class="px-4 py-2 text-xs font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors"
          >
            Reset Semua Filter
          </button>
          <button
            @click="handleOpenCreate"
            class="inline-flex items-center gap-2 px-4 py-2 bg-cimb-800 hover:bg-cimb-900 text-white text-xs font-semibold rounded-xl shadow-xs transition-colors"
          >
            <ListPlus class="w-4 h-4" />
            <span>Tambah Tugas Pertama</span>
          </button>
        </div>
      </div>

      <!-- Grid View -->
      <div
        v-else-if="viewMode === 'grid'"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5"
      >
        <TaskCard
          v-for="task in tasks"
          :key="task.id"
          :task="task"
          @toggle-status="handleToggleStatus"
          @change-status="handleChangeStatus"
          @view="handleViewTask"
          @edit="handleOpenEdit"
          @delete="handleOpenDelete"
        />
      </div>

      <!-- Table View -->
      <TaskTable
        v-else
        :tasks="tasks"
        @toggle-status="handleToggleStatus"
        @change-status="handleChangeStatus"
        @view="handleViewTask"
        @edit="handleOpenEdit"
        @delete="handleOpenDelete"
      />
    </main>

    <!-- Footer -->
    <footer class="mt-auto border-t border-slate-200/80 bg-white py-5 text-center text-xs text-slate-500">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
        <p>© 2026 PT Bank CIMB Niaga Tbk - Modul Pengelolaan Tugas Harian (TaskFlow).</p>
        <div class="flex items-center gap-4 text-xs font-medium text-slate-600">
          <a href="http://localhost:8000/docs" target="_blank" class="hover:text-cimb-800 transition-colors">
            API Swagger
          </a>
          <span>•</span>
          <a href="http://localhost:8000/redoc" target="_blank" class="hover:text-cimb-800 transition-colors">
            ReDoc
          </a>
          <span>•</span>
          <span>MySQL Database</span>
        </div>
      </div>
    </footer>

    <!-- Task Detail Modal (Lihat Rincian Tugas & Lampiran) -->
    <TaskDetailModal
      :isOpen="isDetailOpen"
      :task="detailTask"
      @close="isDetailOpen = false; detailTask = null"
      @edit="isDetailOpen = false; handleOpenEdit($event)"
      @toggle-status="handleToggleStatus"
      @upload-attachment="handleUploadAttachment"
      @delete-attachment="handleDeleteAttachment"
    />

    <!-- Task Create/Edit Modal -->
    <TaskModal
      :isOpen="isModalOpen"
      :task="editingTask"
      :categories="categories"
      :isSubmitting="isSubmitting"
      @close="isModalOpen = false"
      @save="handleSaveTask"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :isOpen="isConfirmOpen"
      :title="'Hapus Tugas'"
      :message="`Apakah Anda yakin ingin menghapus tugas '${taskToDelete?.title}' secara permanen?`"
      :isDeleting="isDeleting"
      @close="isConfirmOpen = false"
      @confirm="handleConfirmDelete"
    />

    <!-- Toast Notification Container -->
    <Toast :toasts="toasts" @remove="removeToast" />
  </div>
</template>
