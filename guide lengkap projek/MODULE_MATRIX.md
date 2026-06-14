# Module Matrix

This matrix classifies each major surface for planning and implementation.

## Tech Stack Status Overview

### Frontend Stack
- **Next.js 14** → Target: Upgrade to 15 with Turbopack
- **shadcn/ui + Radix UI** → Best-in-class, keep
- **TailwindCSS 3.3.0** → Target: Upgrade to 4
- **Zustand** → Good, keep or migrate to Jotai
- **TanStack Table** → Upgrade to v8
- **Recharts** → Upgrade to latest or switch to Visx
- **Framer Motion + GSAP** → Best-in-class, keep
- **Three.js + R3F** → Best-in-class, keep

### Backend Stack
- **FastAPI** → Best-in-class, keep
- **Prisma 7.8.0** → Upgrade to latest
- **PostgreSQL (Supabase)** → Best-in-class, keep
- **Celery + Redis** → Good, consider BullMQ
- **JWT + Passlib** → Consider Supabase Auth

### Critical Gaps (To Add) - FINAL RECOMMENDATION
- ✅ **react-hook-form + Zod** → Form management
- ✅ **@tanstack/react-query** → Data fetching
- ✅ **dinero.js** → Financial precision
- ✅ **exceljs** → Excel export
- ✅ **react-leaflet** → GIS/Mapping
- ✅ **Playwright** → E2E testing
- ✅ **next-seo + sitemap** → SEO optimization
- ✅ **PostHog** → Analytics
- ✅ **Casbin** → Authorization
- ✅ **slowapi** → Rate limiting

### New Critical Features (To Add - Phase 0) - ✅ COMPLETED
- ✅ **Archidep M2M Webhook Integration** → Transfer file siteplan otomatis (HIGH priority untuk proyek properti)
- ⏭️ **DevSecOps & Code Quality Setup** → ESLint, Prettier, TypeScript, pre-commit hooks (HIGH priority untuk production) - SKIPPED due to TypeScript strict mode issues
- ✅ **PostgreSQL Optimization Patterns** → Full-text search, JSONB indexing, batch INSERT (MEDIUM priority untuk performance)

### Upgrades (Performance) - ✅ SEBAGIAN COMPLETED
- ✅ **Next.js 14 → 15** → Turbopack
- ⏭️ **TailwindCSS 3 → 4** → Performance (SKIPPED - belum stabil)
- ✅ **TanStack Table v8** → Latest version
- ✅ **Jest → Vitest** → Faster testing
- ⏭️ **pnpm** → Package manager (SKIPPED - migrasi kompleks)

### New Infrastructure - ✅ SEBAGIAN COMPLETED
- ⏭️ **Turborepo** → Monorepo management (SKIPPED - git submodule issues)
- ✅ **GitHub Actions** → CI/CD
- ✅ **commitlint** → Commit standards

## Frontend Modules

| Module | Status | Notes |
|---|---|---|
| `login` | complete enough | Canonical visual style and auth flow anchor |
| `dashboard` | in progress | Core shell exists, needs backend stability and page consistency |
| `geo-intel` | partial | Map/geo visual exists, needs filter/drill-down/export logic |
| `inbox` | partial | Draft/review flow exists, needs queue, assignment, history, templates |
| `growth` | partial | Metrics and charts exist, needs attribution, pacing, A/B and history |
| `projects` | partial | Directory exists, needs detail lifecycle and data binding |
| `settings` | partial | Config surface exists, needs versioning, rollback, role gates |
| `jarvis` | partial | Control panel exists, needs stable command mapping and history |
| `workflows` | partial | Flow editor exists, needs validation, versioning, test-run, rollback |
| `partner` | partial | Directory and calculator exist, needs lifecycle and payout ledger |
| `governance` | partial | Logs and KPI surface exist, needs audit engine and policy views |
| `dashboard/assets` | partial | Entry hub exists, needs library, tagging, queue, approval state |
| `creative` | partial | Asset tabs exist, needs create/revise/publish/versioning |
| `landing` | partial | Public submit exists, needs preview, attribution, handoff flow |
| `ads-approval` | partial | Approval workflow exists, needs revisions and launch tracking |
| `orchestrator` | partial | React Flow builder exists, needs runtime lifecycle and debug trace |
| `leads/[id]` | unknown | Detail route should be audited against backend data contract |
| `projects/[id]` | unknown | Detail route should be audited against backend data contract |
| `settings/classified-vault` | partial | CRUD and secret management surface exists |
| `dashboard/assets/siteplan-dropzone` | partial | Upload flow exists, needs queue, status, and asset linkage |

## Backend Modules

