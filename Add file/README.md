# Add File - Arsip Dokumentasi

Folder ini berisi file dokumentasi yang diarsipkan dan diorganisir berdasarkan kategori.

## Struktur Folder

### **docs/**
Folder dokumentasi utama dengan subfolder yang dikategorikan:

#### **database/** (9 file)
Dokumentasi skema database, query, monitoring, dan keamanan
- Dokumentasi skema (caching_sha2_password.md)
- Operasi data (data-batch-inserts.md, data-n-plus-one.md, data-pagination.md, data-upsert.md)
- Monitoring (monitor-explain-analyze.md, monitor-pg-stat-statements.md, monitor-vacuum-analyze.md)
- Optimasi query (query-composite-indexes.md, query-covering-indexes.md, query-index-types.md, query-missing-indexes.md, query-partial-indexes.md)
- Keamanan (security-privileges.md, security-rls-basics.md, security-rls-performance.md)

#### **frontend/** (4 file)
Dokumentasi komponen frontend dan UI
- Grafik 3D (BezierMesh.md)
- Contoh React (bindExample.md, connectExample.md, createDerivedMaterial.md)

#### **guides/** (8 file)
Dokumentasi umum dan panduan
- Panduan kontribusi (CONTRIBUTING.md)
- Dokumentasi paket komersial (COMMERCIAL_PACKAGE_README.md)
- Masalah umum (Common-issues.md)
- File README (README-DEVSECOPS.md, README-es.md, README_FASE3_CLOSER.md)
- Kepatuhan legal (legal_compliance.md)
- Panduan pengembangan (fp.md, lang.md, prompt_instructions.md, quotes.md)

#### **integration/** (2 file)
Integrasi pihak ketiga
- Integrasi webhook (archidep_webhook_integration.md)
- Konfigurasi CDN (cdn.md)
- Streaming (streaming.md)

#### **migration/** (62 file)
File yang ditandai untuk migrasi tech stack
- Semua file dengan prefix [MIGRATION_NEEDED] (API, autentikasi, backend, database, frontend, integrasi, laporan)
- File referensi migrasi (FILES_TO_DELETE.txt, FILES_TO_KEEP_CRITICAL.txt)
- Dokumentasi aturan TypeScript/ESLint

#### **typescript/** (4 file)
Konfigurasi TypeScript dan ESLint
- Aturan TypeScript (ban-ts-comment.md, ban-tslint-comment.md, ban-types.md)
- Panduan aksesibilitas (click-events-have-key-events.md)

## Catatan Migrasi

File dengan prefix `[MIGRATION_NEEDED]` memerlukan pembaruan selama fase migrasi tech stack:
- Fase 1: Dependensi kritis (Minggu 1-2)
- Fase 2: Infrastruktur (Minggu 3-4)
- Fase 3: Upgrade framework (Minggu 5-8)
- Fase 4: Fitur lanjutan (Minggu 9-12)

Lihat `guide lengkap projek/` untuk rencana migrasi detail.
