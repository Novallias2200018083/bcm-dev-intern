# CIMB NIAGA - Modul Web Pengelolaan Tugas Harian (TaskFlow)

Aplikasi web modern, responsif, dan *enterprise-ready* dengan identitas korporat resmi **PT Bank CIMB Niaga Tbk** untuk mencatat, mengelola, dan memantau daftar tugas harian. Dibangun dengan **Python (FastAPI)** pada sisi Backend, **Vue.js 3** pada sisi Frontend, dan **MySQL 8.0** sebagai basis data relasional.

---

## 🌟 Fitur Utama

- **Identitas Visual Korporat Bank CIMB Niaga**:
  - Palet warna resmi solid *CIMB Burgundy Red* (`#7E1322`) tanpa gradasi, pita aksen header, tombol aksi utama (*Primary Solid Red Button*), dan elemen status aktif.
  - Logo emblem khas CIMB serta tipografi korporat yang elegan, bersih, dan profesional.
- **Pengelolaan Tugas Lengkap (Full CRUD)**:
  - **Tambah Tugas Baru**: Judul tugas, kategori (dropdown native + opsi tambah kategori mandiri), tingkat prioritas (*Low*, *Medium*, *High*), batas waktu pengerjaan (*due date* lokal WIB), catatan instruksi, serta lampiran dokumen/gambar awal.
  - **Edit Tugas**: Perbarui data tugas kapan saja secara fleksibel dengan sinkronisasi waktu lokal tanpa pergeseran zona waktu.
  - **Hapus Tugas**: Dilengkapi modal konfirmasi keamanan untuk mencegah penghapusan yang tidak disengaja.
  - **Ubah Status Cepat**: Tandai selesai atau buka kembali tugas hanya dengan 1-klik (*checkbox toggle* atau *status dropdown*).
- **Pemantauan Kinerja Tugas (Selesai Tepat Waktu vs Terlambat)**:
  - **Selesai Tepat Waktu (*On-Time Completion*)**: Ditandai dengan badge hijau (*CheckCircle2*) untuk tugas yang berhasil diselesaikan sebelum atau bertepatan dengan tenggat waktu.
  - **Selesai Terlambat (*Late Completion*)**: Ditandai dengan badge oranye/amber (*Timer*) untuk tugas yang diselesaikan setelah melewati batas tenggat waktu.
  - Dilengkapi kartu statistik terpisah pada dashboard untuk memudahkan pemantauan kedisiplinan dan SLA pekerjaan.
- **Lihat Rincian Tugas (Detail Modal View)**:
  - Menampilkan seluruh informasi tugas secara terstruktur: judul, deskripsi lengkap, tenggat waktu, waktu selesai, status ketepatan waktu (*Tepat Waktu / Terlambat*), kategori, dan prioritas.
  - Menghubungkan tugas dengan **dokumen atau gambar pendukung**.
- **Lampiran Dokumen & Gambar Pendukung (Attachment Subsystem)**:
  - **Pratinjau Gambar Langsung (*Image Preview*)**: Jika lampiran berupa gambar (PNG, JPG, JPEG, WEBP), gambar langsung ditampilkan di dalam modal detail dengan opsi perbesar layar penuh.
  - **Dukungan Dokumen (PDF, Word, Excel, TXT)**: Menampilkan kartu berkas lengkap dengan nama asli, ukuran file (KB/MB), serta tombol **Unduh / Buka Dokumen**.
  - **Pengelolaan Berkas Fleksibel**: Kemudahan mengunggah berkas baru, mengganti berkas, atau menghapus lampiran.
- **Dashboard Statistik & KPI Interaktif**:
  - Total tugas, tugas menunggu (*pending*), sedang dikerjakan (*in progress*), dan tugas selesai (*completed*).
  - Indikator persentase penyelesaian tugas (*visual progress bar*).
  - Deteksi otomatis tugas yang melewati batas tenggat waktu (*Overdue alert badge*).
- **Pencarian & Penyaringan Dinamis**:
  - Pencarian *real-time* (*debounced*) berdasarkan judul, catatan, atau kategori.
  - Filter berdasarkan Status, Tingkat Prioritas, dan Kategori.
  - Pengurutan (*sorting*) berdasarkan waktu pembuatan, batas deadline, prioritas, atau abjad judul.
- **Zona Waktu Indonesia (WIB) & Jam Real-Time**:
  - Seluruh pencatatan waktu (*created_at*, *due_date*, *completed_at*) diselaraskan penuh dengan zona waktu **Waktu Indonesia Barat (WIB / UTC+7)** tanpa pergeseran UTC.
  - Dilengkapi jam digital *live* real-time di bagian navigasi (berdetik setiap detik).
