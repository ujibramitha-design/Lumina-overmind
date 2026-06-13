# Lumina Overmind Working Guide

This repository is a dual-stack enterprise application:
- `dashboard/` is the Next.js 14 front end and product UI.
- `api/` is the FastAPI backend and system integration layer.
- `core_modules/`, `agents/`, `tasks/`, and `database/` hold shared runtime logic, automation, and data support.

Use this guide as the working entry point when implementing changes.

## Tech Stack Overview

### Frontend (Best-in-Class)
- **Next.js 14** → Target: Upgrade to 15 with Turbopack
- **shadcn/ui + Radix UI** - Accessible component library
- **TailwindCSS 3.3.0** → Target: Upgrade to 4
- **Zustand** - Global state management
- **TanStack Table** - Data grid with virtualization
- **Recharts** - Charting library
- **Framer Motion + GSAP** - Animations
- **Three.js + React Three Fiber** - 3D graphics
- **TypeScript** - Strict mode enabled

### Backend (Best-in-Class)
- **FastAPI** - Modern async web framework
- **PostgreSQL (Supabase)** - Production database
- **Prisma 7.8.0** - Type-safe ORM
- **Celery + Redis** - Background job processing
- **JWT + Passlib** - Authentication
- **Socket.IO** - Real-time communication
- **Sentry** - Error tracking
- **Prometheus + Grafana** - Monitoring

### Critical Gaps (To Add)
- **react-hook-form + Zod** - Form validation
- **@tanstack/react-query** - Data fetching
- **dinero.js** - Financial precision
- **exceljs** - Excel export
- **react-leaflet** - GIS/Mapping

## What This Project Is

Lumina Overmind is an AI-assisted real-estate intelligence and operations platform. The product spans:
- lead discovery and qualification
- CRM and inbox operations
- project and partner management
- workflow automation
- governance and audit
- asset and creative pipelines
- J.A.R.V.I.S. command/control features

## Current Structure

### Frontend
- `dashboard/app/`
- `dashboard/components/`
- `dashboard/components/ui/`
- `dashboard/lib/`

### Backend
- `api/main.py`
- `api/endpoints/`
- `api/middleware/`
- `api/utils/`

### Shared / Support
- `core_modules/`
- `agents/`
- `templates/`
- `tasks/`
- `database/`
- `docs/`

## Recommended Reading Order

1. `docs/ARCHITECTURE.md`
2. `docs/MODULE_MATRIX.md`
3. `docs/IMPLEMENTATION_GUIDE.md`
4. `docs/API_CONTRACTS.md`
5. `docs/UI_SYSTEM.md`
6. `docs/RUNBOOK.md`
7. `docs/DEPLOYMENT_CHECKLIST.md` - For deployment preparation
8. Existing docs for deeper areas:
   - `README.md`
   - `dashboard/README_SETUP.md`
   - `dashboard/DASHBOARD_AUDIT_REPORT.md`
   - `api` documentation files

## Working Rules

- Do not redesign pages one by one without checking the module matrix first.
- Do not treat visual polish as completion if the backend contract is still missing.
- Keep the login/auth style as the canonical visual language for dashboard surfaces.
- Stabilize route/data dependencies before expanding new screens.

## Documentation Update Rule

**CRITICAL**: Any addition or modification to analysis, checklists, frameworks, or any documentation must be immediately updated in the "guide lengkap projek" folder. This ensures:
- All documentation remains synchronized
- The team always refers to the single source of truth
- No duplicate or contradictory information exists
- Changes are tracked and version-controlled

**Process**:
1. When adding new analysis or checklist → Update corresponding file in "guide lengkap projek"
2. When modifying existing analysis → Update the file in "guide lengkap projek"
3. When creating new framework → Add to "guide lengkap projek" and update README_WORKING_GUIDE.md
4. Always refer to "guide lengkap projek" as the primary source of truth

**Note**: These rules are also defined in `.windsurf/workflows/project-rules.md` for IDE integration. Both locations must be kept in sync.

