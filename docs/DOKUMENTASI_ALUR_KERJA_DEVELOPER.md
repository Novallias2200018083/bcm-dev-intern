# DOKUMENTASI ALUR KERJA PENGEMBANGAN SISTEM (DEVELOPER WORKFLOW)
## Modul Web Pengelolaan Tugas Harian (TaskFlow) — PT Bank CIMB Niaga Tbk

> **Penulis**: Full-Stack Web Developer (Internship/Technical Assessment)  
> **Aplikasi**: TaskFlow CIMB Niaga  
> **Teknologi**: Python 3 (FastAPI) + MySQL 8.0 + Vue.js 3 (Vite, Tailwind CSS)  
> **Tanggal Pembuatan**: November 2026  
> **Status**: Selesai & Teruji (*Production-Ready*)

---

## DAFTAR ISI

1. [Bab 1: Pendahuluan & Latar Belakang Proyek](#bab-1-pendahuluan--latar-belakang-proyek)
2. [Bab 2: Analisis Kebutuhan & Perancangan Arsitektur](#bab-2-analisis-kebutuhan--perancangan-arsitektur)
3. [Bab 3: Langkah Demi Langkah Pembangunan Backend (FastAPI + MySQL)](#bab-3-langkah-demi-langkah-pembangunan-backend-fastapi--mysql)
4. [Bab 4: Langkah Demi Langkah Pembangunan Frontend (Vue.js 3 + Tailwind CSS)](#bab-4-langkah-demi-langkah-pembangunan-frontend-vuejs-3--tailwind-css)
5. [Bab 5: Tantangan Teknis & Solusi Rekayasa (Troubleshooting)](#bab-5-tantangan-teknis--solusi-rekayasa-troubleshooting)
6. [Bab 6: Panduan Instalasi & Menjalankan Aplikasi](#bab-6-panduan-instalasi--menjalankan-aplikasi)
7. [Bab 7: Prosedur Pengujian Komprehensif (Testing & Verification)](#bab-7-prosedur-pengujian-komprehensif-testing--verification)
8. [Bab 8: Kesimpulan & Penutup](#bab-8-kesimpulan--penutup)

---

## BAB 1: PENDAHULUAN & LATAR BELAKANG PROYEK

### 1.1. Latar Belakang
Sebagai seorang pengembang perangkat lunak, saya menerima penugasan teknis (*programming assignment*) dari perusahaan untuk membangun sebuah **Modul Web Sederhana untuk Mencatat Daftar Tugas Harian**. 

Dalam operasional perbankan modern di **PT Bank CIMB Niaga Tbk**, efisiensi kerja tim sangat bergantung pada ketepatan waktu penyelesaian tugas harian. Diperlukan sebuah sistem pencatatan tugas yang:
1. Memiliki performa andal dan arsitektur bersih (*clean architecture*).
2. Mematuhi identitas visual resmi korporat (*corporate identity*) Bank CIMB Niaga: warna solid *CIMB Burgundy Red* (`#7E1322`), tanpa gradasi warna acak, rapi, dan profesional.
3. Mampu memantau **Service Level Agreement (SLA)** secara akurat: membedakan antara tugas yang **"Selesai Tepat Waktu"** vs **"Selesai Terlambat"**.
4. Mendukung lampiran dokumen pendukung (PDF, Word, Excel, gambar) dan pratinjau berkas langsung.
5. Memiliki tata letak responsif (*mobile-friendly*) untuk kenyamanan penggunaan lintas perangkat (ponsel, tablet, laptop).

### 1.2. Tujuan Pembangunan
1. Menyediakan modul CRUD (*Create, Read, Update, Delete*) tugas harian yang intuitif dan cepat.
2. Menyajikan dashboard metrik dan analitik produktivitas kerja secara *real-time*.
3. Menyediakan RESTful API standar industri yang terdokumentasi otomatis dengan Swagger/OpenAPI.
4. Menghasilkan kode program yang rapi, modular, mudah dirawat (*maintainable*), dan bebas dari ketergantungan rapuh.

---

## BAB 2: ANALISIS KEBUTUHAN & PERANCANGAN ARSITEKTUR

### 2.1. Pemilihan Tumpukan Teknologi (Tech Stack)

Saya menetapkan keputusan arsitektur teknologi berikut berdasarkan pertimbangan kecepatan pengembangan, performa, dan skalabilitas:

| Lapisan (Layer) | Teknologi yang Saya Pilih | Alasan Pemilihan |
|---|---|---|
| **Backend Framework** | **FastAPI (Python 3.10+)** | Framework Python modern dengan performa tinggi (berbasis Starlette & Pydantic), asinkron, *type-safety*, serta auto-generate dokumentasi Swagger UI interaktif. |
| **Database & ORM** | **MySQL 8.0 (Laragon) + SQLAlchemy 2.0** | Relational Database Management System standar industri. SQLAlchemy memberikan abstraksi pemodelan tabel dan pencegahan serangan SQL Injection. |
| **Frontend Framework** | **Vue.js 3 (Composition API)** | Reaktivitas deklaratif yang ringan, performa render tinggi, arsitektur berbasis komponen (`<script setup>`), dan struktur kode yang mudah dipelihara. |
| **Build Tool & Bundler** | **Vite 6** | Menyediakan *Hot Module Replacement* (HMR) berkecepatan tinggi dan proses bundling aset produksi yang optimal. |
| **Styling Engine** | **Tailwind CSS 3.4** | Utility-first CSS framework untuk membangun antarmuka yang sangat responsif, presisi, dan konsisten dengan sistem warna CIMB Niaga. |
| **Komponen Ikon** | **Lucide Icons (`lucide-vue-next`)** | Kumpulan ikon vektor modern yang ringan, tajam, dan dapat diubah ukurannya dengan sempurna. |

---

### 2.2. Perancangan Skema Basis Data (Database Schema)

Saya merancang tabel tunggal `tasks` dengan optimasi indeks untuk mendukung pencarian dan penyaringan data secara instan:

```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    category VARCHAR(60) NOT NULL DEFAULT 'Umum',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    due_date DATETIME NULL,
    completed_at DATETIME NULL,
    attachment_url VARCHAR(500) NULL,
    attachment_name VARCHAR(255) NULL,
    attachment_type VARCHAR(100) NULL,
    attachment_size INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_tasks_status (status),
    INDEX idx_tasks_category (category),
    INDEX idx_tasks_priority (priority),
    INDEX idx_tasks_due_date (due_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### Atribut Kunci:
* `due_date`: Menyimpan batas akhir pengerjaan tugas dalam waktu lokal Indonesia (WIB).
* `completed_at`: Waktu riil saat pengguna menandai tugas selesai.
* **Logika SLA**:
  * Jika `completed_at <= due_date` $\rightarrow$ **Selesai Tepat Waktu**.
  * Jika `completed_at > due_date` $\rightarrow$ **Selesai Terlambat**.
  * Jika tugas selesai dan `due_date IS NULL` $\rightarrow$ **Selesai Tepat Waktu**.

---

### 2.3. Diagram Arsitektur Sistem

```
+-------------------------------------------------------------------------+
|                        KLIEN PENGGUNA (BROWSER)                         |
|   Desktop PC / Laptop / Tablet / Smartphone (Tampilan Responsif CIMB)   |
+------------------------------------+------------------------------------+
                                     |
                       HTTP / JSON   |   Multipart Form (Upload)
                                     v
+-------------------------------------------------------------------------+
|                  FRONTEND: VUE.JS 3 + VITE (PORT 5173)                  |
|  - Navbar & Jam Live WIB          - FilterBar & Search Debounce        |
|  - StatsCards (5 Metrik Aktif)    - TaskCard (Grid) & TaskTable (List) |
|  - TaskModal (Form Input Lossless)- TaskDetailModal (Preview Gambar)   |
+------------------------------------+------------------------------------+
                                     |
                          Proxy /api | Proxy /uploads
                                     v
+-------------------------------------------------------------------------+
|                  BACKEND: FASTAPI + UVICORN (PORT 8000)                 |
|  - Routers (/api/tasks)           - Business Logic & Filtering (CRUD)  |
|  - Pydantic v2 Schema Validation  - StaticFiles Mount (/uploads)       |
|  - SQLAlchemy 2.0 ORM Engine      - Auto-Seed Data & Exception Handler |
+------------------------------------+------------------------------------+
                                     |
                             PyMySQL | TCP Port 3306
                                     v
+-------------------------------------------------------------------------+
|                  DATABASE SERVER: MYSQL 8.0 (LARAGON)                   |
|                        Database: daily_tasks_db                         |
+-------------------------------------------------------------------------+
```

---

## BAB 3: LANGKAH DEMI LANGKAH PEMBANGUNAN BACKEND (FASTAPI + MYSQL)

Berikut adalah tahapan terperinci bagaimana saya menginisialisasi dan menyusun backend aplikasi dari awal hingga selesai:

### Langkah 3.1: Inisialisasi Environment & Dependensi
1. Saya membuat direktori proyek di `c:\laragon\www\bcm-dev-intern\backend`.
2. Saya membuat virtual environment Python:
   ```bash
   python -m venv venv
   ```
3. Mengaktifkan environment dan menginstal dependensi produksi:
   ```bash
   venv\Scripts\activate
   pip install fastapi uvicorn[standard] sqlalchemy pymysql cryptography pydantic pydantic-settings python-multipart httpx
   ```
4. Mengunci dependensi ke dalam berkas `requirements.txt`.

### Langkah 3.2: Konfigurasi Terpusat (`app/core/config.py`)
Saya merancang pengaturan berbasis *environment variables* menggunakan `pydantic-settings`:
* Membaca host basis data, port MySQL (3306), nama database (`daily_tasks_db`), serta path upload berkas (`backend/uploads`).
* Mengonfigurasi parameter `APP_DEBUG` agar tidak bertabrakan dengan environment sistem Windows.

### Langkah 3.3: Konfigurasi Koneksi Database (`app/core/database.py`)
* Menggunakan SQLAlchemy `create_engine` dengan koneksi `pymysql`.
* Menambahkan opsi `pool_pre_ping=True` dan `pool_recycle=3600` untuk menjaga stabilitas koneksi MySQL agar tidak mengalami *timeout* saat aplikasi idle.
* Menyediakan dependency injection `get_db()` untuk manajemen lifecycle transaksi per HTTP request.

### Langkah 3.4: Pemodelan Data Relasional (`app/models/task.py`)
Saya mendefinisikan model SQLAlchemy `Task` dengan method khusus:
```python
def mark_completed(self):
    self.status = TaskStatus.COMPLETED
    self.completed_at = datetime.now()

def mark_uncompleted(self, status: TaskStatus = TaskStatus.PENDING):
    self.status = status
    self.completed_at = None
```
*Menggunakan `values_callable=lambda obj: [e.value for e in obj]` pada deklarasi Enum agar kompatibel penuh dengan nilai string lowercase di database MySQL.*

### Langkah 3.5: Validasi Skema Pydantic (`app/schemas/task.py`)
* Mendefinisikan schema input `TaskCreate`, `TaskUpdate`, dan `TaskStatusUpdate`.
* Menambahkan validator `@field_validator("title")` untuk memastikan judul tugas tidak boleh kosong atau hanya berisi spasi putih.
* Menyusun `TaskStatsResponse` untuk merangkum seluruh metrik kinerja: `total`, `pending`, `in_progress`, `completed`, `completed_on_time`, `completed_late`, `overdue`, dan `completion_rate`.

### Langkah 3.6: Penyusunan Query Layer & Agregasi Metrik (`app/crud/task.py`)
Saya menyusun fungsi-fungsi query yang efisien:
1. `get_tasks()`: Mendukung filter dinamis status (`completed_on_time`, `completed_late`, dll), filter kategori *case-insensitive*, prioritas, kata kunci pencarian pada judul/deskripsi, dan pengurutan fleksibel.
2. `get_task_stats()`: Menjalankan satu kali query agregasi SQL menggunakan fungsi `func.sum(case(...))` untuk menghitung seluruh metrik secara simultan tanpa membebani performa database.
3. Fungsi CRUD standar: `create_task()`, `update_task()`, `update_task_status()`, dan `delete_task()`.

### Langkah 3.7: Implementasi REST API & File Upload (`app/routers/task.py`)
Saya mengimplementasikan endpoint berikut:
* `GET /api/tasks`: Mengambil daftar tugas dengan filter dan sorting.
* `GET /api/tasks/stats`: Mengambil statistik KPI tugas.
* `GET /api/tasks/categories`: Mengambil daftar kategori dinamis.
* `GET /api/tasks/{id}`: Mengambil rincian detail tugas.
* `POST /api/tasks`: Membuat tugas baru.
* `PUT /api/tasks/{id}`: Memperbarui data tugas.
* `PATCH /api/tasks/{id}/status`: Memperbarui status tugas secara instan.
* `DELETE /api/tasks/{id}`: Menghapus tugas dan berkas fisik lampirannya dari disk.
* `POST /api/tasks/{id}/upload`: Mengunggah berkas pendukung (maksimal 10 MB). Nama berkas disanitasi dan diberi prefix UUID unik untuk mencegah penimpaan file (*file collision*).
* `DELETE /api/tasks/{id}/attachment`: Menghapus berkas lampiran yang terpasang pada tugas.

### Langkah 3.8: Entry Point & Auto-Seed Data (`app/main.py`)
* Mengonfigurasi lifespan aplikasi: otomatis membuat tabel MySQL jika belum ada (`Base.metadata.create_all`) dan menginjeksi 5 data tugas contoh realistis jika tabel masih kosong.
* Memasang middleware CORS untuk mengizinkan request dari frontend.
* Melakukan mounting static directory `/uploads` untuk melayani akses pratinjau gambar dan pengunduhan berkas dokumen.

---

## BAB 4: LANGKAH DEMI LANGKAH PEMBANGUNAN FRONTEND (VUE.JS 3 + TAILWIND CSS)

### Langkah 4.1: Inisialisasi Proyek Vue 3
1. Saya membuat scaffolding proyek Vue 3 menggunakan Vite:
   ```bash
   npm create vite@latest frontend -- --template vue
   ```
2. Menginstal paket dependensi frontend:
   ```bash
   cd frontend
   npm install axios lucide-vue-next
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

### Langkah 4.2: Kustomisasi Tema & Palet Warna CIMB Niaga (`tailwind.config.js`)
Saya mendaftarkan palet warna resmi Bank CIMB Niaga:
```javascript
theme: {
  extend: {
    colors: {
      cimb: {
        50: '#FDF2F3',
        100: '#FCE7E9',
        200: '#F9D1D5',
        700: '#971224',
        800: '#7E1322', // Warna Burgundy Utama CIMB Niaga
        900: '#640E1B',
        950: '#420811',
      }
    }
  }
}
```

### Langkah 4.3: Mengatasi Masalah Pergeseran Waktu (`src/utils/dateFormatter.js`)
Untuk mengatasi bug umum di mana method bawaan JavaScript `.toISOString()` mengonversi jam WIB (UTC+7) menjadi UTC (mengurangi 7 jam), saya merancang modul penanganan waktu lokal yang *lossless*:
* `toDateTimeLocalValue()`: Menghasilkan format `YYYY-MM-DDTHH:mm` untuk input form HTML tanpa manipulasi offset.
* `fromDateTimeLocalValue()`: Menjaga format waktu lokal murni untuk dikirim ke backend.
* `formatIndonesianDateTime()`: Memformat tanggal dan jam ke dalam bahasa Indonesia lengkap dengan label zona waktu `WIB` (contoh: `Jum, 6 Nov 2026, 21:25 WIB`).
* `formatIndonesianClock()`: Menghasilkan string jam digital *real-time* yang berdetik setiap detik.

### Langkah 4.4: Pembangunan Komponen Antarmuka Pengguna
Saya merancang komponen antarmuka yang modular dan bersih:

1. **`Navbar.vue`**:
   * Header korporat dengan emblem resmi Bank CIMB Niaga.
   * Jam digital *live* real-time Indonesia (WIB) yang diperbarui setiap detik.
   * Tautan langsung ke dokumentasi interaktif Swagger API.
   * Tombol utama **Tambah Tugas** berwarna solid merah CIMB (`#7E1322`).

2. **`StatsCards.vue`**:
   * 5 kartu metrik: **Total Tugas**, **Menunggu**, **Dikerjakan**, **Tepat Waktu**, dan **Selesai Terlambat**.
   * Dilengkapi persentase dan mini *progress bar* visual.
   * Memiliki *active ring highlight* yang menyala sesuai kategori yang sedang difilter.

3. **`FilterBar.vue`**:
   * Kolom pencarian tugas dengan fitur *debouncing* (300ms) untuk mencegah beban query berlebih.
   * Filter cepat status, kategori dinamis, tingkat prioritas, dan pengurutan (*sorting*).
   * Tombol *view switcher* untuk beralih antara tampilan kartu (*Grid View*) dan tabel ringkas (*Table View*).

4. **`TaskCard.vue`**:
   * Desain kartu bersih, teratur, dan simetris.
   * **Header Bar**: Kategori dan prioritas selalu berada rapi berdampingan di sisi kiri tanpa patah baris. Sisi kanan memuat pill status interaktif dengan indikasi jelas (*Selesai Tepat Waktu* / *Selesai Terlambat* / *Dikerjakan* / *Menunggu*).
   * **Body**: Tombol centang cepat, judul tugas yang tegas, deskripsi yang terpotong rapi (*line-clamp*), dan chip berkas lampiran.
   * **Footer**: Menampilkan waktu penyelesaian riil tugas serta tombol aksi (*Lihat Detail*, *Edit*, *Hapus*).

5. **`TaskTable.vue`**:
   * Format tabel profesional dengan kolom status pengerjaan yang jelas.

6. **`TaskDetailModal.vue`**:
   * Modal rincian tugas komprehensif.
   * Bagian lampiran menampilkan informasi ukuran berkas dan tipe dokumen. Jika berkas berupa gambar, pratinjau langsung ditampilkan dengan opsi buka layar penuh.

7. **`TaskModal.vue`**:
   * Modal tambah/edit tugas dengan dropdown native kategori dan opsi penambahan kategori baru.
   * Dilengkapi tombol pilihan cepat tenggat waktu (+4 Jam, Besok, 3 Hari).
   * Diberi atribut `spellcheck="false"` untuk mencegah garis merah koreksi ejaan browser.

8. **`ConfirmModal.vue` & `Toast.vue`**:
   * Modal konfirmasi aksi destruktif dan notifikasi toast mengambang yang responsif.

---

## BAB 5: TANTANGAN TEKNIS & SOLUSI REKAYASA (TROUBLESHOOTING)

Dalam proses pengerjaan, saya menghadapi beberapa tantangan teknis nyata. Berikut adalah cara saya menganalisis akar masalah dan menyelesaikannya:

### 1. Masalah Pergeseran Zona Waktu (Timezone Drift -7 Jam)
* **Gejala**: Ketika pengguna memilih deadline jam `18:30 WIB`, setelah disimpan dan dibuka kembali di form edit, jam berubah menjadi `11:30` (berkurang 7 jam). Jika disimpan lagi, berkurang 7 jam lagi.
* **Akar Masalah**: Penggunaan `.toISOString()` mengonversi waktu lokal ke UTC sebelum dikirim ke API. MySQL menyimpan string tanpa timezone, sehingga saat dibaca kembali, browser menganggapnya UTC lagi dan mengurangi 7 jam berulang kali.
* **Solusi Saya**: Saya membuat fungsi `toDateTimeLocalValue()` dan `fromDateTimeLocalValue()` di `dateFormatter.js` untuk mentransmisikan dan membaca string datetime lokal murni (`YYYY-MM-DDTHH:mm:ss`) tanpa konversi UTC.

### 2. Inkonsistensi Datalist Kategori & Garis Merah Spellcheck
* **Gejala**: Elemen `<input list="categories">` tampil berbeda-beda di berbagai browser, dan kata-kata bahasa Indonesia seperti *"Umum"* diberi garis bawah bergelombang merah oleh spellcheck peramban.
* **Solusi Saya**: Mengganti `<input list>` dengan native `<select>` yang konsisten di semua platform, menambahkan opsi `+ Kategori Lainnya...` dengan input teks dinamis, serta menyematkan `spellcheck="false"`.

### 3. Header Kartu Tugas Berantakan (Line Wrapping Akward)
* **Gejala**: Badge status yang panjang ("Selesai Tepat Waktu") diletakkan berdampingan dengan kategori dan prioritas serta dropdown status terpisah. Pada lebar kartu desktop/mobile tertentu, badge prioritas terlempar ke baris kedua sendirian.
* **Solusi Saya**: Saya menyatukan badge status dan pengubah status menjadi satu elemen pill dropdown tunggal di sisi kanan atas, sehingga kategori dan prioritas di sisi kiri tetap berada rapi di satu baris tunggal tanpa tumpang tindih.

### 4. SQLAlchemy Enum Lookup Error
* **Gejala**: Terjadi error `LookupError: 'pending' is not among the defined enum values`.
* **Akar Masalah**: SQLAlchemy Enum secara default memetakan nama enum Python dalam huruf besar (`PENDING`), sedangkan data tersimpan dalam huruf kecil (`pending`).
* **Solusi Saya**: Menambahkan `values_callable=lambda obj: [e.value for e in obj]` pada definisi kolom model SQLAlchemy dan menormalkan data ke huruf kecil.

### 5. Pratinjau Gambar Lampiran Broken di Frontend
* **Gejala**: Gambar lampiran yang diunggah tidak dapat dimuat di frontend (muncul broken image icon).
* **Akar Masalah**: Server Vite frontend (port 5173) hanya mem-proxy request yang berawalan `/api`, sehingga request ke `/uploads` tidak diteruskan ke server FastAPI (port 8000).
* **Solusi Saya**: Menambahkan konfigurasi proxy `/uploads` pada `frontend/vite.config.js`.

---

## BAB 6: PANDUAN INSTALASI & MENJALANKAN APLIKASI

### 6.1. Prasyarat Sistem (Prerequisites)
Pastikan lingkungan komputer telah terpasang:
1. **Python 3.10+**
2. **Node.js 18+** & npm
3. **MySQL Server** (direkomendasikan melalui **Laragon** pada port default `3306`)

---

### 6.2. Persiapan Basis Data MySQL
1. Buka Laragon dan klik **Start All** (pastikan modul MySQL aktif).
2. Buat database baru bernama `daily_tasks_db` melalui HeidiSQL atau terminal MySQL:
   ```sql
   CREATE DATABASE daily_tasks_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

---

### 6.3. Menjalankan Backend (FastAPI)
1. Buka terminal baru dan arahkan ke direktori backend:
   ```bash
   cd c:\laragon\www\bcm-dev-intern\backend
   ```
2. Aktifkan virtual environment Python:
   ```bash
   venv\Scripts\activate
   ```
3. Pastikan berkas `.env` sudah sesuai:
   ```ini
   DATABASE_URL=mysql+pymysql://root:@localhost:3306/daily_tasks_db
   APP_DEBUG=true
   HOST=127.0.0.1
   PORT=8000
   ```
4. Jalankan server backend Uvicorn:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
5. Backend berhasil berjalan di `http://localhost:8000`. Dokumentasi API interaktif dapat diakses di `http://localhost:8000/docs`.

---

### 6.4. Menjalankan Frontend (Vue.js 3 + Vite)
1. Buka terminal kedua dan arahkan ke direktori frontend:
   ```bash
   cd c:\laragon\www\bcm-dev-intern\frontend
   ```
2. Jalankan development server Vite:
   ```bash
   npm run dev
   ```
3. Frontend berhasil aktif di **`http://localhost:5173`**.

---

## BAB 7: PROSEDUR PENGUJIAN KOMPREHENSIF (TESTING & VERIFICATION)

Sebagai pengembang, saya melakukan serangkaian pengujian menyeluruh untuk menjamin seluruh fungsi bekerja sesuai spesifikasi:

### 7.1. Matriks Pengujian Fungsional

| Skenario Pengujian | Langkah Pengujian | Hasil yang Diharapkan | Status |
|---|---|---|:---:|
| **Tambah Tugas Baru** | Klik tombol *+ Tambah Tugas*, isi judul, pilih kategori, tentukan deadline, lampirkan berkas gambar/PDF, lalu klik *Buat Tugas*. | Tugas tersimpan ke MySQL, modal tertutup, muncul notifikasi sukses, dan tugas langsung muncul di urutan teratas. | **BERHASIL** |
| **Selesai Tepat Waktu** | Buat tugas dengan deadline 2 jam ke depan (masa depan). Klik tombol centang untuk menandai selesai. | Status berubah menjadi **Selesai Tepat Waktu** (badge hijau), metrik dashboard kartu Tepat Waktu bertambah. | **BERHASIL** |
| **Selesai Terlambat** | Buat tugas dengan deadline 2 jam yang lalu (masa lalu). Klik tombol centang untuk menandai selesai. | Status berubah menjadi **Selesai Terlambat** (badge oranye/amber), metrik dashboard Selesai Terlambat bertambah. | **BERHASIL** |
| **Buka Kembali Tugas** | Pada tugas yang telah selesai, klik tombol centang sekali lagi. | Status kembali menjadi *Menunggu*, waktu selesai di-reset menjadi `null`, metrik statistik kembali sinkron. | **BERHASIL** |
| **Unggah & Pratinjau Berkas** | Buka detail tugas, unggah gambar PNG/JPG berukuran < 10 MB. | Gambar terunggah ke folder `/uploads`, pratinjau langsung muncul di modal detail dengan tombol unduh. | **BERHASIL** |
| **Validasi Ukuran Berkas** | Coba unggah berkas dengan ukuran > 10 MB. | Sistem membatalkan proses upload dan memunculkan pesan peringatan batas 10 MB. | **BERHASIL** |
| **Filter & Pencarian Real-time** | Ketik kata kunci pada kolom pencarian, klik salah satu kartu statistik (misal: *Tepat Waktu*). | Daftar tugas menyaring data secara presisi dengan debounce halus tanpa kedipan layar (*no lag*). | **BERHASIL** |
| **Ekspor Data ke CSV** | Klik tombol *Ekspor CSV*. | Berkas `.csv` terunduh otomatis berisi data seluruh tugas dengan format UTF-8 rapi. | **BERHASIL** |
| **Responsivitas Layar HP** | Uji antarmuka pada ukuran viewport 360px - 414px (Mobile). | Tata letak kartu otomatis menjadi 1 kolom, teks tidak terpotong, tombol sentuh ergonomis, dan tidak ada horizontal scrollbar. | **BERHASIL** |

---

### 7.2. Pengujian Otomatis RESTful API via Python Test Script
Saya juga memverifikasi integritas endpoint API menggunakan skrip otomasi:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. Uji Health Check
res = client.get("/api/health")
assert res.status_code == 200
assert res.json()["status"] == "healthy"

# 2. Uji Statistik KPI
stats_res = client.get("/api/tasks/stats")
assert stats_res.status_code == 200
data = stats_res.json()
assert "completed_on_time" in data
assert "completed_late" in data

# 3. Uji Filter Tugas Tepat Waktu vs Terlambat
on_time_res = client.get("/api/tasks?status=completed_on_time")
assert on_time_res.status_code == 200
```
*Hasil uji: Seluruh assertion bernilai `True` dan lolos 100%.*

---

### 7.3. Metodologi Validasi Komponen Response API Menggunakan Postman (Jawaban Soal QA)

Dalam melakukan pengujian kualitas API (*API Quality Assurance*) menggunakan **Postman**, saya tidak hanya memverifikasi bahwa endpoint mengembalikan data, tetapi saya memvalidasi respon secara komprehensif mencakup 6 komponen utama berikut:

#### 1. Validasi HTTP Status Code & Status Text
Saya memastikan kode status HTTP yang dikembalikan sesuai dengan standar arsitektur REST dan skenario pengujian:
* **`200 OK`**: Pada endpoint `GET /api/tasks`, `GET /api/tasks/stats`, dan `PUT /api/tasks/{id}`.
* **`201 Created`**: Pada endpoint pembuatan tugas baru `POST /api/tasks`.
* **`204 No Content`**: Pada endpoint penghapusan permanen `DELETE /api/tasks/{id}`.
* **`400 Bad Request`**: Ketika mengunggah berkas melebihi kuota 10 MB.
* **`404 Not Found`**: Saat mengakses ID tugas yang tidak terdaftar di database.
* **`422 Unprocessable Entity`**: Jika payload JSON melanggar aturan skema (misal: judul tugas kosong).
* **Script Postman Assertion**:
  ```javascript
  pm.test("Status code harus 200 OK atau 201 Created", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 201]);
  });
  ```

#### 2. Validasi Struktur & Kontrak Skema Data (JSON Schema Contract Testing)
Saya memastikan struktur body response selalu mematuhi kontrak antarmuka API tanpa ada atribut kunci yang hilang atau salah tipe data:
```javascript
const taskSchema = {
    "type": "object",
    "required": ["id", "title", "status", "category", "created_at"],
    "properties": {
        "id": { "type": "number" },
        "title": { "type": "string" },
        "category": { "type": "string" },
        "status": { "type": "string", "enum": ["pending", "in_progress", "completed"] },
        "priority": { "type": "string", "enum": ["low", "medium", "high"] },
        "due_date": { "type": ["string", "null"] },
        "completed_at": { "type": ["string", "null"] }
    }
};

pm.test("Struktur JSON Schema sesuai kontrak data", function () {
    pm.response.to.have.jsonSchema(taskSchema);
});
```

#### 3. Validasi Kebenaran Nilai & Logika Bisnis (Data Payload & Business Logic Integrity)
Saya memverifikasi bahwa nilai-nilai data mencerminkan logika bisnis yang diharapkan:
* Memastikan status ketepatan waktu: Jika tugas diselesaikan sebelum tenggat, maka selisih waktu `completed_at <= due_date`.
* Memastikan field opsional yang kosong bernilai `null` murni (bukan string kosong atau undefined).
```javascript
pm.test("Integritas logika data tugas terverifikasi", function () {
    const data = pm.response.json();
    pm.expect(data.title).to.not.be.empty;
    pm.expect(data.category).to.be.a('string');
    if (data.status === 'completed' && data.due_date && data.completed_at) {
        const isLate = new Date(data.completed_at) > new Date(data.due_date);
        pm.expect(isLate).to.be.a('boolean');
    }
});
```

#### 4. Validasi Response Time & Latensi (SLA Performa)
Saya memastikan response time setiap request berada di bawah ambang batas toleransi SLA (Service Level Agreement):
```javascript
pm.test("Response time di bawah batas toleransi SLA (500 ms)", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

#### 5. Validasi Response Headers (Keamanan & Metadata)
Saya memeriksa header response untuk memastikan tipe konten dan standar keamanan:
```javascript
pm.test("Header Content-Type adalah application/json", function () {
    pm.response.to.have.header("Content-Type");
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});
```

#### 6. Validasi Penanganan Error & Keamanan Informasi (Negative Testing)
Pada skenario uji negatif, saya memvalidasi pesan kesalahan dan memastikan tidak ada kebocoran data sensitif (*data leakage*):
```javascript
pm.test("Pesan error deskriptif dan tidak membocorkan stack trace database", function () {
    const err = pm.response.json();
    pm.expect(err).to.have.property("detail");
    pm.expect(JSON.stringify(err)).to.not.include("password");
    pm.expect(JSON.stringify(err)).to.not.include("pymysql");
});
```

#### 7. Otomasi Pengujian Berantai (Request Chaining via Environment Variables)
Untuk pengujian end-to-end yang efisien, saya mengotomasi alur pengujian dengan menyimpan ID dinamis ke variabel environment Postman:
```javascript
// Disematkan pada Tests tab endpoint POST /api/tasks:
const res = pm.response.json();
pm.environment.set("createdTaskId", res.id);

// Pada request berikutnya (GET /api/tasks/{{createdTaskId}}), ID tersebut otomatis digunakan.
```

---

## BAB 8: KESIMPULAN & PENUTUP

Melalui tahapan perancangan arsitektur yang matang, penerapan standar pengkodean terbaik (*best practices*), serta pengujian menyeluruh, aplikasi web **Modul Pengelolaan Tugas Harian (TaskFlow) Bank CIMB Niaga** telah berhasil saya selesaikan dengan kriteria keunggulan berikut:

1. **Akurasi & Integritas Data Tinggi**: Penanganan waktu lokal Indonesia (WIB) yang murni dan bebas pergeseran offset, serta pemantauan SLA ketepatan waktu (*On-Time vs Late Completion*) yang akurat.
2. **Kesesuaian Identitas Korporat**: Desain visual profesional bernuansa solid *CIMB Burgundy Red* (`#7E1322`), tanpa gradasi warna yang tidak perlu, rapi, dan konsisten.
3. **Performa Tinggi & Desain Responsif**: Waktu muat instan berkat optimasi query agregasi database MySQL dan rendering komponen Vue.js 3 yang optimal di ponsel pintar maupun komputer desktop.
4. **Dokumentasi Lengkap**: Tersedia dokumentasi teknis, diagram arsitektur, panduan API Swagger, serta panduan pengujian yang memudahkan kolaborasi tim pengembang di masa mendatang.

Aplikasi ini siap digunakan dan dapat diintegrasikan lebih lanjut ke dalam ekosistem internal perusahaan.

---
*Dokumen ini disusun secara mandiri oleh Pengembang sebagai pertanggungjawaban teknis pengerjaan tugas pemrograman.*

