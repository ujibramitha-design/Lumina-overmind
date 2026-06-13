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

### Critical Gaps (To Add)
- **react-hook-form + Zod** → Form management
- **@tanstack/react-query** → Data fetching
- **dinero.js** → Financial precision
- **exceljs** → Excel export
- **react-leaflet** → GIS/Mapping

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

## Prioritization

### Phase 1: Critical Tech Stack Gaps (Week 1-2)
1. Add react-hook-form + Zod for all forms
2. Add @tanstack/react-query for data fetching
3. Add dinero.js for financial calculations
4. Add exceljs for reporting exports
5. Add react-leaflet for property mapping

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

