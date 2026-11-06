import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_developer_workflow_docx(output_path):
    doc = Document()
    
    # Configure 1 inch page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    CIMB_RED = RGBColor(126, 19, 34)      # #7E1322
    DARK_TEXT = RGBColor(30, 41, 59)      # #1E293B
    MUTED_TEXT = RGBColor(100, 116, 139)  # #64748B
    
    # Title / Cover Page
    p_pre = doc.add_paragraph()
    r_pre = p_pre.add_run("PT BANK CIMB NIAGA TBK — TECHNICAL ASSESSMENT REPORT")
    r_pre.font.size = Pt(10)
    r_pre.font.bold = True
    r_pre.font.color.rgb = CIMB_RED
    
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("DOKUMENTASI ALUR KERJA PENGEMBANGAN SISTEM (DEVELOPER WORKFLOW)")
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = CIMB_RED
    p_title.paragraph_format.space_after = Pt(4)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Modul Web Pengelolaan Tugas Harian (TaskFlow) Berbasis Python FastAPI, MySQL, dan Vue.js 3")
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = DARK_TEXT
    p_sub.paragraph_format.space_after = Pt(18)

    # Meta Table Box
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Penulis (Author)", "Full-Stack Web Developer (Technical Assessment / Internship Candidate)"),
        ("Tumpukan Teknologi", "Python 3.10 (FastAPI), MySQL 8.0 (Laragon), Vue.js 3, Tailwind CSS, Lucide"),
        ("Waktu Pelaksanaan", "November 2026"),
        ("Status Implementasi", "Selesai 100% — Siap Produksi (Production-Ready)"),
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 80, 80, 120, 120)
        set_cell_margins(c1, 80, 80, 120, 120)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = DARK_TEXT
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Helper for Section Heading
    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = CIMB_RED
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = DARK_TEXT
        return p

    def add_body(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.bold = True
            rb.font.size = Pt(10)
            rb.font.color.rgb = DARK_TEXT
        r = p.add_run(text)
        r.font.size = Pt(10)
        r.font.color.rgb = DARK_TEXT
        return p

    def add_code_block(code_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Inches(0.2)
        r = p.add_run(code_text)
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    # --- BAB 1 ---
    add_heading_1("BAB 1: PENDAHULUAN & LATAR BELAKANG PROYEK")
    add_body(
        "Sebagai pengembang perangkat lunak, saya menerima penugasan pemrograman untuk merancang dan membangun modul web pencatatan daftar tugas harian. Penugasan ini menuntut penguasaan tumpukan teknologi modern dengan rekomendasi backend Python web dan database relasional MySQL, dilengkapi frontend interaktif Vue.js.",
        bold_prefix="1.1. Latar Belakang Penugasan: "
    )
    add_body(
        "Dalam lingkungan korporat perbankan di PT Bank CIMB Niaga Tbk, pengelolaan tugas harian memerlukan standar disiplin dan ketepatan waktu (SLA) yang tinggi. Oleh karena itu, saya mengarahkan pengembangan modul ini agar tidak hanya berfungsi sebagai to-do list biasa, melainkan sebuah modul enterprise yang dapat memantau apakah tugas diselesaikan secara Tepat Waktu atau Terlambat, mendukung lampiran berkas dokumen/gambar, serta memiliki identitas visual resmi Bank CIMB Niaga (Solid Burgundy Red #7E1322, bersih, tanpa gradasi warna yang tidak konsisten)."
    )

    # --- BAB 2 ---
    add_heading_1("BAB 2: ANALISIS KEBUTUHAN & PERANCANGAN ARSITEKTUR")
    add_heading_2("2.1. Keputusan Pemilihan Tumpukan Teknologi (Tech Stack)")
    add_body("Saya menetapkan tumpukan teknologi berikut berdasarkan efisiensi dan performa tinggi:")
    
    # Tech Stack Table
    t_stack = doc.add_table(rows=5, cols=3)
    t_stack.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Lapisan (Layer)", "Teknologi", "Alasan & Pertimbangan Desain"]
    for i, h in enumerate(headers):
        cell = t_stack.rows[0].cells[i]
        set_cell_background(cell, "7E1322")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)
    
    rows_data = [
        ("Backend Framework", "Python FastAPI (3.10+)", "Asinkron, performa sekelas NodeJS/Go, type-safety Pydantic, dan auto-generate Swagger UI."),
        ("Basis Data & ORM", "MySQL 8.0 (Laragon) + SQLAlchemy 2.0", "RDBMS teruji di industri. SQLAlchemy mencegah SQL Injection dan mengelola koneksi aman."),
        ("Frontend Framework", "Vue.js 3 (Composition API)", "Reaktivitas deklaratif yang bersih via <script setup>, ringan, dan modular."),
        ("Styling & Icons", "Tailwind CSS 3.4 + Lucide Icons", "Utility-first CSS untuk responsivitas mobile dan konsistensi warna identitas CIMB Niaga.")
    ]
    for row_idx, rdata in enumerate(rows_data, start=1):
        for col_idx, text_val in enumerate(rdata):
            cell = t_stack.rows[row_idx].cells[col_idx]
            set_cell_background(cell, "FFFFFF" if row_idx % 2 == 1 else "F8FAFC")
            set_cell_margins(cell, 80, 80, 120, 120)
            p = cell.paragraphs[0]
            r = p.add_run(text_val)
            r.font.size = Pt(9)
            r.font.color.rgb = DARK_TEXT

    add_heading_2("2.2. Perancangan Skema Database (MySQL Schema)")
    add_body("Saya merancang tabel 'tasks' dengan struktur kolom yang mendukung pencatatan waktu lokal dan lampiran berkas:")
    add_code_block(
        "CREATE TABLE tasks (\n"
        "    id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    title VARCHAR(255) NOT NULL,\n"
        "    description TEXT NULL,\n"
        "    category VARCHAR(60) NOT NULL DEFAULT 'Umum',\n"
        "    priority VARCHAR(20) NOT NULL DEFAULT 'medium',\n"
        "    status VARCHAR(20) NOT NULL DEFAULT 'pending',\n"
        "    due_date DATETIME NULL,\n"
        "    completed_at DATETIME NULL,\n"
        "    attachment_url VARCHAR(500) NULL,\n"
        "    attachment_name VARCHAR(255) NULL,\n"
        "    attachment_type VARCHAR(100) NULL,\n"
        "    attachment_size INT NULL,\n"
        "    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\n"
        "    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n"
        "    INDEX idx_tasks_status (status),\n"
        "    INDEX idx_tasks_category (category),\n"
        "    INDEX idx_tasks_due_date (due_date)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    )

    # --- BAB 3 ---
    add_heading_1("BAB 3: LANGKAH DEMI LANGKAH PEMBANGUNAN BACKEND")
    add_body(
        "Berikut adalah langkah demi langkah teknis yang saya tempuh dalam merealisasikan backend aplikasi:",
        bold_prefix="Tahapan Implementasi Backend: "
    )
    add_body("1. Menginisialisasi virtual environment Python dan menginstal dependensi: fastapi, uvicorn, sqlalchemy, pymysql, cryptography, pydantic, pydantic-settings, python-multipart.")
    add_body("2. Mengonfigurasi koneksi MySQL dengan connection pool (pool_pre_ping=True, pool_recycle=3600) pada app/core/database.py.")
    add_body("3. Mengimplementasikan model SQLAlchemy Task (app/models/task.py) dengan method mark_completed() dan mark_uncompleted(). Saya menggunakan values_callable lambda untuk memastikan kompatibilitas nilai enum string.")
    add_body("4. Menyusun schema validasi Pydantic v2 (app/schemas/task.py) dengan validator khusus pada judul tugas agar tidak kosong dan perangkum metrik TaskStatsResponse.")
    add_body("5. Mengembangkan logika query dan agregasi (app/crud/task.py). Saya membuat fungsi get_task_stats() yang menghitung total, pending, in_progress, completed_on_time, dan completed_late dalam satu kali query SQL case.")
    add_body("6. Mengembangkan REST API router (app/routers/task.py) meliputi operasi CRUD lengkap, pengubahan status cepat (PATCH /status), serta upload berkas pendukung (POST /upload) dengan sanitasi nama berkas UUID dan limit 10 MB.")
    add_body("7. Mengonfigurasi lifespan aplikasi pada app/main.py: otomatis memeriksa dan membuat tabel MySQL serta menyuntikkan 5 data awal realistis (seed tasks) jika tabel masih kosong.")

    # --- BAB 4 ---
    add_heading_1("BAB 4: LANGKAH DEMI LANGKAH PEMBANGUNAN FRONTEND")
    add_body(
        "Pada sisi antarmuka, saya merancang aplikasi web modern berbasis Vue 3 dengan orientasi kenyamanan pengguna (UX) dan responsivitas penuh:",
        bold_prefix="Tahapan Implementasi Frontend: "
    )
    add_body("1. Inisialisasi proyek dengan Vite 6 dan konfigurasi Tailwind CSS 3.4. Saya mendaftarkan palet warna korporat solid CIMB Burgundy Red (#7E1322) pada tailwind.config.js.")
    add_body("2. Mengembangkan modul dateFormatter.js untuk memastikan waktu lokal Indonesia (WIB) tersimpan dan tertampil secara akurat tanpa pergeseran offset UTC.")
    add_body("3. Membangun komponen antarmuka terstruktur:")
    add_body("   - Navbar.vue: Header korporat dengan emblem Bank CIMB Niaga, jam digital live WIB (berdetik setiap detik), tautan Swagger API, dan tombol primer merah.")
    add_body("   - StatsCards.vue: 5 kartu metrik analitik (Total, Menunggu, Dikerjakan, Tepat Waktu, Selesai Terlambat) yang interaktif dan dapat diklik untuk memfilter tugas secara instan.")
    add_body("   - FilterBar.vue: Pencarian teks dengan debouncing 300ms, filter status, kategori, prioritas, sorting, dan toggle view (Grid / Table).")
    add_body("   - TaskCard.vue: Kartu tugas rapi dengan header sejajar (kategori + prioritas di kiri, selector status terpadu di kanan), checkbox selesai, judul, dan footer informatif.")
    add_body("   - TaskTable.vue: Tampilan tabel alternatif ala spreadsheet perbankan.")
    add_body("   - TaskModal.vue: Modal formulir dengan native select kategori, penambahan kategori baru, preset waktu cepat (+4 Jam, Besok, 3 Hari), dan spellcheck disabled.")
    add_body("   - TaskDetailModal.vue: Modal detail lengkap dengan pratinjau langsung berkas gambar (Image Preview) dan kartu berkas dokumen.")
    add_body("   - App.vue: Orkestrator state terpusat, penanganan notifikasi toast, dan fitur ekspor data ke format CSV/Excel.")

    # --- BAB 5 ---
    add_heading_1("BAB 5: TANTANGAN TEKNIS & SOLUSI REKAYASA (TROUBLESHOOTING)")
    add_body("Dalam proses pengerjaan, saya menemukan beberapa kendala teknis dan berhasil menyelesaikannya dengan tepat:")
    
    add_body("1. Masalah Timezone Drift (-7 Jam ke UTC):", bold_prefix="Tantangan 1: ")
    add_body("   Penyebab: JavaScript bawaan toISOString() mengonversi jam WIB (UTC+7) ke UTC saat disimpan. MySQL menyimpan naive timestamp, sehingga saat dimuat ulang jam berkurang 7 jam berulang kali.")
    add_body("   Solusi Saya: Membuat fungsi toDateTimeLocalValue() dan fromDateTimeLocalValue() yang membaca dan mengirim string waktu lokal murni (YYYY-MM-DDTHH:mm:ss) tanpa konversi timezone.")

    add_body("2. Header Kartu Tugas Berantakan (Line Wrapping):", bold_prefix="Tantangan 2: ")
    add_body("   Penyebab: Menampilkan badge panjang 'Selesai Tepat Waktu' bersamaan dengan kategori, prioritas, dan dropdown status dalam satu baris menyebabkan badge prioritas patah ke baris kedua.")
    add_body("   Solusi Saya: Menyatukan badge status dan dropdown pengubah status menjadi satu elemen pill dropdown tunggal di sisi kanan atas, sehingga kategori dan prioritas di sisi kiri tetap sejajar rapi di satu baris.")

    add_body("3. Inkonsistensi Kategori & Garis Merah Ejaan Browser:", bold_prefix="Tantangan 3: ")
    add_body("   Penyebab: Datalist HTML menghasilkan tampilan berbeda pada peramban tertentu dan kata bahasa Indonesia seperti 'Umum' digarisbawahi merah oleh spellcheck.")
    add_body("   Solusi Saya: Mengganti datalist dengan native <select> korporat ditambah opsi '+ Kategori Lainnya...' serta atribut spellcheck='false'.")

    add_body("4. Pratinjau Gambar Lampiran Broken:", bold_prefix="Tantangan 4: ")
    add_body("   Penyebab: Vite hanya mem-proxy rute /api ke port 8000, sehingga aset gambar di /uploads menghasilkan HTTP 404.")
    add_body("   Solusi Saya: Menambahkan rute proxy /uploads pada frontend/vite.config.js yang meneruskan request ke backend FastAPI.")

    # --- BAB 6 ---
    add_heading_1("BAB 6: PANDUAN MENJALANKAN APLIKASI (HOW TO RUN)")
    add_body("Untuk menjalankan seluruh modul aplikasi ini, ikuti langkah-langkah praktis berikut:")
    add_body("1. Pastikan server MySQL berjalan (melalui Laragon) dan database 'daily_tasks_db' telah dibuat.")
    add_body("2. Jalankan Backend FastAPI:")
    add_code_block(
        "cd c:\\laragon\\www\\bcm-dev-intern\\backend\n"
        "venv\\Scripts\\activate\n"
        "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
    )
    add_body("3. Jalankan Frontend Vue.js Vite pada jendela terminal terpisah:")
    add_code_block(
        "cd c:\\laragon\\www\\bcm-dev-intern\\frontend\n"
        "npm run dev"
    )
    add_body("4. Buka peramban (browser) pada URL: http://localhost:5173")
    add_body("5. Akses dokumentasi interaktif Swagger API pada URL: http://localhost:8000/docs")

    # --- BAB 7 ---
    add_heading_1("BAB 7: PROSEDUR PENGUJIAN KOMPREHENSIF (TESTING GUIDE)")
    add_body("Saya telah melakukan verifikasi kualitas perangkat lunak dengan skenario pengujian sebagai berikut:")
    
    t_test = doc.add_table(rows=6, cols=3)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Skenario Pengujian", "Langkah Uji & Parameter", "Hasil yang Terverifikasi"]
    for i, h in enumerate(test_headers):
        cell = t_test.rows[0].cells[i]
        set_cell_background(cell, "7E1322")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)
    
    test_rows = [
        ("CRUD Lengkap", "Membuat, mengedit judul/deskripsi, dan menghapus tugas dengan konfirmasi.", "Data tersimpan, terupdate, dan terhapus secara permanen di database MySQL."),
        ("Selesai Tepat Waktu", "Menandai selesai tugas yang deadline-nya masih di masa depan.", "Status menjadi 'Selesai (Tepat Waktu)' dengan badge hijau, metrik kartu Tepat Waktu bertambah."),
        ("Selesai Terlambat", "Menandai selesai tugas yang deadline-nya telah lewat di masa lalu.", "Status menjadi 'Selesai (Terlambat)' dengan badge oranye, metrik kartu Selesai Terlambat bertambah."),
        ("Upload Berkas Pendukung", "Mengunggah berkas gambar PNG/JPG dan dokumen PDF (maks 10 MB).", "Berkas tersimpan di folder uploads, pratinjau gambar tampil utuh, dokumen dapat diunduh."),
        ("Responsivitas Mobile", "Menguji antarmuka pada viewport smartphone (360px - 414px).", "Kartu otomatis 1 kolom, teks tidak terpotong, tombol sentuh ergonomis, zero horizontal scroll.")
    ]
    for row_idx, rdata in enumerate(test_rows, start=1):
        for col_idx, text_val in enumerate(rdata):
            cell = t_test.rows[row_idx].cells[col_idx]
            set_cell_background(cell, "FFFFFF" if row_idx % 2 == 1 else "F8FAFC")
            set_cell_margins(cell, 80, 80, 120, 120)
            p = cell.paragraphs[0]
            r = p.add_run(text_val)
            r.font.size = Pt(9)
            r.font.color.rgb = DARK_TEXT

    # --- BAB 7.3: QA Testing Methodology in Postman ---
    add_heading_2("7.3. Metodologi Validasi Komponen Response API Menggunakan Postman (Jawaban Soal QA)")
    add_body("Dalam melakukan pengujian kualitas API menggunakan Postman, saya memvalidasi respon secara komprehensif mencakup 6 komponen utama:")
    
    add_body("1. HTTP Status Code & Status Text:", bold_prefix="Komponen 1: ")
    add_body("   Memvalidasi status code 200 OK (GET/PUT), 201 Created (POST), 204 No Content (DELETE), 400 Bad Request (Limit 10MB), 404 Not Found, dan 422 Unprocessable Entity.")
    add_code_block("pm.test('Status code harus 200 OK atau 201 Created', function () {\n    pm.expect(pm.response.code).to.be.oneOf([200, 201]);\n});")

    add_body("2. Response Body Structure & JSON Schema Contract:", bold_prefix="Komponen 2: ")
    add_body("   Memvalidasi kontrak data JSON Schema, memastikan keberadaan atribut kunci (id, title, status, category, created_at) dan kesesuaian tipe data.")
    add_code_block("pm.test('Validasi Kontrak JSON Schema', function () {\n    pm.response.to.have.jsonSchema(taskSchema);\n});")

    add_body("3. Nilai Data & Logika Bisnis (Data Payload & Business Logic Integrity):", bold_prefix="Komponen 3: ")
    add_body("   Memverifikasi kebenaran kalkulasi data, seperti perhitungan SLA ketepatan waktu (completed_at <= due_date sebagai tepat waktu) dan format waktu lokal.")
    add_code_block("pm.test('Nilai data tugas harus sesuai', function () {\n    const data = pm.response.json();\n    pm.expect(data.title).to.not.be.empty;\n    pm.expect(data.status).to.be.oneOf(['pending', 'in_progress', 'completed']);\n});")

    add_body("4. Response Time & Latensi (SLA Performa):", bold_prefix="Komponen 4: ")
    add_body("   Menjamin latensi berada di bawah batas toleransi SLA (Service Level Agreement), misalnya di bawah 500 ms.")
    add_code_block("pm.test('Response time di bawah batas SLA 500 ms', function () {\n    pm.expect(pm.response.responseTime).to.be.below(500);\n});")

    add_body("5. Response Headers (Keamanan & Metadata):", bold_prefix="Komponen 5: ")
    add_body("   Memeriksa header Content-Type (application/json) serta header keamanan web.")
    add_code_block("pm.test('Header Content-Type harus application/json', function () {\n    pm.response.to.be.header('Content-Type', 'application/json');\n});")

    add_body("6. Penanganan Error & Keamanan Informasi (Negative Testing):", bold_prefix="Komponen 6: ")
    add_body("   Memastikan format error deskriptif dan ramah pengguna tanpa membocorkan kredensial atau stack trace database sensitif.")
    add_code_block("pm.test('Format error deskriptif & aman', function () {\n    const err = pm.response.json();\n    pm.expect(err).to.have.property('detail');\n    pm.expect(JSON.stringify(err)).to.not.include('password');\n});")

    add_body("7. Otomasi Pengujian Berantai (Request Chaining via Environment Variables):", bold_prefix="Nilai Tambahan: ")
    add_body("   Menggunakan pm.environment.set('createdTaskId', res.id) pada request POST agar otomatis digunakan pada request GET, PUT, dan DELETE berikutnya dalam Postman Collection Runner.")

    # --- BAB 8 ---
    add_heading_1("BAB 8: KESIMPULAN & PENUTUP")
    add_body(
        "Melalui penerapan arsitektur bersih, integrasi tumpukan teknologi modern FastAPI, MySQL, dan Vue.js 3, serta perhatian mendalam terhadap kebutuhan korporat Bank CIMB Niaga, modul TaskFlow ini telah selesai saya bangun dengan standar kualitas tinggi, reliabilitas data waktu lokal, dan siap untuk tahap implementasi produksi.",
        bold_prefix="Kesimpulan Akhir: "
    )

    try:
        doc.save(output_path)
        print(f"Success! Document generated at: {output_path}")
    except PermissionError:
        alt_path = output_path.replace(".docx", "_V2.docx")
        doc.save(alt_path)
        print(f"Warning: Primary file was locked by Word. Successfully saved to: {alt_path}")

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "DOKUMENTASI_ALUR_KERJA_DEVELOPER.docx")
    create_developer_workflow_docx(out_file)

