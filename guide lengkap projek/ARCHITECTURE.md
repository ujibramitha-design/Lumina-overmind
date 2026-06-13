# Architecture

## System Overview

Lumina Overmind is split into:
- `dashboard/`: Next.js 14 product UI, route shells, dashboards, forms, charts, and interactive control surfaces
- `api/`: FastAPI backend for auth, leads, projects, ads, workflows, jarvis, assets, security, and integrations
- `core_modules/`: shared intelligence, fallback, orchestration, storage, and helper systems
- `agents/`: scouting and automation agents
- `database/`: Prisma schema and PostgreSQL persistence assets

## Tech Stack (Best-in-Class)

### Frontend
- **Framework:** Next.js 14 (target: upgrade to 15 with Turbopack)
- **UI Library:** shadcn/ui + Radix UI
- **Styling:** TailwindCSS 3.3.0 (target: upgrade to 4)
- **State Management:** Zustand
- **Data Fetching:** @tanstack/react-query (to be added)
- **Form Management:** react-hook-form + Zod (to be added)
- **Charts:** Recharts
- **Data Grid:** TanStack Table
- **3D Graphics:** Three.js + React Three Fiber
- **Animation:** Framer Motion + GSAP
- **Icons:** Lucide React
- **TypeScript:** Strict mode enabled

### Backend
- **Framework:** FastAPI
- **Database:** PostgreSQL (Supabase)
- **ORM:** Prisma 7.8.0
- **Authentication:** JWT (PyJWT, python-jose) + Passlib (bcrypt)
- **Background Jobs:** Celery + Redis
- **WebSocket:** Socket.IO
- **Encryption:** cryptography
- **Monitoring:** Sentry, Prometheus, Grafana
- **Logging:** structlog

### Infrastructure
- **Package Manager:** npm (target: migrate to pnpm)
- **Monorepo:** Not yet implemented (target: Turborepo)
- **CI/CD:** Not yet implemented (target: GitHub Actions)
- **Containerization:** Docker + Docker Compose

## Request Flow

Typical path:
1. User interacts with a dashboard page.
2. The page reads data from a dashboard API route or backend endpoint.
3. The API route proxies or transforms data from the backend layer.
4. Backend services read database or external integrations.
5. UI renders the response into panel, table, map, or workflow surface.

## Frontend Layout Layers

### App Shell
- `dashboard/app/layout.tsx`
- `dashboard/middleware.ts`
- `dashboard/components/Sidebar.tsx`
- `dashboard/components/TopHeader.tsx`

### Page Types
- Command center pages: `dashboard`, `jarvis`, `governance`
- Operational pages: `inbox`, `projects`, `partner`, `growth`, `settings`
- Intelligence pages: `geo-intel`, `leads/[id]`, `workflows`, `orchestrator`
- Asset/creative pages: `dashboard/assets`, `creative`, `landing`, `ads-approval`

## Backend Layers

### FastAPI Entry
- `api/main.py`

### Common Endpoint Families
- authentication and security
- leads and projects
- intelligence and analytics
- workflows and orchestration
- J.A.R.V.I.S. control
- asset and visual services
- webhooks and notifications

### Support Utilities
- `api/utils/conversational_ai.py`
- `api/utils/encryption.py`
- `core_modules/vault_manager.py`
- `core_modules/model_fallback.py`

## Visual System Direction

Canonical style:
- dark tactical UI
- emerald accent
- high contrast
- dense enterprise panels
- data-first layouts

Use this style consistently across dashboard pages. Do not mix marketing-style card layouts into operational surfaces.

## Risk Areas

- Database contract mismatch on `leads`
- Pages that rely on backend endpoints not yet stable
- AI provider dependency and env-variable mismatches
- Mixed legacy and new UI surfaces
- **CRITICAL:** Missing form management (react-hook-form + Zod)
- **CRITICAL:** Missing data fetching library (@tanstack/react-query)
- **CRITICAL:** Missing financial precision library (dinero.js)
- **CRITICAL:** Missing Excel export capability (exceljs)
- **CRITICAL:** Missing GIS/Mapping capability (react-leaflet)
- **NEW:** Archidep M2M Webhook Integration belum diimplementasikan (HIGH priority untuk proyek properti)
- **NEW:** DevSecOps & Code Quality Setup belum lengkap (HIGH priority untuk production readiness)
- **NEW:** PostgreSQL Optimization Patterns belum diimplementasikan (MEDIUM priority untuk performance)

## 19-Dimension Global Standard Health Check Integration

This architecture is periodically evaluated using a 19-dimension global standard health framework. See `19_DIMENSIONS_GLOBAL_STANDARD.md` for detailed documentation.