## Progress Tracking Rule

**CRITICAL**: When working through checklists, roadmaps, or any action items:
- Always mark completed items as ✅ (completed)
- Never delete completed items - keep them for tracking history
- Mark incomplete items as ⬜ (not started) or ⏳ (in progress)
- This ensures:
  - Progress visibility at all times
  - Historical tracking of what has been done
  - Ability to resume work from where left off
  - Audit trail of completed tasks

**Format**:
- ✅ Item completed
- ⏳ Item in progress
- ⬜ Item not started
- ❌ Item blocked/cannot be completed

## Known Current Blockers

- Build still fails on `/api/leads` because the SQLite schema state does not match route expectations.
- Some AI paths depend on Gemini/OpenAI packages and environment variables that must be validated together.
- A few routes are still placeholder or partially implemented, especially detail pages and asset/creative flows.

## 22-Dimension Global Standard Health Analysis

This guide is complemented by a 22-dimension global standard health analysis framework. See `22_DIMENSIONS_GLOBAL_STANDARD.md` for detailed documentation of each dimension.

### Scale Progression
- **Indonesia**: 15 dimensions (1-15)
- **Asia**: 18 dimensions (1-18)
- **Eropa**: 20 dimensions (1-20)
- **Global Internasional**: 22 dimensions (1-22)

### Current Status (Core Dimensions 1-10)

#### 1. Struktur Kode & Organisasi
- **Status**: ✅ BAIK - Folder sudah terorganisir dengan kategori yang jelas
- **Current**: 15 folder di root (.config, Add file, api, app, assets, config, core_modules, dashboard, data, frontend, guide lengkap projek, logs, lumina_os, scripts, tasks, tests)
- **Note**: .config terlalu besar (21,649 file - node_modules + .venv)

#### 2. Kualitas Kode
- **Status**: ⚠️ PERLU ANALISA LEBIH DALAM
- **Action**: Review code quality metrics dan linting rules

#### 3. Dokumentasi
- **Status**: ✅ BAIK - guide lengkap projek dan Add file sudah ada
- **Current**: 11 file di guide lengkap projek, 103 file di Add file
- **Note**: Add file masih banyak, perlu review apakah semua masih relevan

#### 4. Testing
- **Status**: ⚠️ MINIMAL
- **Current**: Hanya 14 file test untuk proyek besar
- **Action**: Tambah test coverage sesuai ROADMAP.md Fase 5

#### 5. Security
- **Status**: ⚠️ PERLU CEK
- **Action**: Review file .env dan konfigurasi security

#### 6. Performance
- **Status**: ⚠️ PERLU ANALISA
- **Action**: Monitor performance metrics

#### 7. Scalability
- **Status**: ⚠️ PERLU ANALISA
- **Action**: Review architecture untuk scalability

#### 8. Maintainability
- **Status**: ✅ BAIK
- **Note**: Struktur folder mendukung maintainability

#### 9. User Experience
- **Status**: ⚠️ PERLU ANALISA
- **Action**: Review dashboard UX

#### 10. Deployment & DevOps
- **Status**: ✅ BAIK - Docker files sudah ada
- **Note**: File Docker di root bisa dipindahkan ke folder khusus

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

### Europe Dimensions (19-20) - Not Yet Implemented
- 19. Environmental Sustainability: ⬜ Not started
- 20. AI Ethics & Compliance: ⬜ Not started

### Global International Dimensions (21-22) - Not Yet Implemented
- 21. Cultural Adaptation & RTL Support: ⬜ Not started
- 22. Supply Chain & Vendor Management: ⬜ Not started

## Integration with Roadmap

The 22-dimension global standard analysis complements the 6-phase roadmap:
- **22-Dimension Analysis**: Provides overall project health check with scalability from Indonesia to global international
- **Roadmap**: Provides specific action items with timeline
- **Combined Approach**: Use roadmap for execution, use 22-dimension for periodic health checks

