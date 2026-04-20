# AI GTM Pipeline Runbook

Operational runbook for running the full outbound pipeline: research, score, generate content, push to Airtable/HubSpot/SmartReach, and activate automation.

---

## Architecture

```
                    ┌───────────────────────────────┐
                    │     LEAD INPUT (CSV/JSON)      │
                    │  Contact, Company, Industry    │
                    └──────────────┬────────────────┘
                                   │
                    ┌──────────────▼────────────────┐
                    │    PHASE 1: RESEARCH & SCORE   │
                    │  5 parallel agents per lead    │
                    │  (Company, Contacts, Opp,      │
                    │   Competitive, Strategy)        │
                    └──────────────┬────────────────┘
                                   │
                    ┌──────────────▼────────────────┐
                    │  PHASE 2: CONTENT GENERATION   │
                    │  10 emails + LinkedIn + WA     │
                    │  per UNIFIED_OUTREACH_SEQUENCE │
                    └──────────────┬────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                     ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │    AIRTABLE      │  │    HUBSPOT       │  │   SMARTREACH     │
    │  Source of truth │  │  Contact + notes │  │  Email sequences │
    │  Scores, content │  │  Research profile│  │  SDR campaigns   │
    │  Engagement data │  │  Owner assign    │  │  Content fields  │
    └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
             │                    │                     │
             └────────────────────┼─────────────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │     DAILY AUTOMATION         │
                    │  Task creation (4 PM)        │
                    │  Morning briefing (8 AM)     │
                    │  Midday check-in (12 PM)     │
                    │  Call sync (continuous)       │
                    │  SmartReach webhook (live)    │
                    └──────────────────────────────┘
```

---

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/YOUR_ORG/AI-GTM-agents.git
cd AI-GTM-agents
cp config/config.example.json config/config.json
# Edit config.json with your credentials and batch settings

# 2. One-time: Create new Airtable fields
python3 scripts/pipeline/lg3_create_airtable_fields.py --config config/config.json --dry-run
python3 scripts/pipeline/lg3_create_airtable_fields.py --config config/config.json

# 3. Push pipeline (per batch)
python3 scripts/pipeline/lg3_push_to_airtable.py --config config/config.json
python3 scripts/pipeline/lg3_push_to_hubspot.py --config config/config.json
python3 scripts/pipeline/lg3_push_to_smartreach.py --config config/config.json
```

---

## Dynamic Variables (Change Per Batch)

These values in `config/config.json` must be updated before each run:

| Variable | Path in config.json | Description | Example |
|----------|-------------------|-------------|---------|
| **Batch name** | `batch.name` | Identifier for this run | `"leadgen3_au"` |
| **Region** | `batch.region` | Target region: AU / SG / PH / Other | `"AU"` |
| **Leads file** | `input.leads_file` | Path to scored JSON with content | `"AU_LEADS_OUTREACH_v2.json"` |
| **Target table** | `airtable.target_table` | Which Airtable table to push to | `"AU"` (maps to table ID) |
| **SDR assignment** | `owners.sdr_assignment` | `"round-robin"` or manual mapping | `"round-robin"` |
| **AE assignment** | `owners.ae_assignment` | `"round-robin"` or manual mapping | `"round-robin"` |
| **Campaign IDs** | `smartreach.campaign_ids` | SmartReach campaign per SDR | `{"Harini": "CAMPAIGN_ID"}` |
| **Dry run** | `batch.dry_run` | Preview without pushing | `true` / `false` |

**Credentials (set once, rarely change):**
- `airtable.pat` - Airtable Personal Access Token
- `hubspot.token` - HubSpot Private App Token
- `smartreach.api_key` - SmartReach API Key
- `smartreach.team_id` - SmartReach Team ID
- `owners.hubspot_owner_ids` - HubSpot owner IDs per person

---

## Phase 0: Setup (One-Time)

### Create Airtable Fields

Run once per base to add new fields for AE content, WhatsApp, and AE Owner:

```bash
# Preview what will be created
python3 scripts/pipeline/lg3_create_airtable_fields.py --config config/config.json --dry-run

