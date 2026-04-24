# Content Generation Subagent Spec

Canonical contract for any Claude subagent (or orchestrator) that generates per-lead outreach content. Written after the Apr 2026 Lead Gen 3.0 incident in which 78% of records shipped partial and meta-fields leaked into Airtable PATCH payloads, rejecting entire batches.

**Read this whenever you're about to launch a content-gen subagent.** The prompt template at the bottom of this file is the one you should paste.

---

## Why this file exists

In Apr 2026, a content-gen run over 112 Lead Gen 3.0 records left 87 of them partial — most were missing emails 5-10, all WhatsApp, and late LinkedIn messages. Root causes:

1. **No field-level completeness gate.** The sanity check only verified three sentinel fields (`custom_email1`, `email5_body`, `email9_body`). A record with just those three filled passed the check while 30 others were empty.
2. **Subagent output contract was implicit.** Subagents emitted meta-fields like `_skip_reason` and `_note` alongside real content. Airtable rejected the whole 10-record batch with HTTP 422 on the first unknown field name.
3. **Subagents made unilateral skip decisions.** Each batch subagent independently decided to skip records flagged as DISQUALIFIED in source data. The orchestrator never asked them to — and inconsistency across batches meant some disqualified records got content, others didn't.
4. **No canonical prompt.** Every run reinvented the field-to-formula-to-sender mapping from scratch, producing subtle drift.

This spec fixes all four.

---

## The Contract

### Inputs (provided by orchestrator)

```json
{
  "record_id": "recXXXXXXXXXXXXXXX",
  "region": "AU | SG | PH | Other",
  "company_name": "string",
  "contact_name": "string",
  "missing": ["field_name_1", "field_name_2", ...],
  "present": { "existing_field": "existing_value", ... },
  "context": {
    "Industry": "...",
    "Countries": "...",
    "Currencies": "...",
    "Team Size": 123,
    "Revenue": "...",
    "Outreach Angle": "...",
    "Pain Points": "...",
    "Finance Setup": "...",
    "Cash Timing Risk": "...",
    "Key Signals": "...",
    "Priority": "HIGH | MEDIUM | NURTURE",
    "Lead Score": 73,
    "ICP Fit": 4
  }
}
```

### Output (strict)

```json
{
  "record_id": "recXXXXXXXXXXXXXXX",
  "company_name": "string",
  "contact_name": "string",
  "generated": {
    "<field_in_missing_array>": "content",
    ...
  }
}
```

### Contract rules (violating any fails the push)

1. **Fill every field in `missing`.** No exceptions. If the subagent cannot generate a meaningful field, it must still return the runbook template for that field — never omit the key, never leave the value empty.
2. **Never write to fields not in `missing`.** Fields in `present` are immutable.
3. **Never emit fields outside the 33-field template whitelist (below).** No `_skip_reason`, `_note`, `_risk_flag`, or any key starting with `_`. No `notes`, `reasoning`, `quality_score`. Only the whitelisted schema fields. Meta-data goes in the summary at the end of the run, not inside `generated`.
4. **Never refuse to generate for a record.** If a record looks disqualified, that's the orchestrator's call — generate content anyway. The orchestrator is responsible for pre-filtering before the subagent runs.

### The 33-field whitelist

```
custom_subject1
custom_email1, custom_email2, custom_email3, custom_email4
email5_subject, email5_body
email6_subject, email6_body
email7_subject, email7_body
email8_subject, email8_body
email9_subject, email9_body
email10_subject, email10_body
whatsapp_sdr_1, whatsapp_sdr_2
whatsapp_ae_1, whatsapp_ae_2
whatsapp_ceo_1, whatsapp_ceo_2, whatsapp_ceo_3
ae_linkedin_cr, sdr_linkedin_cr
sdr_linkedin_msg1, sdr_linkedin_msg2, sdr_linkedin_msg3
ae_linkedin_msg1, ae_linkedin_msg2, ae_linkedin_msg3
ceo_linkedin_msg1
```

Anything else in `generated` → Airtable PATCH fails → whole batch rolls back.

---

## Field → Formula → Sender Mapping

This is the canonical mapping. Follow it exactly. Every field has one formula, one sender, and (sometimes) one opt-out line.

