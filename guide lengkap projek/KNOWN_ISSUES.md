# Known Issues

## Build and Runtime

### 1. `/api/leads` schema mismatch
- Build currently fails because the route tries to use a `leads` table that is not available in the current SQLite state.
- This is the highest-priority blocker.

### 2. AI provider dependency and env mismatch
- Gemini-related code previously expected `GEMINI_API_KEY`.
- There is also `GOOGLE_GEMINI_API_KEY` in user context.
- Provider selection and package installation must be verified together.

### 3. Legacy route and page fragmentation
- Some pages still have their own style or partial logic.
- Detail pages and asset subroutes need follow-up auditing.

### 4. Mixed documentation landscape
- The repo already contains many reports and guides.
- Without a single working guide, it is easy to duplicate or contradict instructions.

## Product Gaps

### 1. Workflow history and versioning
- Workflow builder exists, but runtime lifecycle is incomplete.

### 2. Creative and asset pipelines
- Create/revise/publish/version flows are not fully wired.

### 3. Partner lifecycle
- Commission calculator exists, but partner onboarding and payout ledger are incomplete.

### 4. Governance automation
- Logs exist, but policy, incident, and approval flows still need depth.

### 5. Detail pages
- `leads/[id]` and `projects/[id]` need a formal contract check.

## Operational Notes

- Treat page polish as incomplete until the backend contract is stable.
- Treat placeholder routes as planning targets, not production surfaces.
- Fix blockers before adding new visual complexity.

