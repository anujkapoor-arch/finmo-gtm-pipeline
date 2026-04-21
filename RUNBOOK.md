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
| AE Owner | singleSelect | AE assignment (Gibson Saw, Nouvelle Nye, Elross Pangue, Michelle Ling) |
| ae_linkedin_cr | multilineText | AE LinkedIn Connection Request (separate from SDR CR) |
| email5_subject - email10_body | singleLineText / multilineText | AE + CEO email content |
| whatsapp_sdr_1 - whatsapp_ceo_3 | multilineText | WhatsApp message content |

**Total: 21 new fields per table.**

**Manual step:** Remove `Lead Category` field from all 4 tables in Airtable UI (API doesn't support field deletion).

### Timezone

Every prospect MUST have a `Timezone` value. This drives SmartReach campaign send timing.

**Resolution priority:**
1. **Person Country** field (prospect's actual location, not company HQ)
2. **HQ Location** fallback (if Person Country is empty)
3. **First country** in Countries field (last resort)

**Why prospect location, not HQ:** A prospect at Embla Medical (HQ Iceland) who sits in Sydney should get emails at Sydney time, not Reykjavik time.

**Common timezone values:**
| Region | Timezone |
|--------|----------|
| Australia (East) | `Australia/Sydney` |
| Singapore | `Asia/Singapore` |
| Philippines | `Asia/Manila` |
| India | `Asia/Kolkata` |
| UK / Ireland | `Europe/London` |
| France / Germany / Switzerland | `Europe/Paris` / `Europe/Berlin` / `Europe/Zurich` |
| Sweden | `Europe/Stockholm` |
| US East | `America/New_York` |
| US Central | `America/Chicago` |
| US West | `America/Los_Angeles` |
| Canada (Vancouver) | `America/Vancouver` |

**Verify before campaign launch:** Run a check for empty Timezone fields. Zero gaps required.

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

**SDR Email:**
- `custom_subject1` - Email 1 subject line
- `custom_email1` through `custom_email4` - SDR email bodies

**SDR LinkedIn:**
- `sdr_linkedin_cr` - SDR connection request (non-salesy, curiosity-driven)
- `sdr_linkedin_msg1` - Post-acceptance content-offer guide
- `sdr_linkedin_msg2` - Observation about their setup (no ask)
- `sdr_linkedin_msg3` - Open question (genuine curiosity)

**AE Email:**
- `email5_subject` through `email8_body` - AE email subjects + bodies

**AE LinkedIn:**
- `ae_linkedin_cr` - AE connection request (industry peer)
- `ae_linkedin_msg1` - Post-acceptance industry insight
- `ae_linkedin_msg2` - Company-specific value observation
- `ae_linkedin_msg3` - Zero pressure close ("if this isn't on your radar, totally fine")

**CEO Email:**
- `email9_subject` through `email10_body` - CEO email subjects + bodies

**CEO LinkedIn:**
- `ceo_linkedin_msg1` - CEO final connection message

**Legacy fields (to delete in Airtable UI):**
- `custom_linkedin_cr`, `custom_linkedin1`, `custom_linkedin2`, `custom_linkedin3`, `custom_linkedin4`

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

**Basic Checklist:**
- [ ] Airtable: Scores populated? Content fields filled? SDR + AE Owner set?
- [ ] HubSpot: Contact created? marketing_notes has research? Owner assigned?
- [ ] SmartReach: Prospect created? Custom fields have content? Assigned to campaign?

---

## Phase 4b: Sanity Checks (Run After Every Push)

These checks catch issues discovered during pipeline operations. Run ALL of them before launching any campaign.

### 1. Zero Timezone Gaps
Every prospect must have a `Timezone` value. SmartReach uses this for send timing.
```
Query: Count records where Timezone is empty across all 4 tables.
Expected: 0 missing.
Fix: Resolve from Person Country > HQ Location > first Country.
```

### 2. HubSpot Contact URL Populated
After pushing to HubSpot, write the HubSpot Contact URL back to Airtable. SDRs use this link to access the contact record before calls.
```
Query: Count records where HubSpot Contact URL is empty but Contact Email exists.
Expected: 0 missing (for records with email).
Fix: Search HubSpot by email, build URL as https://app.hubspot.com/contacts/{PORTAL_ID}/contact/{HS_ID}.
```

### 3. HubSpot Contact + Company Owner = SDR
Both the HubSpot contact owner AND the associated company owner must match the SDR Owner from Airtable. This drives task assignment and reporting.
```
Query: Compare HubSpot hubspot_owner_id against Airtable SDR Owner mapping.
Expected: All match.
Fix: Batch update HubSpot contact owner, then fetch associated companies and update those too.
```

### 4. No Duplicate Records
Research and content pushes can create duplicates if company names differ slightly (e.g., "Simba Global Pty Ltd" vs "Simba Global").
```
Query: Group records by normalized Contact Name. Flag groups with 2+ records.
Expected: 0 duplicates.
Fix: Keep record with higher Lead Score, merge content fields from duplicate, delete duplicate.
Watch for: Name variants like "Timothy Bartholomew CA/CPA" vs "Timothy Bartholomew".
```

### 5. P1/P2 Content Completeness
Every P1 lead must have SDR (E1-E4) + AE (E5-E8) + CEO (E9-E10) content.
Every P2 lead must have SDR (E1-E4) + AE (E5-E8) content.
```
Query: For each HIGH priority record, check custom_email1, email5_body, email9_body are non-empty.
Expected: P1 (score 70+) has all three tiers. P2 (score 50-69) has SDR + AE.
Fix: Regenerate missing content via Claude agent.
```

### 6. No Hardcoded Sender Names
`{{sender_first_name}}` must be used for all sender references. Never hardcode "David", "Anuj", "Harini" etc.
```
Query: Search all text fields for "David from Finmo", "David here", "it's David", "Anuj from Finmo".
Expected: 0 matches.
Fix: Replace with {{sender_first_name}} or {{sender_first_name}} {{sender_last_name}}.
```

### 7. No {{sender_first_name}} in Greetings
Greetings must use the recipient's actual first name, never the sender variable.
```
Query: Search all email fields for "Hi {{sender_first_name}}".
Expected: 0 matches.
Fix: Replace with "Hi [Contact First Name]".
```

### 8. Correct Sign-Off Format
SDR emails end with "Cheers," + full name. AE emails end with "Best," + full name. CEO emails end with first name only.
```
Query: Check last line of custom_email2-4 contains "Cheers,<br>{{sender_first_name}} {{sender_last_name}}".
        Check last line of email5-8 contains "Best,<br>{{sender_first_name}} {{sender_last_name}}".
Expected: All match.
```

### 9. LinkedIn CR is Non-Salesy
The LinkedIn Connection Request must NOT contain guide offers, CTAs, or product mentions. The content-offer moves to LinkedIn Msg 1 (post-acceptance).
```
Query: Search custom_linkedin_cr for "put together", "guide", "Want me to send", "great to e-meet".
Expected: 0 matches (old salesy patterns).
Should contain: "came across", "caught my eye", "Would be great to connect".
```

### 10. AE LinkedIn CR Exists
Every record with AE content should also have `ae_linkedin_cr` populated.
```
Query: Count records where email5_body exists but ae_linkedin_cr is empty.
Expected: 0 missing.
```

### 11. Email Verification (Pre-Campaign)
Run all emails through Clearout before launching SmartReach campaigns.
```
Query: Clearout instant verify on all Contact Email values.
Expected: 0 invalid/hard-bounce. Flag catch-all domains for monitoring.
Watch for: Generic emails (info@, support@, hr@) - these should have been enriched or flagged.
```

### 12. Data Mismatches
Flag records where email domain doesn't match company (e.g., Wells Fargo email on a BPO company).
```
Query: Compare Contact Email domain against Company Name / Website.
Expected: All match or have documented reason for mismatch.
Fix: Delete or re-enrich mismatched records.
```

### 13. SDR + AE Owner Assigned
Every record with content must have both SDR Owner and AE Owner populated.
```
Query: Count records where custom_email1 exists but SDR Owner or AE Owner is empty.
Expected: 0 missing.
Valid SDR values: Harini, Sukriti.
Valid AE values: Gibson Saw, Nouvelle Nye, Elross Pangue, Michelle Ling.
```

### Quick Sanity Check Script
Run this after every push to catch all issues at once:
```bash
python3 scripts/pipeline/lg3_sanity_check.py --config config/config.json
```
*(Script checks all 13 rules above and reports pass/fail with counts.)*

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

### Duplicate Records After Push
If research and content were pushed in separate runs, company names may differ (e.g., "Simba Global Pty Ltd" vs "Simba Global") creating duplicates. Also watch for contact name variants ("Timothy Bartholomew CA/CPA" vs "Timothy Bartholomew"). After any push:
1. Check for duplicates: group records by normalized contact name
2. Keep the record with the higher Lead Score (the research record)
3. Merge content fields from the duplicate into the keeper
4. Delete the duplicate
The push scripts match by Contact Email first, then company name. If neither matches, a new record is created.

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