| Field | Formula | Sender | Opt-out line |
|---|---|---|---|
| `custom_subject1` | Shared subject for emails 1-4 (2-4 words, lowercase, company-specific) | SDR | — |
| `custom_email1` | E1 Pain Hypothesis | SDR | No opt-out |
| `custom_email2` | E2 BAB (Before-After-Bridge) | SDR | No opt-out |
| `custom_email3` | E3 Referral / Right Person (social proof) | SDR | `Not relevant? Just say 'pass' - no hard feelings.` |
| `custom_email4` | E4 Open Door (zero pressure) | SDR | Whole email IS the opt-out |
| `email5_subject` + `email5_body` | E5 PAS (Problem-Agitate-Solve) | AE | `If I'm way off, reply 'pass' and I'll know.` |
| `email6_subject` + `email6_body` | E6 Pattern Share (discovery) | AE | `If this isn't your world, just say so.` |
| `email7_subject` + `email7_body` | E7 Relevant Question (2 free tips) | AE | Walkthrough ask is soft enough |
| `email8_subject` + `email8_body` | E8 Up to You (zero pressure close) | AE | Ends with "no hard feelings" |
| `email9_subject` + `email9_body` | E9 CEO Personal Reach-Out (< 80 words) | CEO | — |
| `email10_subject` + `email10_body` | E10 CEO Value Drop (E10 subject must start `Re:` + E9 subject) | CEO | `No pressure either way.` |
| `whatsapp_sdr_1` | SDR WA: awkwardness acknowledgment | SDR | — |
| `whatsapp_sdr_2` | SDR WA: "`{{sender_first_name}}` from Finmo, dropped you an email..." | SDR | — |
| `whatsapp_ae_1` | AE WA: "apologies for the cold WhatsApp" | AE | — |
| `whatsapp_ae_2` | AE WA: references SDR colleague + one insight | AE | — |
| `whatsapp_ceo_1` | CEO WA: "Hi [First Name], it's `{{sender_first_name}}` (CEO) from Finmo." | CEO | — |
| `whatsapp_ceo_2` | CEO WA: one-line compliment about the company | CEO | — |
| `whatsapp_ceo_3` | CEO WA: coffee/call ask (MUST include `(potentially)`) | CEO | — |
| `sdr_linkedin_cr` | SDR Connection Request (under 300 chars, SDR template) | SDR | — |
| `ae_linkedin_cr` | AE Connection Request (under 300 chars, AE template) | AE | — |
| `sdr_linkedin_msg1` | After CR accepted: content-guide offer | SDR | — |
| `sdr_linkedin_msg2` | Observation about their setup (no ask) | SDR | — |
| `sdr_linkedin_msg3` | One specific question about their process | SDR | — |
| `ae_linkedin_msg1` | Thanks for connecting + one hypothesis | AE | — |
| `ae_linkedin_msg2` | Market trend / data point (no question) | AE | — |
| `ae_linkedin_msg3` | Open-door close with opt-out ("If this isn't on your radar, totally fine") | AE | — |
| `ceo_linkedin_msg1` | CEO final LinkedIn message ("my team has been following...") | CEO | — |

### Sign-off format (per tier)

| Tier | Emails | Sign-off format |
|---|---|---|
| SDR | E1-E4 | `Cheers,<br>{{sender_first_name}} {{sender_last_name}}` (E1 may be unsigned) |
| AE | E5-E7 | `Best,<br>{{sender_first_name}} {{sender_last_name}}` |
| AE | E8 | No sign-off (ends with "No hard feelings.") |
| CEO | E9-E10 | `{{sender_first_name}}` (first name only) |

`{{sender_first_name}}` is **sign-off only**. Greetings use the recipient's first name (`Hi Robin,` not `Hi {{sender_first_name}},`).

---

## Pre-Generation Filter (Orchestrator's Job — Not the Subagent's)

Before you dispatch a record to a content-gen subagent, apply these filters. Records that don't pass stay out of the batch entirely — they do NOT go to the subagent with a "please skip" flag.

### Reject these records (do not generate content)

1. `Outreach Angle` starts with `DISQUALIFIED` (case-insensitive)
2. `Outreach Angle` starts with `Not recommended`
3. `Outreach Angle` equals `N/A` or is empty AND `Priority` is `NURTURE`
4. Contact Email domain is mismatched with Company Website (e.g., `@wellsfargo.com` on a BPO record)
5. Industry, Countries, AND Currencies are all empty → insufficient context to personalize

### Flag for re-enrichment (don't generate yet)

1. Exactly one of Industry / Countries / Currencies is empty → fix data first
2. Contact Title contains "Board Member", "Advisor", or "Assistant" → wrong decision-maker, re-enrich to find operational finance lead
3. Company appears twice in same table (dedup by normalized company name) → resolve duplicate first

### Generate (but calibrate tone)

1. `Priority = NURTURE` and `Lead Score < 40` → light-touch content only, no aggressive escalation framing
2. Company is a subsidiary of a much larger parent → frame around the local finance function, acknowledge the subsidiary reality
3. Revenue > 10x Finmo ICP → frame around regional/entity-level angle, not central treasury

**Never pass these filter decisions down to the subagent.** The subagent always generates. The orchestrator always filters.

---

## Writing Rules (non-negotiable)

Full rules in [UNIFIED_OUTREACH_SEQUENCE.md](UNIFIED_OUTREACH_SEQUENCE.md). Fail-the-push shortlist:

