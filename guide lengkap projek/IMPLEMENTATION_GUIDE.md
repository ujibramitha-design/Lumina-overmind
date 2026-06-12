# Implementation Guide

## Implementation Order

Use this order for safe delivery:

1. Backend stability
2. Core dashboard shell
3. High-traffic operational pages
4. Detail pages
5. AI/orchestration modules
6. Creative and asset pipelines
7. Governance and audit improvements

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