# Create fields in all 4 tables (AU, SG, PH, Other)
python3 scripts/pipeline/lg3_create_airtable_fields.py --config config/config.json
```

**19 new fields created per table:**

| Field | Type | Purpose |
|-------|------|---------|
| AE Owner | singleSelect | AE assignment (Michelle, Adlin, Nouvelle, Justin, Elross, Gibson, Yan Ling) |
| email5_subject - email10_body | singleLineText / multilineText | AE + CEO email content |
| whatsapp_sdr_1 - whatsapp_ceo_3 | multilineText | WhatsApp message content |

**Manual step:** Remove `Lead Category` field from all 4 tables in Airtable UI (API doesn't support field deletion).

---

## Phase 1: Research & Scoring

Use Claude Code to research leads. Input: raw leads from Airtable (Contact Name, Email, Title, Company, Industry, Team Size, HQ Location).

### Research Runbook

Follow `runbooks/UNIFIED_RESEARCH_RUNBOOK.md`:

1. **Quick Score (Phase 1):** Score on available data to classify P1/P2/P3/P4
2. **Deep Dive (Phase 2):** Web research for P1+P2 leads only
3. **Output:** Research profile per lead with scores, angles, pain points

### Scoring Dimensions

| Dimension | Weight | What to Score |
|-----------|--------|---------------|
| Company Fit | 25% | Cross-border ops, multi-currency, multi-entity, revenue, industry |
| Contact Access | 20% | Decision maker level, email quality, personalization anchors |
| Opportunity Quality | 20% | Pain signals, growth, trigger events, timing |
| Competitive Position | 15% | Current tools, switching cost, gaps |
| Outreach Readiness | 20% | Personalization depth, multiple angles, research quality |

### Classification

| Score | Priority | Action |
|-------|----------|--------|
| 70+ | P1 - HIGH | Full escalation: SDR + AE + Founder (10 emails) |
| 50-69 | P2 - MEDIUM | Standard: SDR + AE (8 emails) |
| 35-49 | P3 - NURTURE | Light-touch: SDR only (3 emails) |
| <35 | P4 - DISQUALIFY | No outreach. Close lead. |

---

## Phase 2: Content Generation

Follow `runbooks/UNIFIED_OUTREACH_SEQUENCE.md`:

### Content Per Priority

| Priority | Emails | LinkedIn | WhatsApp | Total Touches |
|----------|--------|----------|----------|---------------|
| P1 | 10 (E1-E10) | CR + 3 msgs | SDR(2) + AE(2) + CEO(3) | 18 |
| P2 | 8 (E1-E8) | CR + 2 msgs | SDR(2) + AE(2) | 14 |
| P3 | 3 (E1, E2, E4) | CR only | None | 4 |

### Sequence Structure

```
TIER 1: SDR (Days 1-13)           TIER 2: AE (Days 16-25)        TIER 3: CEO (Days 28-35)
  E1: Pain Hypothesis               E5: PAS (Category Creation)    E9: Personal Reach-Out
  E2: BAB (Aspiration)               E6: Pattern Share              E10: Value Drop
  E3: Referral/Social Proof          E7: Relevant Question
  E4: Open Door                      E8: Up to You
```

### Airtable Content Fields

**SDR (existing fields):**
- `custom_subject1` - Email 1 subject line
- `custom_email1` through `custom_email4` - SDR email bodies
- `custom_linkedin_cr` through `custom_linkedin4` - LinkedIn messages

**AE (new fields):**
- `email5_subject` through `email8_body` - AE email subjects + bodies

**CEO (new fields):**
- `email9_subject` through `email10_body` - CEO email subjects + bodies

**WhatsApp (new fields):**
- `whatsapp_sdr_1`, `whatsapp_sdr_2` - SDR WhatsApp
- `whatsapp_ae_1`, `whatsapp_ae_2` - AE WhatsApp
- `whatsapp_ceo_1`, `whatsapp_ceo_2`, `whatsapp_ceo_3` - CEO WhatsApp

---

## Phase 3: Push to Systems

### Step 1: Airtable (Source of Truth)

```bash
# Dry run first
python3 scripts/pipeline/lg3_push_to_airtable.py --config config/config.json --dry-run