### Scale Progression
- **Indonesia**: 15 dimensions (1-15)
- **Asia**: 18 dimensions (1-18)
- **Global Internasional**: 19 dimensions (1-19)

### Note on Removed Dimensions
Framework ini dioptimasi untuk konteks pasukan hunter scraping & market expansion:
- **Environmental Sustainability** - Tidak relevan untuk scraping operations
- **Supply Chain & Vendor Management** - Tidak relevan untuk scraping operations
- **AI Ethics & Compliance** - Optional, dapat ditambahkan jika menggunakan AI untuk decision-making

### Core Dimensions (1-10) - Current Status

#### Structure & Organization (Dimension 1)
- **Current**: 15 organized folders in root
- **Status**: ✅ Good - Well-categorized structure
- **Note**: .config folder contains 21,649 files (node_modules + .venv)

#### Code Quality (Dimension 2)
- **Status**: ⚠️ Needs deeper analysis
- **Action**: Review code quality metrics and linting rules

#### Documentation (Dimension 3)
- **Current**: 11 files in guide lengkap projek, 103 files in Add file
- **Status**: ✅ Good - Comprehensive documentation
- **Note**: Add file needs review for relevance

#### Testing (Dimension 4)
- **Current**: 14 test files for large project
- **Status**: ⚠️ Minimal - Needs expansion per ROADMAP Phase 5

#### Security (Dimension 5)
- **Status**: ⚠️ Needs review
- **Action**: Review .env files and security configuration

#### Performance (Dimension 6)
- **Status**: ⚠️ Needs analysis
- **Action**: Monitor performance metrics

#### Scalability (Dimension 7)
- **Status**: ⚠️ Needs analysis
- **Action**: Review architecture for scalability

#### Maintainability (Dimension 8)
- **Status**: ✅ Good
- **Note**: Folder structure supports maintainability

#### User Experience (Dimension 9)
- **Status**: ⚠️ Needs analysis
- **Action**: Review dashboard UX

#### Deployment & DevOps (Dimension 10)
- **Status**: ✅ Good - Docker files present
- **Note**: Docker files in root could be moved to dedicated folder

### Regional Dimensions (11-15) - Not Yet Implemented
- 11. Accessibility: ⬜ Not started
- 12. Internationalization (i18n): ⬜ Not started
- 13. Compliance & Legal: ⬜ Not started
- 14. Data Privacy: ⬜ Not started
- 15. Cost Management: ⬜ Not started

### Asia Dimensions (16-18) - Not Yet Implemented
- 16. Multi-Currency Support: ⬜ Not started
- 17. Multi-Timezone Support: ⬜ Not started
- 18. Cross-Border Data Transfer: ⬜ Not started

### Global International Dimension (19) - Not Yet Implemented
- 19. Cultural Adaptation & RTL Support: ⬜ Not started

## Tech Stack Gaps (Priority Order) - FINAL RECOMMENDATION

### Keep (Already Best-in-Class)
- Next.js (upgrade to 15)
- FastAPI
- shadcn/ui + Radix UI
- TailwindCSS (upgrade to 4)
- Prisma
- PostgreSQL + Supabase
- Zustand
- Framer Motion
- Three.js + R3F
- Sentry
- Prometheus + Grafana
- ESLint + Prettier
- pytest

### Add (Critical) - ✅ COMPLETED
- ✅ react-hook-form + Zod
- ✅ @tanstack/react-query
- ✅ dinero.js
- ✅ exceljs
- ✅ react-leaflet
- ⏳ Playwright (pending)
- ⏳ next-seo + sitemap (pending)
- ⏳ PostHog (pending)
- ⏳ Casbin (pending)
- ⏳ slowapi (pending)

### Upgrade (Performance) - PENDING
- ⏳ Next.js 14 → 15 (Turbopack)
- ⏳ TailwindCSS 3 → 4
- ⏳ TanStack Table v8
- ⏳ Jest → Vitest
- ⏳ pnpm (package manager)

### New Infrastructure - PENDING
- ⏳ Turborepo (monorepo)
- ⏳ GitHub Actions (CI/CD)
- ⏳ commitlint (commit standards)

### Phase 0: New Critical Features (Week 1-2) - ✅ COMPLETED
1. ✅ **Archidep M2M Webhook Integration** - Transfer file siteplan otomatis (HIGH priority untuk proyek properti)
2. ⏭️ **DevSecOps & Code Quality Setup** - ESLint, Prettier, TypeScript, pre-commit hooks (SKIPPED - TypeScript strict mode disabled due to existing code issues)
3. ✅ **PostgreSQL Optimization Patterns** - Full-text search, JSONB indexing, batch INSERT (MEDIUM priority untuk performance)

