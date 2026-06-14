# JARVIS AI System Working Guide

JARVIS (Just A Rather Very Intelligent System) adalah AI asisten otonom, hyper-intelligent yang terintegrasi dengan sistem Lumina Overmind.

Gunakan panduan ini sebagai titik masuk utama saat mengimplementasikan perubahan pada JARVIS.

## Tech Stack Overview

### Core System (Best-in-Class)
- **Node.js 18+** - Runtime environment
- **Express.js** - Web framework
- **PM2** - Process management
- **Docker** - Containerization
- **WebSocket** - Real-time communication

### AI & Intelligence
- **Google Gemini 1.5 Pro** - Primary AI model
- **Ollama (Llama3)** - Fallback local LLM
- **ethers.js** - Web3 integration
- **Stripe API** - Payment processing
- **MQTT** - IoT communication

### Database & Storage
- **SQLite** - Local database
- **Vector Database** - Knowledge graph storage
- **JSON Files** - State persistence
- **File System** - Document storage

### Python Scripts
- **FastAPI** - Python API endpoints
- **Celery** - Background tasks
- **Redis** - Task queue
- **BeautifulSoup4** - Web scraping
- **Pandas** - Data analysis

## Apa Itu JARVIS

JARVIS adalah sistem AI otonom dengan kemampuan:
- **Creator Security Layer** - Keamanan tingkat tinggi dengan God Mode
- **Elite Modules** - Visual Architect, CFO Ledger
- **Fault Tolerance** - Isolasi proses dan toleransi kesalahan
- **Absolute Resilience** - Bunker Protocol, Generative UI, IoT Bridge
- **Decentralized Entity** - AI Corporation, Hydra Protocol, Legacy Protocol

## Struktur Saat Ini

### Core System
- `core/` - Entry point utama
- `channels/` - Komunikasi (WhatsApp, Telegram)
- `security/` - Layer keamanan
- `intelligence/` - Modul AI dan knowledge graph

### Business Modules
- `shadow_ceo/` - CEO modules (Business Radar, Fiscal Calendar)
- `economics/` - Economic analysis
- `finance/` - Financial ledger
- `revenue/` - Revenue generation
- `business/` - Business analysis
- `empire/` - Empire building
- `invisible/` - Invisible empire

### Advanced Protocols
- `corporation/` - AI Corporation (Bounty Manager)
- `hardware/` - IoT Bridge
- `hydra/` - Multi-cloud protocol
- `legacy/` - Dead Man's Switch

### Python Scripts
- `python/` - Script Python untuk automation
- `scheduler.py` - Job scheduling
- `observer_loop.py` - Weekly observer loop

### Documentation
- `docs/` - Dokumentasi lengkap
- `RULES.md` - Aturan pengembangan ketat

## Urutan Bacaan yang Disarankan

1. `README_WORKING_GUIDE.md` - **INI** - Panduan kerja utama
2. `docs/README.md` - Overview JARVIS
3. `docs/CREATOR_SECURITY.md` - Layer keamanan Creator
4. `docs/ELITE_MODULES.md` - Modul elite
5. `docs/FAULT_TOLERANCE.md` - Toleransi kesalahan
6. `docs/ABSOLUTE_RESILIENCE.md` - Resiliensi absolut
7. `docs/DECENTRALIZED_ENTITY.md` - Entitas terdesentralisasi
8. `docs/DIRECTIVE_LOCK.md` - Directive Lock (Mode Saklek)
9. `RULES.md` - Aturan pengembangan

## Aturan Kerja

- **WAJIB**: JARVIS harus 100% terisolasi dari lumina-overmind
- **WAJIB**: Gunakan environment variables untuk semua sensitive data
- **WAJIB**: Semua async functions harus try-catch
- **WAJIB**: Log semua critical operations
- **WAJIB**: Implement retry logic untuk network calls
- **WAJIB**: Test semua security layer secara terpisah
- **DILARANG**: Hardcode credentials
- **DILARANG**: Commit .env files
- **DILARANG**: Bypass security checks

