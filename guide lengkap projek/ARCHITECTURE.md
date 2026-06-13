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

## 10-Dimension Health Check Integration

This architecture is periodically evaluated using a 10-dimension health framework:

### Structure & Organization (Dimension 1)
- **Current**: 15 organized folders in root
- **Status**: ✅ Good - Well-categorized structure
- **Note**: .config folder contains 21,649 files (node_modules + .venv)

### Code Quality (Dimension 2)
- **Status**: ⚠️ Needs deeper analysis
- **Action**: Review code quality metrics and linting rules

### Documentation (Dimension 3)
- **Current**: 10 files in guide lengkap projek, 103 files in Add file
- **Status**: ✅ Good - Comprehensive documentation
- **Note**: Add file needs review for relevance

### Testing (Dimension 4)
- **Current**: 14 test files for large project
- **Status**: ⚠️ Minimal - Needs expansion per ROADMAP Phase 5

### Security (Dimension 5)
- **Status**: ⚠️ Needs review
- **Action**: Review .env files and security configuration

### Performance (Dimension 6)
- **Status**: ⚠️ Needs analysis
- **Action**: Monitor performance metrics

### Scalability (Dimension 7)
- **Status**: ⚠️ Needs analysis
- **Action**: Review architecture for scalability

### Maintainability (Dimension 8)
- **Status**: ✅ Good
- **Note**: Folder structure supports maintainability

### User Experience (Dimension 9)
- **Status**: ⚠️ Needs analysis
- **Action**: Review dashboard UX

### Deployment & DevOps (Dimension 10)
- **Status**: ✅ Good - Docker files present
- **Note**: Docker files in root could be moved to dedicated folder

## Tech Stack Gaps (Priority Order)

### Phase 1: Critical (Week 1-2)
1. Add react-hook-form + Zod for form validation
2. Add @tanstack/react-query for data fetching
3. Add dinero.js for financial precision
4. Add exceljs for Excel export
5. Add react-leaflet for property mapping

### Phase 2: Infrastructure (Week 3-4)
1. Migrate to Turborepo for monorepo management
2. Setup GitHub Actions for CI/CD
3. Add commitlint for commit standards
4. Add audit trails to Prisma schema
5. Add rate limiting with slowapi

### Phase 3: Enhancement (Week 5-8)
1. Upgrade Next.js to 15 with Turbopack
2. Upgrade TailwindCSS to 4
3. Add next-seo + sitemap generation
4. Add PostHog for analytics
5. Add Playwright for E2E testing

### Phase 4: Advanced (Week 9-12)
1. Migrate to Supabase Auth
2. Add Casbin for RBAC
3. Migrate Jest to Vitest
4. Add react-pdf for PDF generation
5. Migrate to pnpm package manager

