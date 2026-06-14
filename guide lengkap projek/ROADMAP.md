# Roadmap

## 19-Dimension Global Standard Health Check Integration

This roadmap is integrated with the 19-dimension global standard health framework. See `19_DIMENSIONS_GLOBAL_STANDARD.md` for detailed documentation.

### Scale Progression
- **Indonesia**: 15 dimensions (1-15)
- **Asia**: 18 dimensions (1-18)
- **Global Internasional**: 19 dimensions (1-19)

### Note on Removed Dimensions
Framework ini dioptimasi untuk konteks pasukan hunter scraping & market expansion:
- **Environmental Sustainability** - Tidak relevan untuk scraping operations
- **Supply Chain & Vendor Management** - Tidak relevan untuk scraping operations
- **AI Ethics & Compliance** - Optional, dapat ditambahkan jika menggunakan AI untuk decision-making

### Core Dimensions (1-10) Mapping
- **Dimension 1 (Structure)**: Addressed in Phase 2 (Turborepo, folder organization)
- **Dimension 2 (Code Quality)**: Addressed in Phase 2 (commitlint, audit trails)
- **Dimension 3 (Documentation)**: Ongoing - guide lengkap projek maintained
- **Dimension 4 (Testing)**: Addressed in Phase 5 (Playwright E2E testing)
- **Dimension 5 (Security)**: Addressed in Phase 2 (rate limiting, Phase 6 (Supabase Auth, Casbin RBAC))
- **Dimension 6 (Performance)**: Addressed in Phase 3 (Next.js 15 Turbopack, TailwindCSS 4)
- **Dimension 7 (Scalability)**: Addressed in Phase 2 (Turborepo, CI/CD)
- **Dimension 8 (Maintainability)**: Addressed in Phase 2 (audit trails, Phase 6 (policy engine))
- **Dimension 9 (UX)**: Addressed in Phase 3 (UI standardization)
- **Dimension 10 (DevOps)**: Addressed in Phase 2 (GitHub Actions, Docker optimization)

### Regional Dimensions (11-15) Mapping - Future Expansion
- **Dimension 11 (Accessibility)**: Future - WCAG compliance implementation
- **Dimension 12 (i18n)**: Future - Multi-language support for Indonesia
- **Dimension 13 (Compliance)**: Future - PDP Law Indonesia compliance
- **Dimension 14 (Data Privacy)**: Future - Data protection implementation
- **Dimension 15 (Cost Management)**: Future - Cloud cost optimization

### Asia Dimensions (16-18) Mapping - Future Expansion
- **Dimension 16 (Multi-Currency)**: Future - Currency support for Asia markets
- **Dimension 17 (Multi-Timezone)**: Future - Timezone support for Asia
- **Dimension 18 (Cross-Border Data)**: Future - Data transfer compliance for Asia

### Global International Dimension (19) Mapping - Future Expansion
- **Dimension 19 (Cultural Adaptation & RTL)**: Future - RTL support for Middle East, Cyrillic for Russia

### Optional: AI Ethics & Compliance
- **AI Ethics**: Optional - EU AI Act compliance (jika menggunakan AI untuk decision-making)

## Phase 0: New Critical Features (Week 1-2) - ✅ COMPLETED

**Priority: HIGH - Production Readiness & Property Project Integration**

Goals:
- ✅ Implement Archidep M2M Webhook Integration untuk transfer file siteplan otomatis
- ⏭️ Setup DevSecOps & Code Quality (ESLint, Prettier, TypeScript, pre-commit hooks) - SKIPPED due to TypeScript strict mode issues
- ✅ Implement PostgreSQL Optimization Patterns (full-text search, JSONB indexing, batch INSERT)

**Deliverables:**
- ✅ Archidep webhook endpoints dengan authentication dan file processing (`api/endpoints/archidep_webhook.py`)
- ⏭️ Complete DevSecOps setup dengan automated linting dan type checking - SKIPPED
- ✅ PostgreSQL performance optimization dengan proper indexing (GIN indexes added to schema.prisma)
- ✅ PostgreSQL optimization utility functions (`api/utils/postgres_optimization.py`)

