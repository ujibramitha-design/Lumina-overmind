---
description: Retry Policy and Task Execution Rules
---

# Retry Policy and Task Execution Rules

## Retry Scale-Down Strategy

### Initial Phase (2x Retry Limit)
- **Max Retries:** 2 attempts per task
- **On Failure (>2x):** Skip task and move to next task in current phase
- **Continue:** Execute remaining tasks in current phase

### Pending Task Resolution
- **Trigger:** When current phase completes successfully
- **Action:** Return to skipped/pending tasks
- **Retry Limit:** Still 2 attempts per task
- **On Success:** Mark as complete
- **On Failure (>2x):** Scale down to 5x retry limit

### Scale-Down Phase (5x Retry Limit)
- **Max Retries:** 5 attempts per task
- **On Failure (>5x):** Try 1 final time (6th attempt)
- **On 6th Failure:** Stop task permanently and log as blocked

## Execution Order

### Phase 0: Critical Infrastructure
1. Fix `/api/leads` database mismatch
2. Setup DevSecOps & Code Quality (ESLint, Prettier, TypeScript, pre-commit hooks)
3. Implement PostgreSQL Optimization Patterns

### Phase 1: Critical Tech Stack Gaps
1. Install react-hook-form + Zod
2. Setup @tanstack/react-query
3. Add dinero.js
4. Add exceljs
5. Add react-leaflet

### Phase 2: Backend Stability & Infrastructure
1. Backend stability fixes
2. Core dashboard shell
3. Add audit trails to Prisma schema
4. Add rate limiting with slowapi
5. Setup Turborepo
6. Setup GitHub Actions

## Task Status Tracking

- ✅ Completed
- ⏳ In Progress
- ⬜ Not Started
- ⏭️ Skipped (will retry after phase completion)
- ❌ Blocked (failed 6x, manual intervention required)

## Important Notes

- Always update todo_list when task status changes
- Log all failures with error messages
- Document reasons for blocked tasks
- Auto-run safe commands (no destructive operations)
- Stop only for true issues requiring user intervention