- **No em dashes.** Use hyphens. Em dashes (`—`) are a reliable AI tell.
- **No emojis.**
- **HTML:** `<br><br>` between paragraphs, never `<p>` tags.
- **Banned words:** leverage, comprehensive, robust, seamless, cutting-edge, innovative, synergy, streamline, optimize, utilize, facilitate, enhance, foster, delve, excited to, it's worth noting.
- **Banned openings:** "Still thinking about...", "Following up on...", "I've been talking to...", "One pattern that keeps coming up...", "Two patterns keep coming up...", "I keep seeing...", "I keep hearing from...", "Interesting trend:", "Quick follow-up on...".
- **Subject lines:** 2-5 words, lowercase, company-specific.
- **Length:** SDR emails 40-130 words. AE emails 80-165 words. CEO emails under 80 words.
- **LinkedIn CR:** under 300 characters, hard limit.
- **One question OR one CTA per message** — never both, never multiple.
- **`{{sender_first_name}}` is sign-off only** — never in greetings.
- **Product mention starts at E5.** Emails 1-4 are discovery. No "Finmo does X" in the SDR tier.
- **CEO WhatsApp must include `(potentially)`** in the ask — deliberate convention for David's voice.

---

## Canonical Subagent Prompt

Paste this verbatim when dispatching. Replace `{{batch_file}}` and `{{output_file}}` with actual paths.

````
You are generating personalized outreach content for Finmo's Lead Gen 3.0 prospects. This fills in missing template fields in an Airtable content pipeline.

# What you must do

1. Read these canonical references FIRST — source of truth, follow exactly:
   - runbooks/CONTENT_GENERATION_SUBAGENT.md (this file — contract, field mapping, writing rules)
   - runbooks/UNIFIED_OUTREACH_SEQUENCE.md (formula shuffle, templates, sign-offs)
   - runbooks/reference_examples.json (4 fully-completed records — study tone, length, structure)

2. Read your input batch: {{batch_file}}
   Each record has: record_id, region, company_name, contact_name, missing, present, context.

3. For EACH record, generate EVERY field in `missing`. No skipping. No meta-fields. Only fields from the 33-field whitelist.

4. Write output to: {{output_file}}
   Format:
   [
     {
       "record_id": "rec...",
       "company_name": "...",
       "contact_name": "...",
       "generated": {
         "<field>": "<content>",
         ...
       }
     },
     ...
   ]

# Contract (violations fail the push)

- Fill every field in `missing`. Never omit a key, never leave a value empty.
- Never write to `present` fields. They are immutable.
- Only emit fields in the 33-field whitelist. No `_skip_reason`, `_note`, or any other key starting with `_`.
- Never refuse a record. Pre-filtering is the orchestrator's job — you always generate.

# Writing rules (strict)

[Copy the Writing Rules section from CONTENT_GENERATION_SUBAGENT.md inline here.]

# Personalization must-haves

Every email body and LinkedIn body must contain at least one specific detail drawn from the `context` dict:
- Concrete numbers (team size, country count, currency count, revenue)
- Named currencies/countries (not "multi-currency" but "PHP, SGD, USD")
- Industry-specific framing
- Reference to Growth Signals or Key Signals when available
- Use Outreach Angle as the core thread through E1's hypothesis

# Output JSON only

Your final action is writing the JSON file. Do not print content to the console — only a one-line summary: records processed, total fields generated, any personalization risk flags worth surfacing to the orchestrator (not as fields, as a plain text note at the end of your response).
````

---

## Post-Generation Validation (Orchestrator's Job)

Before pushing to Airtable, validate the subagent output with these checks. All must pass.

1. Every record in the input batch has a corresponding entry in the output.
2. Every field in each record's `missing` array is present in `generated` and non-empty.
3. Every key in every `generated` dict is in the 33-field whitelist.
4. Zero em dashes (`—`) across any value.
5. Zero banned words (regex word-boundary match).
6. Zero banned openings (string-prefix match on body fields).
7. Every `email10_subject` starts with `Re:`.
8. Every sign-off matches its tier's expected format (SDR: Cheers, AE: Best, CEO: first name only).
9. Every LinkedIn CR is under 300 characters.
10. Every CEO email body is under 80 words.

If any check fails, fix the affected records (either by editing the JSON directly or by re-running the subagent for just those records) before pushing. The `lg3_sanity_check.py` script runs these same checks against Airtable after the push — it's a belt-and-braces.

---

## Lessons Baked Into This Spec

- A completeness gate that only samples sentinel fields will let partial records ship. The gate must enumerate every expected field.
- Subagents will invent schema extensions under pressure (meta-fields to explain their reasoning). The output contract must whitelist, not blacklist.
- "Should I skip this record?" is always the orchestrator's call. Giving subagents that authority produces inconsistent skip decisions across batches.
- Data hygiene issues (duplicates, empty context, email domain mismatches) must be caught before content-gen, not after. Content gen cost is wasted on records that should never have been in the queue.
