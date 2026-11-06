# Dokumentasi RESTful API CIMB NIAGA TaskFlow

Dokumentasi ini menjelaskan spesifikasi lengkap endpoint API modul tugas harian korporat PT Bank CIMB Niaga Tbk, format request, response JSON, penanganan unggah berkas (*multipart/form-data*), kode status HTTP, dan contoh pemanggilan menggunakan cURL.

---

## 1. Informasi Umum

- **Base URL**: `http://localhost:8000/api`
- **Static Uploads URL**: `http://localhost:8000/uploads/{filename}`
- **Format Pertukaran Data**: `application/json` & `multipart/form-data`
- **Interactive OpenAPI (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative ReDoc UI**: `http://localhost:8000/redoc`

---

## 2. Ringkasan Endpoint

| Method | Endpoint | Deskripsi | Tipe Request | Kode Status Sukses |
|---|---|---|---|---|
| `GET` | `/api/tasks/stats` | Mengambil metrik statistik tugas (Total, Pending, Selesai, Overdue, %) | - | `200 OK` |
| `GET` | `/api/tasks/categories` | Mengambil daftar opsi kategori tugas | - | `200 OK` |
| `GET` | `/api/tasks` | Mengambil daftar tugas (mendukung filter, search, & sort) | Query params | `200 OK` |
| `GET` | `/api/tasks/{id}` | Mengambil rincian detail 1 tugas berdasarkan ID | Path param | `200 OK` |
| `POST` | `/api/tasks` | Membuat tugas harian baru | `application/json` | `201 Created` |
| `PUT` | `/api/tasks/{id}` | Memperbarui seluruh/sebagian data tugas | `application/json` | `200 OK` |
| `PATCH` | `/api/tasks/{id}/status` | Mengubah status tugas secara cepat | `application/json` | `200 OK` |
| `POST` | `/api/tasks/{id}/upload` | Mengunggah gambar atau dokumen pendukung (Maks 10 MB) | `multipart/form-data` | `200 OK` |
| `DELETE` | `/api/tasks/{id}/attachment` | Menghapus berkas lampiran yang terpasang pada tugas | - | `200 OK` |
| `DELETE` | `/api/tasks/{id}` | Menghapus tugas secara permanen | - | `204 No Content` |
| `GET` | `/api/health` | Health check koneksi sistem & database | - | `200 OK` |

---

## 3. Rincian Endpoint

### 3.1. Ringkasan Statistik Tugas
- **Endpoint**: `GET /api/tasks/stats`
- **Response**: `200 OK`
```json
{
  "total": 7,
  "pending": 0,
  "in_progress": 0,
  "completed": 7,
  "completed_on_time": 5,
  "completed_late": 2,
  "overdue": 0,
  "completion_rate": 100.0
}
```

---

### 3.2. Daftar Tugas (List with Filters, Search, & Sort)
- **Endpoint**: `GET /api/tasks`
- **Query Parameters**:
  - `status` *(string, opsional)*: `'pending'`, `'in_progress'`, `'completed'`, `'completed_on_time'`, `'completed_late'`
  - `priority` *(string, opsional)*: `'low'`, `'medium'`, `'high'`
  - `category` *(string, opsional)*: Nama kategori (contoh: `Pekerjaan`)
  - `search` *(string, opsional)*: Kata kunci pada judul, catatan, atau kategori
  - `is_overdue` *(boolean, opsional)*: `true` untuk memfilter tugas yang belum selesai dan telah melewati batas deadline
  - `sort_by` *(string, default: `created_at`)*: `created_at`, `due_date`, `priority`, `title`, `status`
  - `order` *(string, default: `desc`)*: `asc` atau `desc`
  - `skip` *(integer, default: 0)*: Offset data pagination
  - `limit` *(integer, default: 200)*: Limit data per query

- **Response**: `200 OK`
```json
[
  {
    "id": 1,
    "title": "Review Pull Request Modul Absensi Pegawai",
    "description": "Melakukan code review dan testing fungsional...",
    "category": "Pekerjaan",
    "priority": "high",
    "status": "in_progress",
    "due_date": "2026-11-06T18:30:00",
    "completed_at": null,
    "attachment_url": "/uploads/a1b2c3d4e5_laporan.pdf",
    "attachment_name": "laporan.pdf",
    "attachment_type": "application/pdf",
    "attachment_size": 1048576,
    "created_at": "2026-11-06T17:36:30",
    "updated_at": "2026-11-06T17:36:30"
  }
]
```

---

### 3.3. Detail Tugas
- **Endpoint**: `GET /api/tasks/{id}`
- **Response**: `200 OK` (Mengembalikan objek tugas tunggal seperti di atas) atau `404 Not Found`.

---

### 3.4. Tambah Tugas Baru
- **Endpoint**: `POST /api/tasks`
- **Request Body**:
```json
{
  "title": "Audit Internal Keamanan Sistem Pembayaran",
  "description": "Review log transaksi dan pastikan enkripsi SSL/TLS memenuhi standar kepatuhan PCI-DSS.",
  "category": "Pekerjaan",
  "priority": "high",
  "status": "pending",
  "due_date": "2026-11-08T15:00:00"
}
```
- **Response**: `201 Created`

---

### 3.5. Unggah Gambar / Dokumen Pendukung (Upload Attachment)
- **Endpoint**: `POST /api/tasks/{id}/upload`
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `file`: Berkas biner (Gambar: JPG, PNG, WEBP, GIF; Dokumen: PDF, DOCX, XLSX, PPTX, TXT; Maks 10 MB).
- **Logika Sistem**:
  - Memverifikasi ukuran berkas.
  - Menghapus berkas lama jika sebelumnya sudah ada lampiran pada tugas ini (*clean disk storage*).
  - Menyimpan berkas dengan nama unik terenkripsi untuk mencegah tabrakan nama (*file collisions*).
  - Mengupdate atribut `attachment_url`, `attachment_name`, `attachment_type`, dan `attachment_size`.
- **Response**: `200 OK` (Objek tugas yang telah diperbarui dengan data lampiran).

---

### 3.6. Hapus Lampiran Tugas
- **Endpoint**: `DELETE /api/tasks/{id}/attachment`
- **Logika**:
  - Menghapus berkas fisik dari server disk.
  - Mereset kolom lampiran di database menjadi `NULL`.
- **Response**: `200 OK`.

---

### 3.7. Perbarui Tugas
- **Endpoint**: `PUT /api/tasks/{id}`
- **Request Body**: JSON fields yang ingin diperbarui.
- **Response**: `200 OK`.

---

### 3.8. Ubah Status Tugas Cepat
- **Endpoint**: `PATCH /api/tasks/{id}/status`
- **Request Body**: `{"status": "completed"}`
- **Response**: `200 OK` (Timestamp `completed_at` otomatis terisi).

---

### 3.9. Hapus Tugas
- **Endpoint**: `DELETE /api/tasks/{id}`
- **Logika**: Menghapus data tugas dari database sekaligus menghapus file lampiran jika ada.
- **Response**: `204 No Content`.

---

## 4. Contoh Pemanggilan dengan cURL

```bash
# 1. Mengambil seluruh tugas
curl -X GET "http://localhost:8000/api/tasks"

# 2. Mengambil detail tugas ID #1
curl -X GET "http://localhost:8000/api/tasks/1"

# 3. Membuat tugas baru
curl -X POST "http://localhost:8000/api/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Penyusunan Rencana Kerja Sprint 12", "category": "Proyek", "priority": "high"}'

# 4. Mengunggah berkas gambar/dokumen pendukung ke tugas ID #1
curl -X POST "http://localhost:8000/api/tasks/1/upload" \
     -F "file=@/path/to/dokumen_pendukung.pdf"

# 5. Mengunduh / melihat berkas lampiran statis
curl -O "http://localhost:8000/uploads/contoh_file.pdf"

# 6. Menghapus lampiran berkas tugas ID #1
curl -X DELETE "http://localhost:8000/api/tasks/1/attachment"

# 7. Menyelesaikan tugas
curl -X PATCH "http://localhost:8000/api/tasks/1/status" \
     -H "Content-Type: application/json" \
     -d '{"status": "completed"}'

# 8. Menghapus tugas
curl -X DELETE "http://localhost:8000/api/tasks/1"
```
