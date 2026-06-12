# Lumina Overmind Working Guide

This repository is a dual-stack enterprise application:
- `dashboard/` is the Next.js front end and product UI.
- `api/` is the FastAPI backend and system integration layer.
- `core_modules/`, `agents/`, `tasks/`, and `database/` hold shared runtime logic, automation, and data support.

Use this guide as the working entry point when implementing changes.

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
7. Existing docs for deeper areas:
   - `README.md`
   - `dashboard/README_SETUP.md`
   - `dashboard/DASHBOARD_AUDIT_REPORT.md`
   - `api` documentation files

## Working Rules

- Do not redesign pages one by one without checking the module matrix first.
- Do not treat visual polish as completion if the backend contract is still missing.
- Keep the login/auth style as the canonical visual language for dashboard surfaces.
- Stabilize route/data dependencies before expanding new screens.

## Known Current Blockers

- Build still fails on `/api/leads` because the SQLite schema state does not match route expectations.
- Some AI paths depend on Gemini/OpenAI packages and environment variables that must be validated together.
- A few routes are still placeholder or partially implemented, especially detail pages and asset/creative flows.

