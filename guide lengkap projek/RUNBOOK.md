# Runbook

## Local Development

### Frontend (Next.js)
```bash
cd dashboard
npm install
npm run dev
```
- Runs on http://localhost:3000
- Hot reload enabled
- TypeScript strict mode

### Backend (FastAPI)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
- Runs on http://localhost:8000
- Hot reload enabled
- API docs at http://localhost:8000/docs (requires auth)

### Database (PostgreSQL via Supabase)
- Use Supabase cloud database
- Configure connection in `.env`
- Run migrations: `npm run prisma:migrate`
- Open Prisma Studio: `npm run prisma:studio`

### Background Jobs (Celery)
```bash
# Celery Worker
celery -A tasks.celery_app worker --loglevel=info

# Celery Beat (Scheduler)
celery -A tasks.celery_app beat --loglevel=info
```

### Redis (Required for Celery)
```bash
# Using Docker
docker-compose up redis

# Or install locally
redis-server
```

## What To Check First

1. Does the dashboard shell load?
2. Does login redirect to `/dashboard`?
3. Does `/api/leads` still fail during build or prerender?
4. Do jarvis and workflow routes render without missing dependencies?
5. Are environment variables loaded correctly for AI providers?

## Common Failure Modes

- Missing database table or schema mismatch
- Missing npm dependency in `dashboard/package.json`
- Missing Python dependency in `requirements.txt`
- Broken route import in `api/main.py`
- AI provider env mismatch, for example `GEMINI_API_KEY` vs `GOOGLE_GEMINI_API_KEY`
- **NEW:** Missing form validation (react-hook-form + Zod not installed)
- **NEW:** Missing data fetching (@tanstack/react-query not configured)
- **NEW:** Financial precision errors (dinero.js not used)

## Tech Stack Installation Commands

### Phase 1: Critical Dependencies (Week 1-2)
```bash
cd dashboard
npm install react-hook-form @hookform/resolvers zod
npm install @tanstack/react-query @tanstack/react-query-devtools
npm install dinero.js
npm install exceljs
npm install react-leaflet leaflet
npm install -D @types/leaflet
```

### Phase 2: Infrastructure (Week 3-4)
```bash
npm install -D turbo
npm install -D @commitlint/cli @commitlint/config-conventional
pip install slowapi
```

### Phase 3: Framework Upgrades (Week 5-8)
```bash
npm install next@15
npm install tailwindcss@next
npm install next-seo
npm install posthog-js
npm install -D @playwright/test
```

### Phase 4: Advanced (Week 9-12)
```bash
npm install @supabase/supabase-js
pip install casbin
npm install -D vitest @vitest/ui
npm install @react-pdf/renderer
npm install -g pnpm
```

## Recovery Steps

If the build fails:
1. identify the route causing prerender failure
2. verify the database/schema used by that route
3. confirm the backend endpoint returns expected shape
4. ensure all UI imports exist
5. rebuild after fixing the data contract

## Acceptance Checklist

- Shared shell renders
- Dashboard routes render
- Public routes do not break auth
- API routes do not break build
- AI routes have fallback behavior

