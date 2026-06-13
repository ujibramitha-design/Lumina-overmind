---
description: Project Rules and Guidelines for Lumina Overmind
---

# Project Rules and Guidelines

## Critical Rules

### 1. Documentation Update Rule

**CRITICAL**: Any addition or modification to analysis, checklists, frameworks, or any documentation must be immediately updated in the "guide lengkap projek" folder.

**This ensures:**
- All documentation remains synchronized
- The team always refers to the single source of truth
- No duplicate or contradictory information exists
- Changes are tracked and version-controlled

**Process:**
1. When adding new analysis or checklist → Update corresponding file in "guide lengkap projek"
2. When modifying existing analysis → Update the file in "guide lengkap projek"
3. When creating new framework → Add to "guide lengkap projek" and update README_WORKING_GUIDE.md
4. Always refer to "guide lengkap projek" as the primary source of truth

### 2. Progress Tracking Rule

**CRITICAL**: When working through checklists, roadmaps, or any action items:
- Always mark completed items as ✅ (completed)
- Never delete completed items - keep them for tracking history
- Mark incomplete items as ⬜ (not started) or ⏳ (in progress)

**This ensures:**
- Progress visibility at all times
- Historical tracking of what has been done
- Ability to resume work from where left off
- Audit trail of completed tasks

**Format:**
- ✅ Item completed
- ⏳ Item in progress
- ⬜ Item not started
- ❌ Item blocked/cannot be completed

## Working Rules

### Code and Development
- Do not redesign pages one by one without checking the module matrix first
- Do not treat visual polish as completion if the backend contract is still missing
- Keep the login/auth style as the canonical visual language for dashboard surfaces
- Stabilize route/data dependencies before expanding new screens

### Architecture and Structure
- Follow the folder structure defined in ARCHITECTURE.md
- Use the tech stack specified in the roadmap
- Prioritize backend stability before UI expansion
- Fix blockers before adding new visual complexity

## Reference Documents

Always refer to these documents in "guide lengkap projek" folder:
- README_WORKING_GUIDE.md - Primary entry point
- ARCHITECTURE.md - System architecture and tech stack
- ROADMAP.md - 6-phase implementation roadmap
- MODULE_MATRIX.md - Module status and prioritization
- IMPLEMENTATION_GUIDE.md - Implementation order and criteria
- DEPLOYMENT_CHECKLIST.md - Deployment preparation checklist
- RUNBOOK.md - Local development and recovery procedures
- KNOWN_ISSUES.md - Current blockers and issues

## 10-Dimension Health Framework

When making changes, consider impact on:
1. Structure & Organization
2. Code Quality
3. Documentation
4. Testing
5. Security
6. Performance
7. Scalability
8. Maintainability
9. User Experience
10. Deployment & DevOps

## Priority Order

1. Fix critical blockers (e.g., /api/leads schema mismatch)
2. Install critical tech stack gaps (Phase 1 of roadmap)
3. Stabilize backend infrastructure
4. Standardize UI shell across all pages
5. Complete feature depth for core modules
6. Add advanced features and integrations

## Error Handling

If encountering issues:
1. Check KNOWN_ISSUES.md for known blockers
2. Refer to RUNBOOK.md for recovery steps
3. Update documentation if new issues are discovered
4. Mark blocked items with ❌ in checklists
