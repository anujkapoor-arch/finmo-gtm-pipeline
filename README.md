# Finmo GTM Pipeline

AI-powered Go-To-Market pipeline for outbound sales. Research prospects, score leads, generate personalized outreach sequences, and push to Airtable/HubSpot/SmartReach.

## What This Does

```
Raw Leads (CSV/JSON)
    |
    v
Phase 1: Research & Score (5 parallel AI agents per lead)
    |
    v
Phase 2: Content Generation (10 emails + LinkedIn + WhatsApp per lead)
    |
    v
Phase 3: Push to Systems (Airtable -> HubSpot -> SmartReach)
    |
    v
Phase 4: Daily Automation (task creation, notifications, engagement sync)
```

## Quick Start

```bash
# Clone
git clone https://github.com/anujkapoor-arch/finmo-gtm-pipeline.git
cd finmo-gtm-pipeline

# Configure
cp config/config.example.json config/config.json
# Edit config.json with your credentials

# One-time: Create Airtable fields
python3 scripts/pipeline/lg3_create_airtable_fields.py --config config/config.json --dry-run
python3 scripts/pipeline/lg3_create_airtable_fields.py --config config/config.json

# Push pipeline (per batch)
python3 scripts/pipeline/lg3_push_to_airtable.py --config config/config.json --dry-run
python3 scripts/pipeline/lg3_push_to_airtable.py --config config/config.json
python3 scripts/pipeline/lg3_push_to_hubspot.py --config config/config.json
python3 scripts/pipeline/lg3_push_to_smartreach.py --config config/config.json
```

See [RUNBOOK.md](RUNBOOK.md) for full operational documentation.

## Repo Structure

```
finmo-gtm-pipeline/
|-- RUNBOOK.md                              <- Master operational runbook
|-- config/
|   |-- config.example.json                 <- Template (copy to config.json)
|   |-- field_mappings.json                 <- Airtable/HubSpot/SmartReach field maps
|-- runbooks/
|   |-- UNIFIED_RESEARCH_RUNBOOK.md         <- Research & scoring methodology
|   |-- UNIFIED_OUTREACH_SEQUENCE.md        <- Content generation rules
|-- scripts/pipeline/
|   |-- lg3_create_airtable_fields.py       <- One-time: create new Airtable fields
|   |-- lg3_push_to_airtable.py             <- Push scored leads + content
|   |-- lg3_push_to_hubspot.py              <- Push contacts + research notes
|   |-- lg3_push_to_smartreach.py           <- Push prospects to campaigns
```

## Dynamic Variables (Change Per Batch)

| Variable | Description |
|----------|-------------|
| `batch.name` | Identifier for this run |
| `batch.region` | AU / SG / PH / Other |
| `input.leads_file` | Path to scored JSON |
| `smartreach.campaign_ids` | Campaign ID per SDR |
| `batch.dry_run` | Preview without pushing |

## Systems

| System | Purpose |
|--------|---------|
| **Airtable** | Source of truth - scores, content, engagement |
| **HubSpot** | CRM - contacts, research notes, tasks |
| **SmartReach** | Email sequences - SDR campaigns |
| **Slack** | Daily notifications (via Zapier) |

## Requirements

- Python 3.8+
- `requests` library (`pip install requests`)
- Airtable, HubSpot, SmartReach API credentials