### Phase 1: Critical Tech Stack Gaps (Week 1-2) - ✅ COMPLETED
1. ✅ Add react-hook-form + Zod for form validation
2. ✅ Add @tanstack/react-query for data fetching
3. ✅ Add dinero.js for financial precision
4. ✅ Add exceljs for Excel export
5. ✅ Add react-leaflet for property mapping

### Phase 2: Infrastructure (Week 3-4) - PENDING
1. ⏳ Upgrade Next.js to 15 with Turbopack
2. ⏳ Upgrade TailwindCSS to 4
3. ⏳ Add Playwright for E2E testing
4. ⏳ Add next-seo + sitemap for SEO
5. ⏳ Add PostHog for analytics
6. ⏳ Add Casbin for authorization
7. ⏳ Add slowapi for rate limiting
8. ⏳ Migrate to Turborepo for monorepo management
9. ⏳ Setup GitHub Actions for CI/CD
10. ⏳ Add commitlint for commit standards
11. ⏳ Switch to pnpm package manager
12. ⏳ Upgrade TanStack Table to v8
13. ⏳ Migrate Jest to Vitest

## Additional Components Status

### Scripts Folder (20+ scripts - IMPLEMENTED)
- `run_closer_agent.py` - Sales Consultant Agent scheduler ✅
- `run_master_hunter.py` - Master Hunter Orchestrator (5 parallel agents) ✅
- `enhanced_backup_system.py` - Multi-storage backup (Local, S3, GDrive) ✅
- `cron_revival_protocol.py` - Lead revival system dengan AI-powered closing tactics ✅
- `backup_db.py`, `backup_db.sh`, `backup_postgresql.sh` - Database backup ✅
- `cleanup_system.py`, `cleanup_sqlite_references.py` - System cleanup ✅
- `create_sample_leads.py`, `simple_insert_leads.py` - Lead creation ✅
- `deploy_production.sh` - Production deployment ✅
- `integrate_security_modules.py` - Security integration ✅
- `integration_checker.py` - Integration checker ✅
- `migrate_database.py`, `migrate_vault.py` - Database migration ✅
- `monitor_system.py` - System monitoring ✅
- `run_server_with_backup.py` - Server with backup ✅
- `simulate_incoming_leads.py` - Lead simulation ✅
- `test_webhook.sh` - Webhook testing ✅

### Tasks Folder (Celery Task Queue - IMPLEMENTED)
- `celery_app.py` - Enterprise-grade task queue dengan Redis broker ✅
- `intelligence_tasks.py` - Lead scouting, market analysis, area intelligence ✅
- `visual_tasks.py` - ComfyUI, video generation, PDF creation, image processing ✅
- `notification_tasks.py` - Email, WhatsApp, Telegram, SMS, campaign notifications ✅
- `maintenance_tasks.py` - System maintenance tasks ✅
- `runner_tasks.py` - Task execution runners ✅

### Tests Folder (14+ test files - IMPLEMENTED)
- API endpoints, auth, brochure, commission testing ✅
- Data isolation, inbox API, predictive scoring ✅
- 3D artist standards, webhook API testing ✅

### Config Folder (IMPLEMENTED)
- Agency marketing database, government sources, property database ✅
- Competitors list, proxy configuration, sources configuration ✅
- System prompts untuk agents ✅
- Nginx configuration ✅

### Lumina OS Sub-Project (IMPLEMENTED)
- API module dengan endpoints ✅
- Dashboard UI (dashboard.html, index.html, leads.html) ✅
- Core modules integration ✅
- Environment configuration ✅

### Frontend Folder (IMPLEMENTED)
- `SentinelGazeReaction.tsx` - Sentinel Gaze Tracker component ✅
- `VirtualTour.jsx` - Virtual Tour component ✅
- `DaVinciLayout.tsx` - DaVinci PDF layout ✅
- `EditorialLayout.tsx` - Editorial PDF layout ✅

### App Folder (PARTIALLY IMPLEMENTED)
- Growth module ✅
- Pages module ✅
- Templates ✅

### Assets Folder (IMPLEMENTED)
- BPS Serang data ✅
- Documents, media, templates ✅
- Verified social proof ✅

## Overall Implementation Status

- **Implemented:** ~70% dari fitur core sudah diimplementasikan
- **Partially Implemented:** ~20% membutuhkan completion
- **Not Implemented:** ~10% ide baru yang belum dimulai

**Laporan lengkap tersedia di:** `guide lengkap projek/laporan_komprehensif_final.md`