**Note:** Phase ini khusus untuk proyek properti dengan Archidep dan production readiness.

## Phase 1: Critical Tech Stack Gaps (Week 1-2) - ✅ COMPLETED

**Priority: CRITICAL - Foundation for all other work**

Goals:
- ✅ Install react-hook-form + Zod for form validation
- ✅ Setup @tanstack/react-query for data fetching
- ✅ Add dinero.js for financial precision
- ✅ Add exceljs for Excel export
- ✅ Add react-leaflet for property mapping

**Deliverables:**
- ✅ Form validation system across all forms
- ✅ Data fetching with caching and deduplication
- ✅ Financial calculations without floating point errors
- ✅ Excel export functionality for reports
- ✅ Property location visualization with maps

## Phase 2: Infrastructure & Performance Upgrades (Week 3-4) - ✅ SEBAGIAN COMPLETED

Goals:
- ✅ Upgrade Next.js to 15 with Turbopack
- ⏭️ Upgrade TailwindCSS to 4 (SKIPPED - belum stabil)
- ✅ Add Playwright for E2E testing
- ✅ Add next-seo + sitemap for SEO
- ✅ Add PostHog for analytics
- ✅ Add Casbin for authorization
- ✅ Add slowapi for rate limiting
- ⏭️ Migrate to Turborepo for monorepo management (SKIPPED - git submodule issues)
- ✅ Setup GitHub Actions for CI/CD
- ✅ Add commitlint for commit standards
- ⏭️ Switch to pnpm package manager (SKIPPED - migrasi kompleks)
- ✅ Upgrade TanStack Table to v8
- ✅ Migrate Jest to Vitest

**Deliverables:**
- ✅ Next.js 15 + React 19
- ✅ Playwright untuk E2E testing
- ✅ next-seo + next-sitemap untuk SEO
- ✅ PostHog untuk analytics
- ✅ Casbin untuk authorization
- ✅ slowapi untuk rate limiting
- ✅ GitHub Actions CI/CD pipeline
- ✅ commitlint untuk commit standards
- ✅ TanStack Table v8
- ✅ Vitest untuk testing
- ⏭️ Monorepo structure dengan Turborepo (SKIPPED)
- ⏭️ pnpm package manager (SKIPPED)

## Phase 3: Standardize UI & Upgrade Framework (Week 5-6)

Goals:
- apply one shell and one design language to all operational pages
- finish detail pages
- align tables, cards, search bars, and filters
- Upgrade Next.js to 15 with Turbopack
- Upgrade TailwindCSS to 4

**Deliverables:**
- Consistent UI across all pages
- 700x faster builds with Turbopack
- Improved performance with TailwindCSS 4
- Complete detail pages (leads/[id], projects/[id])

## Phase 4: AI Orchestration & Analytics (Week 7-8)

Goals:
- stabilize J.A.R.V.I.S. commands
- add command history and analytics
- connect workflows to backend execution
- improve fallback behavior
- Add next-seo + sitemap generation
- Add PostHog for analytics

**Deliverables:**
- Stable J.A.R.V.I.S. command system
- SEO optimization with sitemap
- User behavior analytics with PostHog
- Workflow runtime completion

## Phase 5: Creative and Asset Pipelines (Week 9-10)

Goals:
- upload queue
- tagging and search
- approval/revision flow
- publish history
- project linkage
- Add react-pdf for PDF generation
- Add Playwright for E2E testing

**Deliverables:**
- Complete asset pipeline
- PDF generation for reports
- E2E test coverage
- Approval workflow completion

## Phase 6: Governance & Advanced Features (Week 11-12)

Goals:
- formalize runbooks
- document API contracts
- keep module matrix updated
- add testing coverage around blockers and critical flows
- Migrate to Supabase Auth
- Add Casbin for RBAC
- Migrate to pnpm package manager
- Complete policy engine and compliance reporting

**Deliverables:**
- Unified authentication with Supabase
- Role-based access control with Casbin
- Comprehensive governance system
- pnpm for faster package management
- Complete compliance reporting

