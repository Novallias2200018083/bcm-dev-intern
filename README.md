# CIMB NIAGA — Modul Web Pengelolaan Tugas Harian (TaskFlow)

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.115+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/Database-MySQL%208.0-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Vue.js](https://img.shields.io/badge/Frontend-Vue.js%203-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS%203.4-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Vite](https://img.shields.io/badge/Bundler-Vite%206-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-7E1322?style=flat-square)](#)

Aplikasi web modern, responsif, dan *enterprise-ready* dengan identitas korporat resmi **PT Bank CIMB Niaga Tbk** untuk mencatat, mengelola, memantau, dan mengevaluasi daftar tugas harian tim secara terstruktur.

Dibangun dengan arsitektur bersih (*Clean Architecture*): **Python (FastAPI)** pada sisi Backend, **MySQL 8.0 (Laragon)** sebagai basis data relasional berkinerja tinggi, dan **Vue.js 3 (Composition API `<script setup>` + Tailwind CSS)** pada sisi Frontend.

---

## DAFTAR ISI

1. [Ringkasan & Nilai Bisnis](#-ringkasan--nilai-bisnis)
2. [Fitur-Fitur Utama](#-fitur-fitur-utama)
3. [Tumpukan Teknologi (Tech Stack)](#-tumpukan-teknologi-tech-stack)
4. [Struktur Direktori Proyek](#-struktur-direktori-proyek)
5. [Panduan Instalasi & Menjalankan Sistem](#-panduan-instalasi--menjalankan-sistem)
6. [Spesifikasi RESTful API & Swagger UI](#-spesifikasi-restful-api--swagger-ui)
7. [Pengujian Kualitas (QA & Postman Suite)](#-pengujian-kualitas-qa--postman-suite)
8. [Indeks Dokumentasi Teknis](#-indeks-dokumentasi-teknis)
9. [Kontributor](#-kontributor)

---

## 💼 Ringkasan & Nilai Bisnis

Dalam operasional perbankan yang dinamis, kedisiplinan pemenuhan batas waktu kerja (*Service Level Agreement* / SLA) merupakan faktor penentu kepuasan nasabah dan keunggulan operasional. **TaskFlow CIMB Niaga** dirancang untuk menjawab kebutuhan tersebut melalui:

* **Transparansi Kinerja SLA**: Memisahkan secara otomatis tugas yang diselesaikan tepat waktu (*On-Time*) dengan tugas yang diselesaikan lewat tenggat (*Late*).
* **Integritas Waktu Lokal**: Penanganan waktu lokal Indonesia (Waktu Indonesia Barat / WIB) yang murni dan bebas dari pergeseran offset UTC.
* **Sentralisasi Berkas Kerja**: Pengelolaan berkas pendukung (dokumen dan gambar) langsung di dalam kartu tugas.
* **Kepatuhan Brand Identity**: Mengusung warna solid *CIMB Burgundy Red* (`#7E1322`), tanpa gradasi warna acak, rapi, dan sesuai dengan standar antarmuka perbankan.

---

## 🌟 Fitur-Fitur Utama

### 1. Identitas Visual Korporat Bank CIMB Niaga
* Palet warna resmi solid **CIMB Burgundy Red** (`#7E1322`) pada pita header, tombol aksi primer, ikon aktif, dan elemen branding.
* Tipografi korporat yang bersih, kontras tinggi, dan nyaman dibaca.
* Tidak menggunakan warna gradasi sembarangan guna menjaga kesan elegan dan formal.

### 2. Pengelolaan Tugas Lengkap (Full CRUD)
* **Tambah Tugas Baru**: Formulir lengkap mencakup judul, rincian instruksi, kategori, prioritas (*Low*, *Medium*, *High*), batas waktu (*due date* WIB), serta lampiran berkas langsung.
* **Edit Tugas**: Pembaruan data tugas kapan saja dengan sinkronisasi waktu lokal murni.
* **Hapus Tugas**: Dilengkapi modal konfirmasi keamanan untuk mencegah penghapusan data secara tidak sengaja.
* **Ubah Status Instan**: Centang tombol *checkbox* atau ubah melalui *pill dropdown* untuk mengubah status secara *real-time*.

### 3. Pemantauan SLA: Selesai Tepat Waktu vs Terlambat
Sistem secara otomatis menghitung selisih waktu penyelesaian dengan deadline:
* **Selesai Tepat Waktu (*On-Time Completion*)**: Ditandai dengan badge hijau (*CheckCircle2*) untuk tugas yang diselesaikan $\le$ tenggat waktu atau tugas tanpa tenggat khusus.
* **Selesai Terlambat (*Late Completion*)**: Ditandai dengan badge oranye/amber (*Timer*) untuk tugas yang diselesaikan setelah melewati batas tenggat waktu.

### 4. Dashboard Metrik & Analitik Kinerja (5 Kartu Interaktif)
* **Total Tugas**: Jumlah seluruh tugas terdaftar.
* **Menunggu**: Tugas dalam antrean awal pengerjaan.
* **Dikerjakan**: Tugas yang sedang dalam proses eksekusi.
* **Tepat Waktu**: Metrik tugas tepat waktu dilengkapi persentase (%) dan progress bar visual hijau.
* **Selesai Terlambat**: Metrik tugas terlambat dilengkapi persentase (%) dan progress bar visual oranye.
* **Active Filter Ring**: Mengklik salah satu kartu metrik akan langsung menyaring daftar tugas dan menyalakan ring sorotan aktif pada kartu tersebut.

### 5. Lampiran Berkas Dokumen & Gambar (Attachment Subsystem)
* **Pratinjau Gambar Langsung (*Image Preview*)**: Jika berkas berupa gambar (PNG, JPG, JPEG, WEBP), gambar langsung dirender pada modal detail dengan opsi buka layar penuh (*full screen*).
* **Dukungan Dokumen Multifformat**: Mendukung file PDF, Word (.docx), Excel (.xlsx), dan berkas teks dengan batas ukuran aman hingga 10 MB.
* **Aksi Berkas**: Dilengkapi tombol unduh (*download*), ganti berkas (*replace*), dan hapus berkas lampiran.

### 6. Waktu Indonesia Barat (WIB) & Jam Digital Live
* Seluruh pencatatan waktu (*created_at*, *due_date*, *completed_at*) disinkronkan ke zona waktu **WIB (UTC+7)**.
* Header navigasi memuat jam digital *real-time* yang berdetik setiap detik beserta penanggalan lengkap berbahasa Indonesia.

### 7. Pencarian Real-Time & Penyaringan Fleksibel
* Kolom pencarian teks dengan teknik *debouncing* (300 ms) pada judul, catatan, dan kategori.
* Filter berdasarkan status pengerjaan, kategori dinamis, dan tingkat prioritas.
* Pengurutan (*sorting*) berdasarkan tanggal dibuat, tenggat waktu, prioritas, atau abjad judul.

### 8. Fleksibilitas Tampilan (Grid & Table View)
* **Grid View**: Tampilan kartu modern simetris yang lega dan informatif.
* **Table View**: Tampilan tabel ringkas ala spreadsheet perbankan.

### 9. Desain Responsif Lintas Perangkat (Mobile-Friendly)
* Antarmuka dioptimalkan secara presisi untuk berbagai resolusi layar: Smartphone (360px - 480px), Tablet (768px), hingga Layar Desktop lebar.
* Area sentuh (*touch target*) ergonomis untuk kenyamanan navigasi jari di perangkat bergerak tanpa ada elemen yang terpotong ke samping (*zero horizontal scrollbar*).

### 10. Ekspor Data ke Format CSV / Excel
* Ekspor seluruh data tugas harian ke dalam berkas `.csv` (kompatibel penuh dengan Microsoft Excel) hanya dengan 1-klik.

---

## 🛠️ Tumpukan Teknologi (Tech Stack)

### Backend (Python Web)
* **Bahasa**: Python 3.10+
* **Framework Web**: **FastAPI** (Performa tinggi, asinkron, validasi tipe otomatis)
* **ORM & Database Driver**: **SQLAlchemy 2.0** + **PyMySQL** + **Cryptography**
* **Validasi Skema**: **Pydantic v2** + **pydantic-settings**
* **Pengelola File Upload**: **python-multipart**
* **Server Produksi**: **Uvicorn** ASGI Server

### Frontend (Vue.js Web)
* **Framework**: **Vue.js 3** (Composition API `<script setup>`)
* **Build Tool**: **Vite 6** (*Lightning-fast Hot Module Replacement*)
* **Styling**: **Tailwind CSS 3.4** (Palet warna kustom CIMB Niaga)
* **Icon Library**: **Lucide Icons** (`lucide-vue-next`)
* **HTTP Client**: **Axios** (Dikonfigurasi dengan proxy Vite `/api` dan `/uploads`)

### Database
* **RDBMS**: **MySQL 8.0+** (Laragon MySQL Server pada port `3306`)
* **Nama Database**: `daily_tasks_db`
* **Karakter Set**: `utf8mb4_unicode_ci`

---

## 📁 Struktur Direktori Proyek

```
bcm-dev-intern/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py           # Konfigurasi aplikasi & database (.env)
│   │   │   └── database.py         # SQLAlchemy engine, session pool, & Base
│   │   ├── crud/
│   │   │   └── task.py             # Layer query DB, filter dinamis, & agregasi
│   │   ├── models/
│   │   │   └── task.py             # Model tabel tasks SQLAlchemy & status SLA
│   │   ├── routers/
│   │   │   └── task.py             # Endpoint REST API & upload file handler
│   │   ├── schemas/
│   │   │   └── task.py             # Validasi input/output schema Pydantic v2
│   │   └── main.py                 # FastAPI entrypoint, CORS, auto-seed, & static
│   ├── uploads/                    # Direktori penyimpanan berkas gambar & dokumen
│   ├── generate_docx.py            # Skrip pembuat dokumen resmi Word (.docx)
│   ├── .env                        # Konfigurasi environment aktif
│   ├── requirements.txt            # Daftar paket dependensi Python
│   └── seed.py                     # Skrip mandiri seed data awal
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ConfirmModal.vue    # Modal konfirmasi keamanan hapus data
│   │   │   ├── FilterBar.vue       # Komponen filter, pencarian, & view toggle
│   │   │   ├── Navbar.vue          # Header resmi CIMB & jam digital live WIB
│   │   │   ├── StatsCards.vue      # 5 kartu metrik analitik KPI tugas
│   │   │   ├── TaskCard.vue        # Kartu tugas grid modern & terstruktur
│   │   │   ├── TaskDetailModal.vue # Modal rincian tugas & pratinjau gambar
│   │   │   ├── TaskModal.vue       # Form tambah/edit tugas (dropdown native)
│   │   │   ├── TaskTable.vue       # Tampilan tabel korporat alternatif
│   │   │   └── Toast.vue           # Notifikasi status mengambang
│   │   ├── services/
│   │   │   ├── api.js              # Instance Axios terpusat
│   │   │   └── taskService.js      # Kumpulan fungsi pemanggil endpoint REST API
│   │   ├── utils/
│   │   │   └── dateFormatter.js    # Modul pembaca waktu lokal lossless Indonesia
│   │   ├── App.vue                 # Komponen utama & pengelola state aplikasi
│   │   └── main.js                 # Mount aplikasi Vue 3
│   ├── index.html                  # Berkas HTML utama
│   ├── package.json                # Dependensi frontend & script build
│   ├── tailwind.config.js          # Kustomisasi tema & warna CIMB Burgundy Red
│   └── vite.config.js              # Konfigurasi Vite & proxy backend (/api, /uploads)
├── docs/                           # Dokumentasi teknis lengkap proyek
│   ├── DOKUMENTASI_ALUR_KERJA_DEVELOPER.docx   # Dokumen Word alur kerja developer
│   ├── DOKUMENTASI_ALUR_KERJA_DEVELOPER.md     # Dokumen Markdown alur kerja developer
│   ├── TaskFlow_CIMB_Niaga.postman_collection.json # Suite koleksi otomatis Postman
│   ├── API_DOCUMENTATION.md        # Spesifikasi teknis REST API
│   ├── ARCHITECTURE.md             # Arsitektur sistem & skema database
│   └── FLOWCHART.md                # Diagram alur logika pengerjaan tugas
└── README.md                       # Dokumentasi utama repositori
```

---

## 🚀 Panduan Instalasi & Menjalankan Sistem

### 1. Prasyarat Sistem (Prerequisites)
Pastikan komputer telah terpasang:
* **Python 3.10** atau lebih baru
* **Node.js 18** atau lebih baru & npm
* **MySQL Server** (direkomendasikan melalui **Laragon**)

---

### 2. Persiapan Basis Data MySQL
1. Jalankan aplikasi **Laragon** dan klik **Start All** (pastikan modul MySQL aktif pada port `3306`).
2. Buat database baru bernama `daily_tasks_db` melalui HeidiSQL atau terminal MySQL:
   ```sql
   CREATE DATABASE daily_tasks_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

---

### 3. Menjalankan Backend (FastAPI)
1. Buka terminal baru dan arahkan ke direktori `backend`:
   ```bash
   cd c:\laragon\www\bcm-dev-intern\backend
   ```
2. Aktifkan virtual environment Python:
   ```bash
   # Windows PowerShell / CMD:
   venv\Scripts\activate
   ```
   *(Jika belum pernah membuat virtual environment, jalankan: `python -m venv venv` lalu `pip install -r requirements.txt`)*.

3. Jalankan server backend menggunakan Uvicorn:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
4. Server backend aktif di: **`http://localhost:8000`**.  
   *Tabel `tasks` dan 5 data tugas awal realistis akan otomatis diinisialisasi saat pertama kali dijalankan.*

---

### 4. Menjalankan Frontend (Vue.js 3 + Vite)
1. Buka jendela terminal kedua dan arahkan ke direktori `frontend`:
   ```bash
   cd c:\laragon\www\bcm-dev-intern\frontend
   ```
2. Jalankan development server:
   ```bash
   npm run dev
   ```
3. Buka peramban (browser) dan akses alamat:
   👉 **`http://localhost:5173`**

---

## 📡 Spesifikasi RESTful API & Swagger UI

FastAPI menyediakan dokumentasi antarmuka interaktif yang dapat diuji langsung melalui browser:
* **Interactive Swagger UI**: [`http://localhost:8000/docs`](http://localhost:8000/docs)
* **Alternative ReDoc UI**: [`http://localhost:8000/redoc`](http://localhost:8000/redoc)

### Ringkasan Endpoint Utama

| Method | Endpoint | Deskripsi | Tipe Request | Kode Status Sukses |
|:---:|---|---|---|:---:|
| `GET` | `/api/tasks/stats` | Mengambil statistik metrik tugas (Total, Pending, Selesai, Tepat Waktu, Terlambat) | - | `200 OK` |
| `GET` | `/api/tasks/categories` | Mengambil daftar opsi kategori tugas dinamis | - | `200 OK` |
| `GET` | `/api/tasks` | Mengambil daftar tugas (mendukung filter status, kategori, prioritas, pencarian, & sorting) | Query params | `200 OK` |
| `GET` | `/api/tasks/{id}` | Mengambil rincian detail 1 tugas berdasarkan ID | Path param | `200 OK` |
| `POST` | `/api/tasks` | Membuat tugas harian baru | `application/json` | `201 Created` |
| `PUT` | `/api/tasks/{id}` | Memperbarui seluruh/sebagian data tugas | `application/json` | `200 OK` |
| `PATCH` | `/api/tasks/{id}/status` | Mengubah status pengerjaan tugas secara instan | `application/json` | `200 OK` |
| `POST` | `/api/tasks/{id}/upload` | Mengunggah gambar atau berkas dokumen pendukung (Maks 10 MB) | `multipart/form-data` | `200 OK` |
| `DELETE` | `/api/tasks/{id}/attachment` | Menghapus berkas lampiran yang terpasang pada tugas | - | `200 OK` |
| `DELETE` | `/api/tasks/{id}` | Menghapus tugas secara permanen beserta berkas fisiknya | - | `204 No Content` |
| `GET` | `/api/health` | Health check koneksi sistem, database, dan zona waktu | - | `200 OK` |

---

## 🧪 Pengujian Kualitas (QA & Postman Suite)

Aplikasi ini telah melalui serangkaian pengujian perangkat lunak komprehensif mencakup validasi fungsional, performa SLA, kontrak data, dan penanganan kesalahan.

### 1. Postman Automated Test Collection
Tersedia koleksi pengujian otomatis siap pakai di berkas:  
📁 [`docs/TaskFlow_CIMB_Niaga.postman_collection.json`](file:///c:/laragon/www/bcm-dev-intern/docs/TaskFlow_CIMB_Niaga.postman_collection.json)

**Komponen Utama yang Divalidasi dalam Postman:**
1. **HTTP Status Code**: Memastikan respon mengembalikan `200 OK`, `201 Created`, `204 No Content`, atau `422 Unprocessable Entity` secara tepat.
2. **JSON Schema Contract**: Memastikan struktur objek, kehadiran atribut wajib (*mandatory fields*), dan tipe data sesuai spesifikasi.
3. **Data Integrity & Business Logic**: Memverifikasi formula SLA (tugas diselesaikan $\le$ deadline terhitung tepat waktu).
4. **Performance SLA**: Memastikan response time setiap endpoint berada di bawah ambang batas toleransi (latensi $< 300\text{ ms}$).
5. **Response Headers**: Memastikan keberadaan header `Content-Type: application/json` dan header keamanan.
6. **Error Handling**: Memastikan pesan error informatif dan tidak membocorkan informasi sensitif server/database.
7. **Request Chaining**: Menggunakan variabel environment Postman (`pm.environment.set("currentTaskId", res.id)`) untuk pengujian berantai dari `POST` $\rightarrow$ `GET` $\rightarrow$ `PATCH` $\rightarrow$ `DELETE`.

#### Cara Menjalankan Uji di Postman:
1. Buka aplikasi **Postman**.
2. Klik tombol **Import** dan pilih berkas `docs/TaskFlow_CIMB_Niaga.postman_collection.json`.
3. Klik kanan pada koleksi **CIMB Niaga - TaskFlow API Test Suite** lalu pilih **Run Collection**.
4. Seluruh skenario pengujian akan dieksekusi dengan hasil **Pass (100% Lolos)**.

---

### 2. Matriks Pengujian Fungsional

| Modul Pengujian | Skenario Uji | Hasil Verifikasi | Status |
|---|---|---|:---:|
| **Pencatatan Tugas** | Input judul, kategori, prioritas, deadline, dan simpan. | Data tersimpan ke MySQL dan tampil di urutan paling atas. | **LULUS** |
| **SLA Tepat Waktu** | Tandai selesai tugas yang deadline-nya di masa depan. | Status menjadi *Selesai Tepat Waktu* (badge hijau), kartu metrik bertambah. | **LULUS** |
| **SLA Terlambat** | Tandai selesai tugas yang deadline-nya di masa lalu. | Status menjadi *Selesai Terlambat* (badge oranye), kartu metrik bertambah. | **LULUS** |
| **Unggah Lampiran** | Unggah berkas gambar PNG/JPG atau PDF (maks 10 MB). | Berkas tersimpan di `/uploads`, pratinjau gambar tampil utuh, berkas dapat diunduh. | **LULUS** |
| **Validasi Ukuran File** | Coba unggah file dengan ukuran $> 10\text{ MB}$. | Sistem menolak upload dengan pesan error HTTP 400 Bad Request. | **LULUS** |
| **Pencarian Real-Time** | Ketik kata kunci pada input pencarian (debounced 300ms). | Daftar tugas menyaring data instan tanpa kedipan/flicker pada layar. | **LULUS** |
| **Responsivitas Layar HP** | Uji viewport mobile (360px - 414px). | Tampilan kartu simetris 1 kolom, teks rapi, tombol sentuh ergonomis. | **LULUS** |

---

## 📚 Indeks Dokumentasi Teknis

Untuk mempelajari perancangan sistem secara lebih mendalam, silakan merujuk pada berkas dokumentasi teknis di dalam direktori `docs/`:

* 📄 **[DOKUMENTASI_ALUR_KERJA_DEVELOPER.md](file:///c:/laragon/www/bcm-dev-intern/docs/DOKUMENTASI_ALUR_KERJA_DEVELOPER.md)**: Catatan alur kerja pengembangan komprehensif dari sudut pandang pengembang (*First-Person Developer Perspective*), mulai dari arsitektur, coding langkah demi langkah, troubleshooting, hingga jawaban lengkap soal QA.
* 📁 **[DOKUMENTASI_ALUR_KERJA_DEVELOPER_V2.docx](file:///c:/laragon/www/bcm-dev-intern/docs/DOKUMENTASI_ALUR_KERJA_DEVELOPER_V2.docx)**: Dokumen resmi format Microsoft Word lengkap dengan kop laporan Bank CIMB Niaga, tabel terformat, dan kotak kode program.
* 🌐 **[API_DOCUMENTATION.md](file:///c:/laragon/www/bcm-dev-intern/docs/API_DOCUMENTATION.md)**: Spesifikasi teknis seluruh endpoint REST API, struktur payload JSON, query params, dan contoh cURL.
* 🏗️ **[ARCHITECTURE.md](file:///c:/laragon/www/bcm-dev-intern/docs/ARCHITECTURE.md)**: Rancangan arsitektur perangkat lunak, diagram lapisan aplikasi, dan skema database relasional.
* 📊 **[FLOWCHART.md](file:///c:/laragon/www/bcm-dev-intern/docs/FLOWCHART.md)**: Diagram alur logika pengerjaan tugas, evaluasi SLA, dan alur unggah berkas.
* 📦 **[TaskFlow_CIMB_Niaga.postman_collection.json](file:///c:/laragon/www/bcm-dev-intern/docs/TaskFlow_CIMB_Niaga.postman_collection.json)**: Berkas koleksi otomatis Postman untuk pengujian API.

---

## 👨‍💻 Kontributor

Proyek ini dirancang dan dikembangkan sebagai bagian dari **Technical Assessment / Internship Programming Assignment** untuk posisi Pengembang Perangkat Lunak di **PT Bank CIMB Niaga Tbk**.

* **Author**: Full-Stack Web Developer Candidate
* **Email / Kontak**: Tim Rekrutmen & Pengembangan Bakat PT Bank CIMB Niaga Tbk
* **Tahun Pembuatan**: November 2026
* **Lisensi**: Hak cipta milik PT Bank CIMB Niaga Tbk (Internal Use Only)
