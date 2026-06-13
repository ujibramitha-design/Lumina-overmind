# Add File - Documentation Archive

This folder contains archived documentation files organized by category.

## Folder Structure

### **docs/**
Main documentation folder with categorized subfolders:

#### **database/** (9 files)
Database schema, queries, monitoring, and security documentation
- Schema documentation (caching_sha2_password.md)
- Data operations (data-batch-inserts.md, data-n-plus-one.md, data-pagination.md, data-upsert.md)
- Monitoring (monitor-explain-analyze.md, monitor-pg-stat-statements.md, monitor-vacuum-analyze.md)
- Query optimization (query-composite-indexes.md, query-covering-indexes.md, query-index-types.md, query-missing-indexes.md, query-partial-indexes.md)
- Security (security-privileges.md, security-rls-basics.md, security-rls-performance.md)

#### **frontend/** (4 files)
Frontend components and UI documentation
- 3D graphics (BezierMesh.md)
- React examples (bindExample.md, connectExample.md, createDerivedMaterial.md)

#### **guides/** (8 files)
General documentation and guides
- Contributing guides (CONTRIBUTING.md)
- Commercial package documentation (COMMERCIAL_PACKAGE_README.md)
- Common issues (Common-issues.md)
- README files (README-DEVSECOPS.md, README-es.md, README_FASE3_CLOSER.md)
- Legal compliance (legal_compliance.md)
- Development guides (fp.md, lang.md, prompt_instructions.md, quotes.md)

#### **integration/** (2 files)
Third-party integrations
- Webhook integration (archidep_webhook_integration.md)
- CDN configuration (cdn.md)
- Streaming (streaming.md)

#### **migration/** (62 files)
Files marked for tech stack migration
- All files with [MIGRATION_NEEDED] prefix (API, authentication, backend, database, frontend, integration, reports)
- Migration reference files (FILES_TO_DELETE.txt, FILES_TO_KEEP_CRITICAL.txt)
- TypeScript/ESLint rule documentation

#### **typescript/** (4 files)
TypeScript and ESLint configuration
- TypeScript rules (ban-ts-comment.md, ban-tslint-comment.md, ban-types.md)
- Accessibility guidelines (click-events-have-key-events.md)

## Migration Notes

Files marked with `[MIGRATION_NEEDED]` prefix require updates during the tech stack migration phases:
- Phase 1: Critical dependencies (Week 1-2)
- Phase 2: Infrastructure (Week 3-4)
- Phase 3: Framework upgrades (Week 5-8)
- Phase 4: Advanced features (Week 9-12)

See `guide lengkap projek/` for detailed migration plans.
