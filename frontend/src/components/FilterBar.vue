<script setup>
import {
  Search,
  X,
  LayoutGrid,
  List,
} from 'lucide-vue-next'

const props = defineProps({
  search: {
    type: String,
    default: '',
  },
  selectedStatus: {
    type: String,
    default: '',
  },
  selectedPriority: {
    type: String,
    default: '',
  },
  selectedCategory: {
    type: String,
    default: '',
  },
  sortBy: {
    type: String,
    default: 'created_at',
  },
  order: {
    type: String,
    default: 'desc',
  },
  viewMode: {
    type: String,
    default: 'grid', // 'grid' | 'table'
  },
  categories: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits([
  'update:search',
  'update:selectedStatus',
  'update:selectedPriority',
  'update:selectedCategory',
  'update:sortBy',
  'update:order',
  'update:viewMode',
  'reset-filters',
])

const statusOptions = [
  { value: '', label: 'Semua Status' },
  { value: 'pending', label: 'Menunggu' },
  { value: 'in_progress', label: 'Dikerjakan' },
  { value: 'completed', label: 'Selesai (Semua)' },
  { value: 'completed_on_time', label: 'Selesai: Tepat Waktu' },
  { value: 'completed_late', label: 'Selesai: Terlambat' },
]

const priorityOptions = [
  { value: '', label: 'Semua Prioritas' },
  { value: 'high', label: 'Prioritas: Tinggi' },
  { value: 'medium', label: 'Prioritas: Sedang' },
  { value: 'low', label: 'Prioritas: Rendah' },
]

const sortOptions = [
  { value: 'created_at:desc', label: 'Dibuat: Terbaru' },
  { value: 'created_at:asc', label: 'Dibuat: Terlama' },
  { value: 'due_date:asc', label: 'Deadline: Terdekat' },
  { value: 'due_date:desc', label: 'Deadline: Terjauh' },
  { value: 'priority:desc', label: 'Prioritas Tertinggi' },
  { value: 'title:asc', label: 'Judul (A - Z)' },
]

const handleSortChange = (e) => {
  const [col, ord] = e.target.value.split(':')
  emit('update:sortBy', col)
  emit('update:order', ord)
}
</script>

<template>
  <div class="bg-white rounded-2xl border border-slate-200/80 shadow-xs p-3.5 sm:p-5 mb-5 sm:mb-6">
    <div class="flex flex-col lg:flex-row gap-3 sm:gap-4 items-stretch lg:items-center justify-between">
      
      <!-- Search Input (Full width on mobile) -->
      <div class="relative flex-1 min-w-[220px]">
        <Search class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
        <input
          :value="search"
          @input="emit('update:search', $event.target.value)"
          type="text"
          placeholder="Cari tugas berdasarkan judul, catatan, atau kategori..."
          class="w-full pl-10 pr-9 py-2 sm:py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 focus:bg-white transition-all"
        />
        <button
          v-if="search"
          @click="emit('update:search', '')"
          class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 p-0.5 rounded-full hover:bg-slate-200/50"
        >
          <X class="w-3.5 h-3.5" />
        </button>
      </div>

      <!-- Filters & Actions (Grid 2-col on mobile, flex row on sm/md/lg) -->
      <div class="grid grid-cols-2 sm:flex sm:flex-wrap items-center gap-2 sm:gap-2.5">
        <!-- Status Filter -->
        <select
          :value="selectedStatus"
          @change="emit('update:selectedStatus', $event.target.value)"
          class="w-full sm:w-auto py-2 sm:py-2.5 px-2.5 sm:px-3 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm font-medium text-slate-700 hover:bg-slate-100/70 focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 cursor-pointer truncate"
        >
          <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>

        <!-- Category Filter -->
        <select
          :value="selectedCategory"
          @change="emit('update:selectedCategory', $event.target.value)"
          class="w-full sm:w-auto py-2 sm:py-2.5 px-2.5 sm:px-3 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm font-medium text-slate-700 hover:bg-slate-100/70 focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 cursor-pointer truncate"
        >
          <option value="">Semua Kategori</option>
          <option v-for="cat in categories" :key="cat" :value="cat">
            {{ cat }}
          </option>
        </select>

        <!-- Priority Filter -->
        <select
          :value="selectedPriority"
          @change="emit('update:selectedPriority', $event.target.value)"
          class="w-full sm:w-auto py-2 sm:py-2.5 px-2.5 sm:px-3 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm font-medium text-slate-700 hover:bg-slate-100/70 focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 cursor-pointer truncate"
        >
          <option v-for="opt in priorityOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>

        <!-- Sorting -->
        <select
          :value="`${sortBy}:${order}`"
          @change="handleSortChange"
          class="w-full sm:w-auto py-2 sm:py-2.5 px-2.5 sm:px-3 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm font-medium text-slate-700 hover:bg-slate-100/70 focus:outline-none focus:ring-2 focus:ring-cimb-800/15 focus:border-cimb-700 cursor-pointer truncate"
        >
          <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>

        <!-- Controls Row for Mobile: View Mode Toggle & Reset -->
        <div class="col-span-2 sm:col-span-1 flex items-center justify-between sm:justify-start gap-2 pt-1 sm:pt-0">
          <!-- View Toggle (Grid / Table) -->
          <div class="flex items-center p-1 bg-slate-100 rounded-xl border border-slate-200/80">
            <button
              @click="emit('update:viewMode', 'grid')"
              :class="[
                'p-1.5 rounded-lg text-xs font-medium transition-all',
                viewMode === 'grid'
                  ? 'bg-white text-cimb-800 shadow-xs'
                  : 'text-slate-500 hover:text-slate-800'
              ]"
              title="Tampilan Grid Kartu"
            >
              <LayoutGrid class="w-4 h-4" />
            </button>
            <button
              @click="emit('update:viewMode', 'table')"
              :class="[
                'p-1.5 rounded-lg text-xs font-medium transition-all',
                viewMode === 'table'
                  ? 'bg-white text-cimb-800 shadow-xs'
                  : 'text-slate-500 hover:text-slate-800'
              ]"
              title="Tampilan Tabel Rinci"
            >
              <List class="w-4 h-4" />
            </button>
          </div>

          <!-- Reset Button if any filter active -->
          <button
            v-if="search || selectedStatus || selectedPriority || selectedCategory"
            @click="emit('reset-filters')"
            class="px-2.5 py-1.5 sm:py-2 text-xs font-semibold text-cimb-700 hover:text-cimb-800 hover:bg-cimb-50 rounded-lg transition-colors flex items-center gap-1 shrink-0"
            title="Reset semua filter"
          >
            <X class="w-3.5 h-3.5" />
            <span>Reset Filter</span>
          </button>
        </div>
      </div>

    </div>
  </div>
</template>
