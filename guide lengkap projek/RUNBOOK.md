# Runbook

## Local Development

Frontend:
```bash
cd dashboard
npm run dev
```

Backend:
```bash
cd ..
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
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

