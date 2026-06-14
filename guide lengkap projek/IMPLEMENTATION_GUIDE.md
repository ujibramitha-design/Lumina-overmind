# Implementation Guide

## Implementation Order (Updated with Tech Stack Priorities)

Use this order for safe delivery:

### Phase 0: New Critical Features (Week 1-2) - ✅ COMPLETED
**Priority: HIGH - Production Readiness & Property Project Integration**
1. ✅ Implement Archidep M2M Webhook Integration untuk transfer file siteplan otomatis
2. ⏭️ Setup DevSecOps & Code Quality (ESLint, Prettier, TypeScript, pre-commit hooks) - SKIPPED due to TypeScript strict mode issues
3. ✅ Implement PostgreSQL Optimization Patterns (full-text search, JSONB indexing, batch INSERT)

**Note:** Phase ini khusus untuk proyek properti dengan Archidep dan production readiness.

### Phase 1: Critical Tech Stack Gaps (Week 1-2) - ✅ COMPLETED
**Priority: CRITICAL - Must complete first**
1. ✅ Install and configure react-hook-form + Zod for all forms
2. ✅ Setup @tanstack/react-query for data fetching and caching
3. ✅ Add dinero.js for financial precision calculations
4. ✅ Add exceljs for Excel export functionality
5. ✅ Add react-leaflet for property mapping/GIS

### Phase 2: Infrastructure & Performance Upgrades (Week 3-4) - ✅ SEBAGIAN COMPLETED
**Priority: HIGH - Performance & DevOps**
1. ✅ Upgrade Next.js to 15 with Turbopack
2. ⏭️ Upgrade TailwindCSS to 4 (SKIPPED - belum stabil)
3. ✅ Add Playwright for E2E testing
4. ✅ Add next-seo + sitemap for SEO
5. ✅ Add PostHog for analytics
6. ✅ Add Casbin for authorization
7. ✅ Add slowapi for rate limiting
8. ⏭️ Migrate to Turborepo for monorepo management (SKIPPED - git submodule issues)
9. ✅ Setup GitHub Actions for CI/CD
10. ✅ Add commitlint for commit standards
11. ⏭️ Switch to pnpm package manager (SKIPPED - migrasi kompleks)
12. ⏳ Upgrade TanStack Table to v8 (pending)
13. ⏳ Migrate Jest to Vitest (pending)

### Phase 3: High-traffic Operational Pages (Week 5-6)
1. Standardize UI shell across all pages
2. Complete detail pages (leads/[id], projects/[id])
3. Upgrade Next.js to 15 with Turbopack
4. Upgrade TailwindCSS to 4

### Phase 4: AI/Orchestration Modules (Week 7-8)
1. Stabilize J.A.R.V.I.S. commands
2. Add next-seo + sitemap generation
3. Add PostHog for analytics
4. Complete workflow runtime and versioning

### Phase 5: Creative and Asset Pipelines (Week 9-10)
1. Add react-pdf for PDF generation
2. Complete upload queue and approval flows
3. Add Playwright for E2E testing

### Phase 6: Governance and Audit Improvements (Week 11-12)
1. Migrate to Supabase Auth
2. Add Casbin for RBAC
3. Migrate to pnpm package manager
4. Complete policy engine and compliance reporting

## Backend Stability First

Fix these before expanding UI:
- `/api/leads` database mismatch
- any route that breaks build or prerender
- AI provider dependency and environment mismatches
- config vault / secret retrieval failures

## UI Shell Standard

All dashboard pages should share:
- dark tactical background
- emerald accent
- left sidebar
- sticky top header
- panel cards with dense layout
- table/list/filter/search controls

## Feature Depth by Module

### Dashboard
- metrics
- quick actions
- alert summary
- search
- recent activity

### Geo Intel
- map canvas
- filters
- drill-down
- layers
- export/reporting

### Inbox
- queue
- draft review
- assignment
- message templates
- history

### Growth
- campaign summary
- budget pacing
- ROI tracking
- conversion attribution

### Projects
- project directory
- detail page
- pricing
- status
- asset and lead linkage

### Settings
- config versioning
- rollback
- role gates
- audit trace

### Jarvis
- command history
- command-to-backend mapping
- live status
- recovery handling

### Workflows
- template library
- validation
- test-run
- publish/rollback

### Partner
- onboarding
- partner tiers
- commission ledger
- payout history

### Governance
- terminal logs
- policy engine
- incident queue
- compliance reporting

### Assets / Creative
- upload queue
- tagging
- search
- approval state
- versioning
- publish flow

## Detail Page Expectations

Detail pages such as `leads/[id]` and `projects/[id]` should contain:
- summary header
- source/project context
- timeline/history
- actions panel
- related records
- backend-linked state

## Completion Criteria

A module is complete only when:
- page renders in the shared shell
- data contract exists
- primary actions work
- empty/error states are handled
- backend route does not break build

