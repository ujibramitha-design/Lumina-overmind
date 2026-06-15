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
1. ✅ Install and configure react-hook-form + Zod for all forms (INTEGRATED - form-helpers.ts)
2. ✅ Setup @tanstack/react-query for data fetching and caching (INTEGRATED - ReactQueryProvider)
3. ✅ Add dinero.js for financial precision calculations (INTEGRATED - financial-utils.ts)
4. ✅ Add exceljs for Excel export functionality (INTEGRATED - excel-export.ts)
5. ✅ Add react-leaflet for property mapping/GIS (INTEGRATED - PropertyMap component)

### Phase 2: Infrastructure & Performance Upgrades (Week 3-4) - ✅ FULLY COMPLETED
**Priority: HIGH - Performance & DevOps**
1. ✅ Upgrade Next.js to 15 with Turbopack
2. ⏭️ Upgrade TailwindCSS to 4 (SKIPPED - belum stabil)
3. ✅ Add Playwright for E2E testing (config created)
4. ✅ Add next-seo + sitemap for SEO (config created)
5. ✅ Add PostHog for analytics (integrated in dashboard)
6. ✅ Add Casbin for authorization (RBAC policy configured)
7. ✅ Add slowapi for rate limiting (integrated in FastAPI)
8. ⏭️ Migrate to Turborepo for monorepo management (SKIPPED - git submodule issues)
9. ✅ Setup GitHub Actions for CI/CD
10. ✅ Add commitlint for commit standards
11. ⏭️ Switch to pnpm package manager (SKIPPED - migrasi kompleks)
12. ✅ Upgrade TanStack Table to v8
13. ✅ Migrate Jest to Vitest

### Phase 3: Standardize UI & Complete Pages (Week 5-6) - ✅ COMPLETED
**Priority: HIGH - User Experience**
1. ✅ Standardize UI shell across all pages (Sidebar + TopHeader)
2. ✅ Complete detail pages (leads/[id], projects/[id])
3. ✅ Create leads listing page
4. ✅ Remove dashboard submodule and add as regular directory

### Phase 4: AI Orchestration & Analytics (Week 7-8) - ✅ COMPLETED
**Priority: HIGH - AI System Stability**
1. ✅ Stabilize J.A.R.V.I.S. commands
2. ✅ Add command history and analytics
3. ✅ Connect workflows to backend execution
4. ✅ Improve fallback behavior

### Phase 5: Creative and Asset Pipelines (Week 9-10) - ✅ COMPLETED
**Priority: MEDIUM - Asset Management**
1. ✅ Add react-pdf for PDF generation
2. ✅ Complete upload queue and approval flows
3. ✅ Add tagging and search for assets

### Phase 6: Governance and Audit Improvements (Week 11-12) - ✅ COMPLETED
1. ✅ Migrate to Supabase Auth
2. ✅ Add Casbin for RBAC
3. ⏭️ Migrate to pnpm package manager (SKIPPED - migrasi kompleks)
4. ✅ Complete policy engine and compliance reporting

### Phase 7: Regional Expansion - Indonesia (Week 13-14) - ✅ COMPLETED
**Priority: HIGH - Indonesia Market Readiness**
1. ✅ Implement WCAG compliance (Dimension 11) - COMPLETED
   - ✅ Accessibility wrapper component
   - ✅ Skip to main content link
   - ✅ Accessibility helper functions
   - ✅ Accessibility CSS styles (screen reader, focus, reduced motion, high contrast)
   - ✅ Removed emojis from navigation for screen readers
   - ✅ Added main-content landmark
   - ✅ ARIA labels for Button component
   - ✅ ARIA labels for Input component
   - ✅ ARIA labels for Textarea component
   - ✅ ARIA labels for Switch component
   - ✅ ARIA labels for Slider component
   - ✅ ARIA labels for TabsTrigger component
   - ✅ AccessibleImage component with required alt text
2. ✅ Add multi-language support for Indonesia (Dimension 12) - COMPLETED
   - ✅ LanguageSwitcher component
   - ✅ Comprehensive Indonesian translations (id.json)
   - ✅ Comprehensive English translations (en.json)
   - ✅ Sidebar navigation with i18n support
   - ✅ Language switcher in sidebar footer
3. ✅ Implement PDP Law Indonesia compliance (Dimension 13) - COMPLETED
   - ✅ PDP compliance API endpoints
   - ✅ Privacy policy (Indonesian and English)
   - ✅ Consent management endpoints
   - ✅ Data deletion request endpoints
   - ✅ Data export endpoints
   - ✅ Retention policy endpoints
   - ✅ Consent withdrawal endpoints
4. ✅ Add data protection implementation (Dimension 14) - COMPLETED
   - ✅ Data protection module (encryption, masking, classification)
   - ✅ Data protection API endpoints
   - ✅ Email, phone, credit card masking
   - ✅ Data anonymization utilities
   - ✅ Data classification by sensitivity level
5. ✅ Implement cloud cost optimization API (Dimension 15) - COMPLETED
   - ✅ Cost metrics tracking endpoints
   - ✅ Optimization recommendations engine
   - ✅ Budget management and alerts
   - ✅ Cost forecasting
   - ✅ Cost breakdown by category
   - ✅ Anomaly detection
   - ✅ Savings opportunities analysis

### Phase 8: Asia Expansion (Week 15-16) - ✅ COMPLETED
**Priority: HIGH - Asia Market Readiness**
1. ✅ Add multi-currency support (Dimension 16) - COMPLETED
   - ✅ Currency converter module (IDR, SGD, MYR, THB, VND, PHP, USD)
   - ✅ Currency formatting utilities
   - ✅ Exchange rate management
   - ✅ Currency API endpoints
2. ✅ Add multi-timezone support (Dimension 17) - COMPLETED
   - ✅ Timezone manager for Asia markets (WIB, WITA, WIT, Singapore, Malaysia, Thailand, Vietnam, Philippines)
   - ✅ Timezone conversion utilities
   - ✅ Business hours checking
   - ✅ Relative time formatting
   - ✅ Timezone API endpoints
3. ✅ Implement cross-border data compliance (Dimension 18) - COMPLETED
   - ✅ Asia data transfer regulations (Indonesia UU PDP, Singapore PDPA, Malaysia PDPA, Thailand PDPA, Vietnam Decree, Philippines Data Privacy Act)
   - ✅ Compliance checking endpoints
   - ✅ Data transfer logging
   - ✅ Consent template generation
   - ✅ Data localization checking

### Phase 9: Global International Expansion (Week 17-18) - ✅ COMPLETED
**Priority: HIGH - Global Market Readiness**
1. ✅ Implement cultural adaptation and RTL support (Dimension 19) - COMPLETED
   - ✅ Cultural adapter module (RTL support for Arabic, Hebrew, Persian, Urdu)
   - ✅ Cyrillic support for Russian and Eastern European languages
   - ✅ Script detection (Arabic, Cyrillic, CJK, Thai, Hangul, Latin)
   - ✅ Number formatting by culture
   - ✅ Date formatting by culture
   - ✅ RTL layout mirroring utilities
   - ✅ Cultural adaptation API endpoints

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