# Push
python3 scripts/pipeline/lg3_push_to_airtable.py --config config/config.json
```

**What it does:**
- Loads scored leads + content from JSON
- Assigns SDR and AE owners (round-robin or manual)
- Maps priority (P1/P2 -> HIGH, P3 -> MEDIUM, P4 -> NURTURE)
- Creates new records or updates existing (matched by Contact Email)
- Pushes all research fields, scores, and content

### Step 2: HubSpot (CRM + Research Notes)

```bash
python3 scripts/pipeline/lg3_push_to_hubspot.py --config config/config.json --dry-run
python3 scripts/pipeline/lg3_push_to_hubspot.py --config config/config.json
```

**What it does:**
- Creates/updates HubSpot contacts
- Sets owner, timezone, MQL type
- Writes full research profile to `marketing_notes`:

```
[Research Summary]
Multi-country textile manufacturer with $50M investment...

[Company Profile]
Countries: AU, NZ, USA, Asia
Currencies: AUD, USD, NZD, CNY
Revenue: $20.2M

[Scoring]
Lead Score: 83/100 | ICP Fit: 5/5 | Priority: P1

[Pain Points]
Multi-currency supplier payments, FX exposure, M&A integration...

[Outreach Angle]
Four countries, four currencies, $48M financing...

[Finance Setup]
Traditional banking + spreadsheets...

[Key Signals]
$50M investment, active M&A, Group CFO title...
```

### Step 3: SmartReach (Email Sequences)

```bash
python3 scripts/pipeline/lg3_push_to_smartreach.py --config config/config.json --dry-run
python3 scripts/pipeline/lg3_push_to_smartreach.py --config config/config.json
```

**Prerequisite:** Campaign IDs must be set in `config.json`. Create campaigns in SmartReach first, then update:
```json
"campaign_ids": {
    "Harini": "YOUR_CAMPAIGN_ID",
    "Sukriti": "YOUR_CAMPAIGN_ID"
}
```

**What it does:**
- Creates prospects in SmartReach with SDR content in custom fields
- Assigns to correct campaign per SDR owner
- Handles rate limits and duplicates (409 = already exists)

---

## Phase 4: Verification

After pushing, verify 5 random records across all three systems:

```bash
# Check Airtable
curl -s "https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}?maxRecords=5" \
  -H "Authorization: Bearer {PAT}" | python3 -m json.tool

# Check HubSpot
curl -s "https://api.hubapi.com/crm/v3/objects/contacts/search" \
  -H "Authorization: Bearer {TOKEN}" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"email","operator":"EQ","value":"test@example.com"}]}]}' | python3 -m json.tool
