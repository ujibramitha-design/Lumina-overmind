# Data Model

## Core Domain Objects

### Lead
Represents a captured prospect or property-related contact.

Expected fields:
- id
- title or business name
- contact
- score
- status
- location
- source
- notes or follow-up state
- created_at
- updated_at

### Project
Represents a real-estate project or development target.

Expected fields:
- id
- nama_proyek
- tipe_proyek
- lokasi
- harga_start
- target_market
- is_active
- lead counters
- scoring metadata

### Partner
Represents broker or agency relationships.

Expected fields:
- id
- name
- tier
- total deals
- total revenue
- join date
- status

### Asset
Represents media or siteplan assets.

Expected fields:
- id
- project name
- file type
- file size
- status
- upload and processing timestamps
- file URL

### Config Key
Represents secure settings or credentials in the vault.

Expected fields:
- id
- key_name
- key_value
- description
- category
- is_active
- timestamps

## Relationship Notes

- Leads should be linkable to a project.
- Projects should be linkable to assets.
- Partner activity should map to leads and deals.
- Workflow execution should be traceable back to a project or lead context.
- Vault values should be isolated from normal business data.

## Data Contracts That Need Auditing

- lead detail
- project detail
- inbox draft data
- workflow runtime state
- ad proposal state
- asset upload state
- J.A.R.V.I.S. status and analytics