## Aturan Update Dokumentasi

**KRITIS**: Setiap penambahan atau modifikasi pada analisis, checklist, framework, atau dokumentasi harus segera diupdate di folder "JARVIS SYSTEM/docs". Ini memastikan:
- Semua dokumentasi tetap tersinkronisasi
- Tim selalu merujuk ke single source of truth
- Tidak ada duplikasi atau informasi yang bertentangan
- Perubahan dilacak dan version-controlled

**Proses**:
1. Saat menambahkan analisis baru → Update file yang sesuai di "JARVIS SYSTEM/docs"
2. Saat memodifikasi analisis yang ada → Update file di "JARVIS SYSTEM/docs"
3. Saat membuat framework baru → Tambahkan ke "JARVIS SYSTEM/docs" dan update README_WORKING_GUIDE.md
4. Selalu merujuk ke "JARVIS SYSTEM/docs" sebagai sumber kebenaran utama

## Aturan Tracking Progress

**KRITIS**: Saat bekerja melalui checklist, roadmap, atau action items:
- Selalu tandai item yang selesai sebagai ✅ (completed)
- Jangan hapus item yang selesai - simpan untuk tracking history
- Tandai item yang belum selesai sebagai ⬜ (not started) atau ⏳ (in progress)
- Ini memastikan:
  - Visibilitas progress setiap saat
  - Tracking historis apa yang sudah dilakukan
  - Kemampuan untuk melanjutkan kerja dari mana berhenti
  - Audit trail dari task yang selesai

**Format**:
- ✅ Item selesai
- ⏳ Item sedang berjalan
- ⬜ Item belum dimulai
- ❌ Item diblokir/tidak bisa diselesaikan

## Blocker Saat Ini

- Tidak ada blocker utama
- Sistem berjalan dalam mode development
- Perlu testing untuk production deployment

## Status Kesehatan Sistem

### Core Dimensions 1-10

#### 1. Struktur Kode & Organisasi
- **Status**: ✅ BAIK - Folder sudah terorganisir dengan jelas
- **Current**: 20 folder utama dengan kategori yang jelas

#### 2. Kualitas Kode
- **Status**: ✅ BAIK - Code quality tinggi dengan error handling
- **Note**: Semua async functions memiliki try-catch

#### 3. Dokumentasi
- **Status**: ✅ SANGAT BAIK - Dokumentasi lengkap di docs/
- **Current**: 18 file dokumentasi dengan detail lengkap

#### 4. Testing
- **Status**: ⚠️ MINIMAL - Perlu ditambah
- **Action**: Tambah unit tests untuk critical functions

#### 5. Security
- **Status**: ✅ SANGAT BAIK - Creator Security Layer aktif
- **Note**: God Mode dan Terminate Protocol diimplementasikan

#### 6. Performance
- **Status**: ✅ BAIK - Optimized dengan caching dan connection pooling

#### 7. Scalability
- **Status**: ✅ BAIK - Hydra Protocol untuk multi-cloud

#### 8. Maintainability
- **Status**: ✅ SANGAT BAIK - Struktur folder mendukung maintainability

#### 9. User Experience
- **Status**: ✅ BAIK - UI modern dengan shadcn/ui

#### 10. Deployment & DevOps
- **Status**: ✅ BAIK - Docker dan PM2 sudah dikonfigurasi

### Advanced Dimensions 11-15

#### 11. Fault Tolerance
- **Status**: ✅ SANGAT BAIK - Isolasi proses lengkap
- **Note**: PM2 dual process management

#### 12. Absolute Resilience
- **Status**: ✅ SANGAT BAIK - Bunker Protocol aktif
- **Note**: Failover Gemini ke Ollama

#### 13. Generative UI
- **Status**: ✅ BAIK - Dynamic React component renderer
- **Note**: WebSocket UI push mechanism

#### 14. Physical Actuation
- **Status**: ✅ BAIK - IoT Bridge dengan MQTT
- **Note**: Physical Hard Reboot capability