| Module | Status | Notes |
|---|---|---|
| `api/main.py` | in progress | Main app entry, router composition, route toggles |
| `api/endpoints/leads.py` | blocked | Build/runtime issue traces to missing SQLite table state |
| `api/endpoints/projects.py` | partial | Used by several dashboard screens |
| `api/endpoints/jarvis.py` | partial | Tied to conversational AI and control surface |
| `api/endpoints/workflows.py` | partial | Needed by workflow builder and orchestration |
| `api/endpoints/visual.py` / `visual_mirage.py` / `vr.py` | partial | Visual/asset pipeline dependencies |
| `api/endpoints/config_vault.py` | partial | Secret and config management |
| `api/endpoints/webhooks.py` and webhook variants | partial | Integration edge and automation hooks |

## Shared Systems

| Module | Status | Notes |
|---|---|---|
| `core_modules/vault_manager.py` | partial | Central API key retrieval and cache |
| `core_modules/model_fallback.py` | partial | Multi-provider model fallback registry |
| `api/utils/conversational_ai.py` | blocked | Previously had syntax/compatibility issues |
| `dashboard/components/Sidebar.tsx` | complete enough | Navigation shell, still tied to menu state |
| `dashboard/components/TopHeader.tsx` | complete enough | Search/project switcher/notifications shell |

## Scripts Folder (20+ scripts - IMPLEMENTED)

| Module | Status | Notes |
|---|---|---|
| `run_closer_agent.py` | ✅ implemented | Sales Consultant Agent scheduler dengan AI-powered follow-up |
| `run_master_hunter.py` | ✅ implemented | Master Hunter Orchestrator (5 parallel agents) |
| `enhanced_backup_system.py` | ✅ implemented | Multi-storage backup (Local, S3, GDrive) |
| `cron_revival_protocol.py` | ✅ implemented | Lead revival system dengan AI-powered closing tactics |
| `backup_db.py`, `backup_db.sh`, `backup_postgresql.sh` | ✅ implemented | Database backup scripts |
| `cleanup_system.py`, `cleanup_sqlite_references.py` | ✅ implemented | System cleanup scripts |
| `create_sample_leads.py`, `simple_insert_leads.py` | ✅ implemented | Lead creation scripts |
| `deploy_production.sh` | ✅ implemented | Production deployment script |
| `integrate_security_modules.py` | ✅ implemented | Security modules integration |
| `integration_checker.py` | ✅ implemented | Integration checker |
| `migrate_database.py`, `migrate_vault.py` | ✅ implemented | Database migration scripts |
| `monitor_system.py` | ✅ implemented | System monitoring script |
| `run_server_with_backup.py` | ✅ implemented | Server runner dengan backup |
| `simulate_incoming_leads.py` | ✅ implemented | Lead simulation script |
| `test_webhook.sh` | ✅ implemented | Webhook testing script |

## Tasks Folder (Celery Task Queue - IMPLEMENTED)

| Module | Status | Notes |
|---|---|---|
| `celery_app.py` | ✅ implemented | Enterprise-grade task queue dengan Redis broker |
| `intelligence_tasks.py` | ✅ implemented | Lead scouting, market analysis, area intelligence |
| `visual_tasks.py` | ✅ implemented | ComfyUI, video generation, PDF creation, image processing |
| `notification_tasks.py` | ✅ implemented | Email, WhatsApp, Telegram, SMS, campaign notifications |
| `maintenance_tasks.py` | ✅ implemented | System maintenance tasks |
| `runner_tasks.py` | ✅ implemented | Task execution runners |

## Tests Folder (14+ test files - IMPLEMENTED)

| Module | Status | Notes |
|---|---|---|
| `test_api_endpoints.py` | ✅ implemented | API endpoint testing |
| `test_auth_api.py` | ✅ implemented | Authentication API testing |
| `test_brochure.py` | ✅ implemented | Brochure testing |
| `test_commission_simple.py` | ✅ implemented | Commission testing |
| `test_commission_tracker.py` | ✅ implemented | Commission tracker testing |
| `test_critical_files.py` | ✅ implemented | Critical files testing |
| `test_data_isolation.py` | ✅ implemented | Data isolation testing |
| `test_final_commission.py` | ✅ implemented | Final commission testing |
| `test_inbox_api.py` | ✅ implemented | Inbox API testing |
| `test_masterpiece_brochure.py` | ✅ implemented | Masterpiece brochure testing |
| `test_mock_sync.py` | ✅ implemented | Mock sync testing |
| `test_predictive_scoring.py` | ✅ implemented | Predictive scoring testing |
| `test_senior_3d_artist_standards.py` | ✅ implemented | 3D artist standards testing |
| `test_webhook_api.py` | ✅ implemented | Webhook API testing |

