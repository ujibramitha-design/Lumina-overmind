# Roadmap

## Phase 1: Critical Tech Stack Gaps (Week 1-2)

**Priority: CRITICAL - Foundation for all other work**

Goals:
- Install react-hook-form + Zod for form validation
- Setup @tanstack/react-query for data fetching
- Add dinero.js for financial precision
- Add exceljs for Excel export
- Add react-leaflet for property mapping

**Deliverables:**
- Form validation system across all forms
- Data fetching with caching and deduplication
- Financial calculations without floating point errors
- Excel export functionality for reports
- Property location visualization with maps

## Phase 2: Backend Stability & Infrastructure (Week 3-4)

Goals:
- fix `/api/leads` database mismatch
- verify AI provider env and dependency setup
- ensure build passes without route failures
- confirm login and dashboard shell are stable
- Add audit trails to Prisma schema
- Add rate limiting with slowapi
- Setup Turborepo for monorepo
- Setup GitHub Actions for CI/CD

**Deliverables:**
- Stable backend API routes
- Audit logging for compliance
- Rate limiting for API protection
- Monorepo structure with Turborepo
- Automated CI/CD pipeline

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

