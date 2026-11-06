# Diagram Alur Sistem (Flowcharts) - CIMB NIAGA TaskFlow

Dokumen ini memuat diagram alur (*flowcharts*) yang mendokumentasikan interaksi pengguna, alur navigasi detail tugas, siklus hidup dokumen/gambar pendukung, dan alur permintaan API pada modul tugas harian **PT Bank CIMB Niaga Tbk**.

---

## 1. Alur Interaksi Pengguna (User Journey Flowchart)

```mermaid
flowchart TD
    Start([Pengguna Membuka Web CIMB Niaga TaskFlow]) --> LoadData[Aplikasi Memuat Data Tugas & Statistik via API]
    LoadData --> DisplayDashboard[Tampilkan Dashboard: Metrik KPI, Filter Bar, dan Daftar Tugas]

    DisplayDashboard --> UserAction{Pilih Aksi Pengguna}

    UserAction -->|Lihat Rincian Tugas| OpenDetail[Klik Kartu / Judul / Ikon 'Lihat Detail']
    OpenDetail --> ViewDetailModal[Buka Modal Detail Tugas: Info Lengkap, Deadline, Preview Berkas]
    ViewDetailModal --> DetailAction{Aksi pada Modal Detail}
    DetailAction -->|Unggah Dokumen / Gambar| SelectFile[Pilih Berkas Lampiran Maks 10 MB]
    SelectFile --> UploadApi[POST /api/tasks/:id/upload]
    UploadApi --> RefreshDetail[Perbarui Preview Gambar/Dokumen & Tampilkan Toast]
    DetailAction -->|Hapus Lampiran| DeleteAttachApi[DELETE /api/tasks/:id/attachment]
    DeleteAttachApi --> RefreshDetail
    DetailAction -->|Toggle Selesai| ToggleDetailStatus[Update Status Cepat]
    ToggleDetailStatus --> RefreshDetail
    DetailAction -->|Tutup| DisplayDashboard

    UserAction -->|Tambah Tugas Baru| OpenCreateModal[Klik Tombol Merah '+ Tambah Tugas']
    OpenCreateModal --> InputForm[Isi Form: Judul, Kategori, Prioritas, Deadline, Dokumen/Gambar]
    InputForm --> SubmitCreate{Validasi Input}
    SubmitCreate -->|Valid| ApiPost[POST /api/tasks + Upload Berkas]
    SubmitCreate -->|Tidak Valid| ShowError[Tampilkan Pesan Error Validasi Form]
    ShowError --> InputForm
    ApiPost --> ToastSuccess1[Tampilkan Notifikasi Sukses]
    ToastSuccess1 --> LoadData

    UserAction -->|Filter / Cari| FilterTask[Input Keyword / Pilih Status / Kategori / Prioritas]
    FilterTask --> UpdateList[Update Daftar Tugas secara Real-time]
    UpdateList --> DisplayDashboard

    UserAction -->|Toggle Tampilan| SwitchView[Pilih Mode: Grid Kartu atau Mode Tabel]
    SwitchView --> DisplayDashboard

    UserAction -->|Hapus Tugas| OpenDeleteModal[Klik Ikon Sampah]
    OpenDeleteModal --> ConfirmDelete{Konfirmasi Hapus?}
    ConfirmDelete -->|Ya| ApiDelete[DELETE /api/tasks/:id]
    ConfirmDelete -->|Batal| DisplayDashboard
    ApiDelete --> ToastSuccess2[Tampilkan Notifikasi Tugas Berhasil Dihapus]
    ToastSuccess2 --> LoadData

    UserAction -->|Ekspor Data| ExportCSV[Klik Tombol 'Ekspor CSV']
    ExportCSV --> DownloadFile[Unduh File daftar_tugas_cimb_niaga.csv]
    DownloadFile --> DisplayDashboard
```

---

## 2. Alur Pengelolaan Berkas Lampiran (Attachment Flowchart)

```mermaid
flowchart TD
    UserSelectFile[Pengguna Memilih Berkas: Gambar PNG/JPG atau Dokumen PDF/Doc/Excel] --> CheckSize{Ukuran <= 10 MB?}
    CheckSize -->|Tidak| RejectFile[Tolak Berkas & Tampilkan Pesan Error: Maksimal 10 MB]
    CheckSize -->|Ya| CheckType{Validasi Ekstensi/MIME}
    
    CheckType -->|Valid| UploadServer[Kirim multipart/form-data ke Server]
    UploadServer --> ServerCheckOld{Ada Berkas Lama?}
    ServerCheckOld -->|Ada| UnlinkOld[Hapus Berkas Lama dari Direktori /uploads]
    ServerCheckOld -->|Tidak| GenName[Generate Nama Unik: UUID + Sanitized Filename]
    UnlinkOld --> GenName

    GenName --> SaveDisk[Simpan Berkas Fisik ke backend/uploads/]
    SaveDisk --> UpdateDB[Update tasks: attachment_url, attachment_name, attachment_type, attachment_size]
    UpdateDB --> Return200[Kembalikan Task Object 200 OK]
    
    Return200 --> ClientDetect{Deteksi Tipe Lampiran}
    ClientDetect -->|Gambar| RenderImage[Tampilkan Preview Gambar & Tombol 'Lihat Penuh']
    ClientDetect -->|Dokumen| RenderDocCard[Tampilkan Kartu Berkas, Ukuran, & Tombol Unduh]
```

---

## 3. Alur Siklus Hidup Tugas (Task State Transition)

```mermaid
stateDiagram-v2
    [*] --> Menunggu : Dibuat (Status: pending)
    
    Menunggu --> Dikerjakan : Mulai Pengerjaan (Status: in_progress)
    Menunggu --> Selesai : Langsung Diselesaikan (Status: completed)
    
    Dikerjakan --> Selesai : Tugas Selesai (Status: completed)
    Dikerjakan --> Menunggu : Ditunda (Status: pending)
    
    Selesai --> Menunggu : Dibuka Kembali (Status: pending)
    Selesai --> Dikerjakan : Dikerjakan Ulang (Status: in_progress)

    Menunggu --> [*] : Dihapus
    Dikerjakan --> [*] : Dihapus
    Selesai --> [*] : Dihapus
```

---

## 4. Alur Permintaan HTTP & Penanganan Backend

```mermaid
flowchart TD
    ClientReq[HTTP Request dari Frontend Vue.js] --> CheckCORS{Header CORS Terverifikasi?}
    CheckCORS -->|Tidak| BlockCORS[403 Forbidden]
    CheckCORS -->|Ya| RouteMatch{Cek Endpoint}

    RouteMatch -->|/uploads/*| StaticServer[StaticFiles Handler: Serve File Gambar/Dokumen]
    RouteMatch -->|/api/tasks/*| APIHandler[FastAPI Router]

    APIHandler --> ValidatePydantic{Validasi Schema & File}
    ValidatePydantic -->|Gagal| Err422[422 Unprocessable Entity / 400 Bad Request]
    ValidatePydantic -->|Sukses| ExecCRUD[Eksekusi Query Database via PyMySQL]
    
    ExecCRUD --> DBResult{Hasil Query}
    DBResult -->|Not Found| Err404[404 Not Found]
    DBResult -->|Sukses| SendJSON[Return JSON Data 200 / 201 / 204]
```