- **Desain Ultra-Responsif (Mobile, Tablet, & Desktop)**:
  - Tata letak dirancang khusus agar rapi dan nyaman digunakan di berbagai ukuran layar: smartphone (320px - 480px), tablet, hingga layar monitor desktop.
  - Elemen modal, form input, dan tombol aksi dioptimalkan dengan target sentuh (*touch-friendly*) yang ergonomis untuk pengguna ponsel.
- **Fleksibilitas Tampilan (Grid & Table View)**:
  - **Grid View**: Tampilan kartu visual modern dengan indikator lampiran.
  - **Table View**: Tampilan tabel ringkas ala spreadsheet korporat.
- **Ekspor Data**:
  - Ekspor seluruh daftar tugas ke dalam format **CSV / Excel** dalam satu klik.
- **Dokumentasi API Otomatis**:
  - Terintegrasi langsung dengan **Swagger UI** (`/docs`) dan **ReDoc** (`/redoc`).

---

## 🛠️ Teknologi yang Digunakan (Tech Stack)

### Backend (Python Web)
- **Language**: Python 3.10+
- **Framework**: **FastAPI** (Performa tinggi, asinkron, validasi tipe otomatis)
- **ORM & Database Driver**: **SQLAlchemy 2.0** + **PyMySQL** + **Cryptography**
- **Data Validation**: **Pydantic v2** + **pydantic-settings**
- **File Upload Handler**: **python-multipart**
- **Static File Serving**: **Starlette StaticFiles**
- **Server Engine**: **Uvicorn** ASGI Web Server

### Frontend (Vue.js Web)
- **Framework**: **Vue.js 3** (Composition API `<script setup>`)
- **Build Tool**: **Vite 6** (Super cepat untuk *Hot Module Replacement*)
- **Styling**: **Tailwind CSS 3.4** dengan kustomisasi palet warna CIMB Niaga
- **Iconography**: **Lucide Icons** (`lucide-vue-next`)
- **HTTP Client**: **Axios** (dengan *interceptor* penanganan error terpusat dan *multipart upload*)

### Database
- **DBMS**: **MySQL 8.0+** (Laragon MySQL)
- **Database Name**: `daily_tasks_db`
- **Tabel**: `tasks` (dilengkapi indeks performa)

---

## 📁 Struktur Direktori Proyek

```
bcm-dev-intern/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py         # Konfigurasi aplikasi, path upload, & DB (.env)
│   │   │   └── database.py       # Engine SQLAlchemy & session dependency
│   │   ├── crud/
│   │   │   └── task.py           # Layer query database & business logic
│   │   ├── models/
│   │   │   └── task.py           # Model tabel database SQLAlchemy
│   │   ├── routers/
│   │   │   └── task.py           # Endpoint REST API & file upload handler
│   │   ├── schemas/
│   │   │   └── task.py           # Validasi schema input & output Pydantic
│   │   └── main.py               # Entry point FastAPI, static mount, & auto seed
│   ├── uploads/                  # Direktori penyimpanan berkas gambar & dokumen
│   ├── .env                      # File konfigurasi environment aktif
│   ├── .env.example              # Template contoh konfigurasi
│   ├── requirements.txt          # Daftar dependensi Python
│   └── seed.py                   # Script mandiri untuk inisialisasi data contoh
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ConfirmModal.vue    # Modal konfirmasi hapus data
│   │   │   ├── FilterBar.vue       # Komponen filter, pencarian, & view toggle
│   │   │   ├── Navbar.vue          # Header navbar CIMB Niaga & tombol merah
│   │   │   ├── StatsCards.vue      # Kartu metrik KPI & progress bar
│   │   │   ├── TaskCard.vue        # Komponen kartu tugas dengan indikator lampiran
│   │   │   ├── TaskDetailModal.vue # Modal lihat rincian tugas & preview lampiran
│   │   │   ├── TaskModal.vue       # Modal form tambah & edit tugas + upload berkas
│   │   │   ├── TaskTable.vue       # Komponen tabel tugas ringkas
│   │   │   └── Toast.vue           # Notifikasi toast feedback
│   │   ├── services/
│   │   │   ├── api.js              # Axios client & error interceptor
│   │   │   └── taskService.js      # Service layer pemanggilan endpoint & upload
│   │   ├── App.vue                 # Komponen utama aplikasi
│   │   ├── main.js                 # Inisialisasi aplikasi Vue
│   │   └── style.css               # Tailwind directive & styling
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── database/
│   └── schema.sql                  # Skema DDL MySQL & data awal
├── docs/
│   ├── ARCHITECTURE.md             # Rancang arsitektur sistem & kamus data ERD
│   ├── FLOWCHART.md                # Diagram alur proses pengguna & alur berkas
│   └── API_DOCUMENTATION.md        # Spesifikasi lengkap REST API & cURL
├── run_backend.bat                 # Script 1-klik jalankan Backend
├── run_frontend.bat                # Script 1-klik jalankan Frontend
├── run_all.bat                     # Script 1-klik jalankan Backend & Frontend
└── README.md                       # Dokumentasi utama proyek
```