```

**Checklist:**
- [ ] Airtable: Scores populated? Content fields filled? SDR + AE Owner set?
- [ ] HubSpot: Contact created? marketing_notes has research? Owner assigned?
- [ ] SmartReach: Prospect created? Custom fields have content? Assigned to campaign?

---

## Phase 5: Automation (Runs Automatically)

Once leads are in all three systems, the daily automation handles everything:

### SmartReach Webhook (Real-Time)

Runs in Zapier. Syncs engagement events to Airtable:
- Email sent -> `Last Contacted At`, `Current Step`
- Email opened -> `Last Opened At`, `Email Opens` +1
- Email replied -> `Last Replied At`, `Reply Sentiment`
- Category updated -> `Prospect Category`

### Daily Task Creation (4 PM IST)

```bash
gh workflow run task-notifications.yml -R YOUR_ORG/YOUR_REPO -f mode=evening
```

- Fetches all leads from Airtable tables
- Scores by intent (opens, replies, calls, status)
- Creates HubSpot tasks for next business day
- Channel assignment: top 20% WhatsApp, middle 60% call, bottom 20% LinkedIn
- 50 tasks per SDR per day, 3-day cooldown rotation

### Slack Notifications

| Time | Mode | What |
|------|------|------|
| 8:00 AM IST | Morning | Task breakdown per SDR, top 5 leads |
| 12:00 PM IST | Midday | AU completion checkpoint |
| 4:00 PM IST | Evening | End-of-day report + tomorrow's task creation |

```bash
gh workflow run task-notifications.yml -R YOUR_ORG/YOUR_REPO -f mode=morning
gh workflow run task-notifications.yml -R YOUR_ORG/YOUR_REPO -f mode=midday
gh workflow run task-notifications.yml -R YOUR_ORG/YOUR_REPO -f mode=evening
```

### Call Sync

```bash
gh workflow run sync-calls.yml -R YOUR_ORG/YOUR_REPO
```

Syncs HubSpot call data to Airtable: Number of Calls, Call Status, Last Call Made.

---

## Adding New Regions

To activate PH Leads or Other Regions in the automation:

1. Add table IDs to `hubspot_daily_tasks.py` and `hubspot_task_checker.py`:
   ```python
   TABLES = {
       "AU": "YOUR_AU_TABLE_ID",
       "SG": "YOUR_SG_TABLE_ID",
       "PH": "YOUR_PH_TABLE_ID",       # Add this
       "Other": "YOUR_OTHER_TABLE_ID",  # Add this
   }
   ```

2. Add timezone logic for task due times:
   - PH: 2:00 PM IST (same as SG)
   - Other: varies by lead timezone

3. Add table IDs to SmartReach webhook handler search loop

4. Run the pipeline with `batch.region = "PH"` in config

---

## Adding New SDRs or AEs

### New SDR
1. Add to `config.json` -> `owners.sdrs` array
2. Add HubSpot owner ID to `owners.hubspot_owner_ids`
3. Add Slack ID to `hubspot_task_checker.py` -> `SLACK_IDS`
4. Create SmartReach campaign, add ID to `smartreach.campaign_ids`

### New AE
1. Add to `config.json` -> `owners.aes` array
2. Add to Airtable `AE Owner` singleSelect choices (via field creation script or UI)
3. Add HubSpot owner ID to `owners.hubspot_owner_ids`

---

## Team

| Role | People | System |
|------|--------|--------|
| SDRs | Harini, Sukriti | SmartReach campaigns, HubSpot tasks |
| AEs | Michelle, Adlin, Nouvelle, Justin, Elross, Gibson, Yan Ling | HubSpot, Airtable AE Owner |
| CEO | David | Tier 3 founder emails |

---

## Credentials Reference

| Service | Key Type | Where Stored |
|---------|----------|-------------|
| Airtable | Personal Access Token | `config.json` + GitHub secret |
| HubSpot | Private App Token | `config.json` + GitHub secret |
| SmartReach | X-API-KEY | `config.json` + GitHub secret |
| GitHub (Zapier) | PAT | Zapier webhook headers |

---

## Troubleshooting

### Airtable 422 "Invalid value for column"
- Check field type matches value (e.g., Priority must be HIGH/MEDIUM/NURTURE, not P1/P2)
- Check singleSelect fields have the choice defined
- Number fields can't accept strings

### HubSpot 429 Rate Limit
All scripts use exponential backoff (2s, 3s, 5s, 9s). If persistent, increase `time.sleep()` between calls.

### SmartReach 409 Already Exists
Expected for re-runs. Use `update_existing=true` endpoint to update content on existing prospects.

### SmartReach API Gotchas
- Must use v3 API (v4 returns 404)
- Prospect create: `json=[prospect]` (array, not object)
- Custom fields must be nested: `{"custom_fields": {"field": "value"}}`
- Tags: alphanumeric + hyphens only (no underscores)

### Content Not Showing in SmartReach
- Verify custom fields exist in SmartReach campaign template
- Field names must match exactly: `custom_subject1`, `custom_email1`, etc.
- Check prospect was assigned to the campaign (not just created)

---

## File Reference

| File | Purpose |
|------|---------|
| `config/config.example.json` | Template - copy to config.json |
| `config/field_mappings.json` | Airtable/HubSpot/SmartReach field definitions |
| `runbooks/UNIFIED_RESEARCH_RUNBOOK.md` | How to research and score leads |
| `runbooks/UNIFIED_OUTREACH_SEQUENCE.md` | How to generate outreach content |
| `scripts/pipeline/lg3_create_airtable_fields.py` | One-time field creation |
| `scripts/pipeline/lg3_push_to_airtable.py` | Push to Airtable |
| `scripts/pipeline/lg3_push_to_hubspot.py` | Push to HubSpot |
| `scripts/pipeline/lg3_push_to_smartreach.py` | Push to SmartReach |
