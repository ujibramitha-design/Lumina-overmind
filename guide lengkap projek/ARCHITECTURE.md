# Architecture

## System Overview

Lumina Overmind is split into:
- `dashboard/`: product UI, route shells, dashboards, forms, charts, and interactive control surfaces
- `api/`: FastAPI backend for auth, leads, projects, ads, workflows, jarvis, assets, security, and integrations
- `core_modules/`: shared intelligence, fallback, orchestration, storage, and helper systems
- `agents/`: scouting and automation agents
- `database/`: schema and persistence assets

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

