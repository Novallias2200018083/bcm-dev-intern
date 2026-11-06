-- ==============================================================
-- DATABASE SCHEMA: DAILY TASKS MANAGEMENT SYSTEM (TaskFlow)
-- Database Engine: MySQL 8.0+
-- Charset: utf8mb4 / utf8mb4_unicode_ci
-- ==============================================================

CREATE DATABASE IF NOT EXISTS `daily_tasks_db`
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE `daily_tasks_db`;

-- Table structure for table `tasks`
DROP TABLE IF EXISTS `tasks`;

CREATE TABLE `tasks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL COMMENT 'Judul tugas harian',
  `description` TEXT DEFAULT NULL COMMENT 'Detail deskripsi dan instruksi tugas',
  `category` VARCHAR(60) NOT NULL DEFAULT 'Umum' COMMENT 'Kategori tugas (e.g. Pekerjaan, Rapat, Proyek, Pribadi)',
  `priority` ENUM('low', 'medium', 'high') NOT NULL DEFAULT 'medium' COMMENT 'Tingkat prioritas tugas',
  `status` ENUM('pending', 'in_progress', 'completed') NOT NULL DEFAULT 'pending' COMMENT 'Status pengerjaan tugas',
  `due_date` DATETIME DEFAULT NULL COMMENT 'Tenggat waktu penyelesaian (deadline)',
  `completed_at` DATETIME DEFAULT NULL COMMENT 'Waktu tugas diselesaikan',
  `attachment_url` VARCHAR(500) DEFAULT NULL COMMENT 'URL / Path file dokumen atau gambar pendukung',
  `attachment_name` VARCHAR(255) DEFAULT NULL COMMENT 'Nama asli file lampiran',
  `attachment_type` VARCHAR(100) DEFAULT NULL COMMENT 'MIME type file lampiran',
  `attachment_size` INT DEFAULT NULL COMMENT 'Ukuran file lampiran dalam bytes',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu pembuatan data',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Waktu pembaruan data terakhir',
  PRIMARY KEY (`id`),
  INDEX `ix_tasks_status` (`status`),
  INDEX `ix_tasks_priority` (`priority`),
  INDEX `ix_tasks_category` (`category`),
  INDEX `ix_tasks_due_date` (`due_date`),
  INDEX `ix_tasks_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample initial data
INSERT INTO `tasks` (`title`, `description`, `category`, `priority`, `status`, `due_date`, `completed_at`) VALUES
('Review Pull Request Modul Absensi Pegawai', 'Melakukan code review dan testing fungsional untuk branch feature/attendance-v2 di repository Git.', 'Pekerjaan', 'high', 'in_progress', DATE_ADD(NOW(), INTERVAL 4 HOUR), NULL),
('Daily Standup Meeting Tim Engineering', 'Koordinasi sprint harian, laporan blocker, dan update progress pekerjaan harian melalui Google Meet.', 'Rapat', 'high', 'completed', DATE_SUB(NOW(), INTERVAL 2 HOUR), DATE_SUB(NOW(), INTERVAL 1 HOUR)),
('Menyusun Dokumentasi Teknis API & ERD', 'Lengkapi dokumen Swagger, panduan instalasi, dan diagram alur modul daftar tugas harian.', 'Pekerjaan', 'medium', 'pending', DATE_ADD(NOW(), INTERVAL 1 DAY), NULL),
('Optimasi Query Database MySQL Task', 'Membuat index komposit untuk filter status, prioritas, dan kategori agar load query tetap responsif.', 'Proyek', 'medium', 'pending', DATE_ADD(NOW(), INTERVAL 2 DAY), NULL),
('Update Sistem Operasi & Backup Database', 'Jadwal pemeliharaan server mingguan dan backup snapshot berkala pada database staging.', 'Pribadi', 'low', 'completed', DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_SUB(NOW(), INTERVAL 6 HOUR));

