# API Contracts

This document is a working contract summary, not a complete schema dump.

## Core API Families

### Auth
- login and token verification
- middleware cookie validation

### Leads
- list leads
- lead detail
- public submit
- inbox/approval integration

### Projects
- project list
- project detail
- active project selection

### Workflows
- workflow deploy
- workflow runtime or status endpoints

### Jarvis
- status
- analytics
- toggle
- chat/command routes

### Assets
- siteplan upload
- asset listing
- processing queue

### Governance / Security
- vault keys
- logs
- audit and policy controls

### Ads
- proposal listing
- approve/reject
- revision loop

## Contract Rules

- Frontend pages should not assume hidden fields.
- If a page needs a field, that field must be documented in the API response.
- If a route can fail during build, its data access path must be audited first.
- Any AI endpoint must define fallback behavior when the primary provider is unavailable.

## Important Known Gap

The current build failure around `/api/leads` indicates the data contract is not aligned with the database schema at runtime. That must be fixed before treating the dashboard build as production-stable.