## Config Folder (IMPLEMENTED)

| Module | Status | Notes |
|---|---|---|
| `agency_marketing_database.json` | ✅ implemented | Agency marketing database |
| `banten_government_sources.json` | ✅ implemented | Banten government sources |
| `banten_ministry_sources.json` | ✅ implemented | Banten ministry sources |
| `banten_property_database.json` | ✅ implemented | Banten property database |
| `competitors_list.json` | ✅ implemented | Competitors list |
| `config.py` | ✅ implemented | Configuration module |
| `system_prompts.py` | ✅ implemented | System prompts untuk agents |
| `nginx/` | ✅ implemented | Nginx configuration |
| `proxy_config.json` | ✅ implemented | Proxy configuration |
| `sources.json` | ✅ implemented | Sources configuration |

## Lumina OS Sub-Project (IMPLEMENTED)

| Module | Status | Notes |
|---|---|---|
| `api/` | ✅ implemented | API module dengan endpoints |
| `src/dashboard.html` | ✅ implemented | Dashboard UI |
| `src/index.html` | ✅ implemented | Index page |
| `src/leads.html` | ✅ implemented | Leads page |
| `app.py` | ✅ implemented | Main application |
| `core_modules/` | ✅ implemented | Core modules integration |
| `.env` | ✅ implemented | Environment configuration |

## Frontend Folder (IMPLEMENTED)

| Module | Status | Notes |
|---|---|---|
| `components/SentinelGazeReaction.tsx` | ✅ implemented | Sentinel Gaze Tracker component |
| `components/VirtualTour.jsx` | ✅ implemented | Virtual Tour component |
| `pdf_engine/DaVinciLayout.tsx` | ✅ implemented | DaVinci PDF layout |
| `pdf_engine/EditorialLayout.tsx` | ✅ implemented | Editorial PDF layout |

## App Folder (PARTIALLY IMPLEMENTED)

| Module | Status | Notes |
|---|---|---|
| `growth/` | ✅ implemented | Growth module |
| `p/` | ✅ implemented | Pages module |
| `templates/` | ✅ implemented | Templates |

## Assets Folder (IMPLEMENTED)

| Module | Status | Notes |
|---|---|---|
| `bps_serang.csv` | ✅ implemented | BPS Serang data |
| `documents/` | ✅ implemented | Documents directory |
| `dok pic page/` | ✅ implemented | Picture page documents |
| `media/` | ✅ implemented | Media directory |
| `templates/` | ✅ implemented | Templates |
| `verified_social_proof/` | ✅ implemented | Verified social proof |

## Prioritization

### Phase 0: New Critical Features (Week 1-2) - ✅ COMPLETED
1. ✅ Implement Archidep M2M Webhook Integration untuk transfer file siteplan otomatis
2. ⏭️ Setup DevSecOps & Code Quality (ESLint, Prettier, TypeScript, pre-commit hooks) - SKIPPED due to TypeScript strict mode issues
3. ✅ Implement PostgreSQL Optimization Patterns (full-text search, JSONB indexing, batch INSERT)

**Note:** Phase ini khusus untuk proyek properti dengan Archidep dan production readiness.

### Phase 1: Critical Tech Stack Gaps (Week 1-2) - ✅ COMPLETED
1. ✅ Add react-hook-form + Zod for all forms
2. ✅ Add @tanstack/react-query for data fetching
3. ✅ Add dinero.js for financial calculations
4. ✅ Add exceljs for reporting exports
5. ✅ Add react-leaflet for property mapping

### Phase 2: Backend Stability (Week 3-4)
1. Stabilize blocked backend routes
2. Complete page/detail data contracts
3. Add audit trails to Prisma schema
4. Add rate limiting with slowapi
5. Setup Turborepo for monorepo

### Phase 3: UI Standardization (Week 5-8)
1. Standardize all remaining pages to the same shell
2. Upgrade Next.js to 15 with Turbopack
3. Upgrade TailwindCSS to 4
4. Add next-seo + sitemap
5. Add PostHog analytics

### Phase 4: Feature Depth (Week 9-12)
1. Finish workflow, creative, asset, and governance feature depth
2. Add Playwright for E2E testing
3. Migrate to Supabase Auth
4. Add Casbin for RBAC
5. Migrate to pnpm package manager

## Overall Implementation Status

- **Implemented:** ~70% dari fitur core sudah diimplementasikan
- **Partially Implemented:** ~20% membutuhkan completion
- **Not Implemented:** ~10% ide baru yang belum dimulai

**Laporan lengkap tersedia di:** `laporan_komprehensif_final.md`