---

## 🚀 Panduan Menjalankan Aplikasi

### Opsi A: Cara Cepat (One-Click Launcher Windows)
1. Pastikan service **MySQL di Laragon** sudah berjalan (*Start All*).
2. Klik ganda (*double click*) file berikut:
   👉 **`run_all.bat`**

File ini otomatis membuka Backend dan Frontend di jendela terminal terpisah:
- **Backend API**: `http://localhost:8000`
- **Frontend App**: `http://localhost:5173`

---

### Opsi B: Cara Manual Melalui Terminal

#### 1. Persiapan Database MySQL
Pastikan server MySQL di Laragon / XAMPP sudah berjalan pada port 3306.
Database `daily_tasks_db` dan tabel `tasks` akan otomatis dibuat oleh sistem saat backend pertama kali dijalankan.

#### 2. Menjalankan Backend (Python FastAPI)
Buka terminal di root direktori proyek:
```bash
cd backend

# Aktifkan virtual environment
.\venv\Scripts\activate

# Jalankan server FastAPI
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Akses di browser:
- Swagger UI (Dokumentasi Interaktif API): **`http://localhost:8000/docs`**
- ReDoc: **`http://localhost:8000/redoc`**

#### 3. Menjalankan Frontend (Vue.js 3 + Vite)
Buka terminal baru di direktori `frontend`:
```bash
cd frontend

# Jalankan development server Vite
npm run dev
```
Akses di browser:
- Aplikasi Web TaskFlow: **`http://localhost:5173`**

---

## 📖 Dokumentasi Lengkap & Diagram Alur

Sistem ini telah dilengkapi dokumentasi teknis mendalam:

1. [Arsitektur Sistem & ERD Database](file:///c:/laragon/www/bcm-dev-intern/docs/ARCHITECTURE.md)
   - Penjelasan struktur arsitektur *Separation of Concerns* (Layered Architecture).
   - Entity Relationship Diagram (ERD) & Kamus Data (*Data Dictionary*) lengkap dengan kolom lampiran.
   - Analisis keamanan dan optimalisasi performa database indexing serta *clean storage cleanup*.
2. [Diagram Alur Sistem (Flowcharts)](file:///c:/laragon/www/bcm-dev-intern/docs/FLOWCHART.md)
   - Diagram alur interaksi pengguna (*User Flowchart*).
   - Diagram alur unggah dan pengelolaan berkas lampiran (*Attachment Flowchart*).
   - Diagram siklus perubahan status tugas (*State Transition*).
   - Diagram alur request HTTP, validasi schema, dan database query.
3. [Spesifikasi RESTful API](file:///c:/laragon/www/bcm-dev-intern/docs/API_DOCUMENTATION.md)
   - Detail seluruh endpoint: parameter, request body, upload berkas (*multipart/form-data*), response JSON, dan contoh pemanggilan via cURL.

---

## 🧪 Pengujian Sistem

Proyek ini telah melalui verifikasi pengujian menyeluruh:
1. **Pengujian Integrasi Backend**:
   - CRUD tugas harian berjalan 100% sukses terhubung ke MySQL 8.0.
   - Pydantic schema berhasil memvalidasi input judul kosong atau karakter tak valid.
   - Endpoint upload berkas berhasil menerima gambar dan dokumen, menyimpannya di `/uploads/`, serta menghapus berkas lama jika diganti.
   - Perhitungan metrik statistik (*KPI aggregation*) berjalan akurat secara real-time.
2. **Pengujian Frontend**:
   - Kompilasi Vite production build sukses tanpa error (`npm run build`).
   - Modal detail tugas, modal form tambah/edit, pratinjau gambar, pengunduh dokumen, konfirmasi hapus, filter, dan ekspor CSV berfungsi dengan lancar.
#   b c m - d e v - i n t e r n  
 