#### 15. Autonomous Funding
- **Status**: ✅ BAIK - AI Corporation dengan Bounty Manager
- **Note**: Web3 dan Stripe integration

### Decentralized Dimensions 16-19

#### 16. Multi-Cloud Regeneration
- **Status**: ✅ BAIK - Hydra Protocol dengan Terraform
- **Note**: AWS Tokyo dan DigitalOcean SG

#### 17. Leader Election
- **Status**: ✅ BAIK - Gossip Protocol dengan heartbeat
- **Note**: Automatic DNS failover

#### 18. Dead Man's Switch
- **Status**: ✅ BAIK - Legacy Protocol aktif
- **Note**: 30-day threshold dengan emergency ping

#### 19. Autonomous Sustenance
- **Status**: ✅ BAIK - Legacy Will execution
- **Note**: Asset liquidation dan next-of-kin alert

## Integrasi dengan Roadmap

Framework 19-dimension global standard ini melengkapi roadmap pengembangan JARVIS:
- **19-Dimension Analysis**: Memberikan health check keseluruhan
- **Roadmap**: Memberikan action items spesifik dengan timeline
- **Pendekatan Kombinasi**: Gunakan roadmap untuk eksekusi, gunakan 19-dimension untuk periodic health checks

## Quick Start

### Development
```bash
cd "JARVIS SYSTEM/jarvis"
npm install
npm run dev
```

### Production
```bash
cd "JARVIS SYSTEM/jarvis"
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Monitoring
```bash
pm2 logs jarvis-app
pm2 monit
pm2 status
```

## Environment Variables

```bash
# Core
NODE_ENV=production
JARVIS_PORT=3001
LUMINA_API_URL=http://localhost:8000

# Security
ROOT_CREATOR_WA_NUMBER=your_wa_number
ROOT_CREATOR_TG_ID=your_tg_id
ROOT_CREATOR_VERIFICATION_TOKEN=your_token

# AI
GEMINI_API_KEY=your_gemini_key
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3

# Financial
JARVIS_WALLET_PRIVATE_KEY=your_wallet_key
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
STRIPE_SECRET_KEY=your_stripe_key

# IoT
MQTT_BROKER=mqtt://localhost:1883
MQTT_USERNAME=jarvis
MQTT_PASSWORD=secure_password

# Cloudflare
CLOUDFLARE_API_TOKEN=your_cloudflare_token
CLOUDFLARE_ZONE_ID=your_zone_id

# Legacy
NEXT_OF_KIN_EMAIL=next_of_kin@example.com
NEXT_OF_KIN_PHONE=+1234567890
NEXT_OF_KIN_ADDRESS=0x1234567890abcdef1234567890abcdef12345678
```

## Git Workflow

### Branch Naming
- `feature/feature-name` untuk new features
- `bugfix/bug-description` untuk bug fixes
- `hotfix/critical-fix` untuk urgent fixes
- `refactor/refactor-description` untuk refactoring

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

## Emergency Procedures

### Creator Emergency Access
1. Gunakan Creator credentials
2. Aktifkan God Mode dengan `/override`
3. Execute emergency command
4. Monitor system response

### System Failure
1. Check PM2 status
2. Check logs
3. Restart affected services
4. Verify health endpoints

### Security Breach
1. Activate Directive Lock
2. Isolate affected systems
3. Review audit logs
4. Rotate all credentials
5. Notify Creator

## Support

Untuk pertanyaan atau issues:
- Review documentation di docs/
- Check logs
- Contact Creator untuk critical issues
- Gunakan proper channels untuk non-critical issues

## Version History

- v6.0.0 - Decentralized Entity dengan Absolute Persistence
- v5.0.0 - Absolute Resilience (Bunker Protocol, Generative UI, IoT Bridge)
- v4.0.0 - Fault Tolerance dengan Process Isolation
- v3.0.0 - Elite Modules (Visual Architect, CFO Ledger)
- v2.0.0 - Creator Security Layer
- v1.0.0 - Initial JARVIS system

## License

JARVIS AI System - Proprietary
All rights reserved
