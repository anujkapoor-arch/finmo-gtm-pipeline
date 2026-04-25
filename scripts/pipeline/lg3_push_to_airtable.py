#!/usr/bin/env python3
"""
Push scored research + outreach content to Airtable Lead Gen 3.0.
Creates new records or updates existing ones (matched by Contact Email).

Usage:
  python3 lg3_push_to_airtable.py --config config/config.json
  python3 lg3_push_to_airtable.py --config config/config.json --dry-run
"""
import json
import argparse
import re
import requests
import time
from datetime import date
from itertools import cycle

def load_config(path):
    with open(path) as f:
        return json.load(f)

def api_call(method, url, headers, payload=None, retries=3):
    for attempt in range(retries):
        if method == "POST":
            resp = requests.post(url, headers=headers, json=payload)
        elif method == "PATCH":
            resp = requests.patch(url, headers=headers, json=payload)
        elif method == "GET":
            resp = requests.get(url, headers=headers, params=payload)
        else:
            raise ValueError(f"Unknown method: {method}")
        if resp.status_code == 429:
            wait = 30 * (attempt + 1)
            print(f"    Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue
        elif resp.status_code >= 500:
            time.sleep(5)
            continue
        return resp
    return resp

def get_existing_emails(base_id, table_id, headers):
    email_to_record = {}
    offset = None
    while True:
        url = f"https://api.airtable.com/v0/{base_id}/{table_id}?fields%5B%5D=Contact+Email&pageSize=100"
        if offset:
            url += f"&offset={offset}"
        resp = api_call("GET", url, headers)
        data = resp.json()
        for r in data.get("records", []):
            email = r.get("fields", {}).get("Contact Email", "").strip().lower()
            if email:
                email_to_record[email] = r["id"]
        offset = data.get("offset")
        if not offset:
            break
    return email_to_record

_COMPANY_SUFFIX_RE = re.compile(
    r'(?i)\b(pty|ltd|limited|inc|incorporated|llc|plc|group|holdings|corp|corporation|gmbh|bv|sa|ag|nv)\b'
)

def normalize_company_name(name):
    """Lowercase and strip legal suffixes / punctuation. Used to dedupe
    'Acme Inc' vs 'Acme Inc.' vs 'Acme Group' as the same firm for AE assignment."""
    if not name:
        return ""
    n = _COMPANY_SUFFIX_RE.sub('', name)
    return re.sub(r'[^a-z0-9]+', ' ', n.lower()).strip()


def assign_owners(leads, config):
    """Assign SDR and AE owners.

    AE is grouped by normalized company name: all contacts at the same firm
    must land with the same AE. Otherwise two AEs end up engaging one company
    independently. Pre-assigned AEs are preserved and propagated to siblings.

    SDR remains per-lead round-robin (different SDR cadences are intentional).
    """
    sdrs = cycle(config["owners"]["sdrs"])
    aes = cycle(config["owners"]["aes"])

    # Pass 1: collect any pre-assigned AE per normalized company so we
    # propagate that choice to other contacts at the same firm.
    company_to_ae = {}
    for lead in leads:
        co = normalize_company_name(lead.get("company_name") or lead.get("Company Name"))
        ae = lead.get("ae") or lead.get("AE Owner")
        if co and ae and co not in company_to_ae:
            company_to_ae[co] = ae

    # Pass 2: assign SDRs (per-lead) and AEs (per-company).
    for lead in leads:
        if not lead.get("sdr"):
            lead["sdr"] = next(sdrs)
        if not lead.get("ae"):
            co = normalize_company_name(lead.get("company_name") or lead.get("Company Name"))
            if co and co in company_to_ae:
                lead["ae"] = company_to_ae[co]
            else:
                lead["ae"] = next(aes)
                if co:
                    company_to_ae[co] = lead["ae"]
    return leads

PRIORITY_MAP = {"P1": "HIGH", "P2": "HIGH", "P3": "MEDIUM", "P4": "NURTURE"}

# All content fields that map directly from JSON to Airtable
CONTENT_FIELDS = [
    "custom_subject1", "custom_email1", "custom_email2", "custom_email3", "custom_email4",
    "custom_linkedin_cr", "custom_linkedin1", "custom_linkedin2", "custom_linkedin3", "custom_linkedin4",
    "email5_subject", "email5_body", "email6_subject", "email6_body",
    "email7_subject", "email7_body", "email8_subject", "email8_body",
    "email9_subject", "email9_body", "email10_subject", "email10_body",
    "whatsapp_sdr_1", "whatsapp_sdr_2", "whatsapp_ae_1", "whatsapp_ae_2",
    "whatsapp_ceo_1", "whatsapp_ceo_2", "whatsapp_ceo_3",
]

def build_record(lead, config):
    region = config["batch"]["region"]
    tz = config["timezones"].get(region, "UTC")
    today = date.today().isoformat()

    # Map priority from P1/P2/P3/P4 to HIGH/MEDIUM/NURTURE
    raw_priority = lead.get("priority", "") or ""
    priority = PRIORITY_MAP.get(raw_priority, raw_priority)

    fields = {
        "Company Name": lead.get("company_name", "") or lead.get("Company Name", ""),
        "Website": lead.get("website", "") or lead.get("Website", ""),
        "Industry": lead.get("industry", "") or lead.get("Industry", ""),
        "Team Size": str(lead.get("team_size", "") or lead.get("Team Size", "")),
        "HQ Location": lead.get("hq_location", "") or lead.get("HQ Location", ""),
        "Countries": lead.get("countries", "") or lead.get("Countries", ""),
        "Currencies": lead.get("currencies", "") or lead.get("Currencies", ""),
        "Business Model": lead.get("business_model", "") or lead.get("Business Model", ""),
        "Revenue": lead.get("revenue", "") or lead.get("Revenue", ""),
        "Growth Signals": lead.get("growth_signals", "") or lead.get("Growth Signals", ""),
        "Contact Name": lead.get("contact_name", "") or lead.get("Contact Name", ""),
        "Contact Title": lead.get("contact_title", "") or lead.get("Contact Title", ""),
        "Contact Email": lead.get("contact_email", "") or lead.get("Contact Email", ""),
        "Lead Score": lead.get("lead_score", 0) or lead.get("Lead Score", 0),
        "ICP Fit": lead.get("icp_fit", 0) or lead.get("ICP Fit", 0),
        "Timing Score": lead.get("timing_score", 0) or lead.get("Timing Score", 0),
        "Cash Risk Score": lead.get("cash_risk_score", 0) or lead.get("Cash Risk Score", 0),
        "Priority": priority if priority in ("HIGH", "MEDIUM", "NURTURE") else "",
        "SDR Owner": lead.get("sdr", "") or lead.get("SDR Owner", ""),
        "AE Owner": lead.get("ae", "") or lead.get("AE Owner", ""),
        "Outreach Angle": lead.get("outreach_angle", "") or lead.get("Outreach Angle", ""),
        "Pain Points": lead.get("pain_points", "") or lead.get("Pain Points", ""),
        "Finance Setup": lead.get("finance_setup", "") or lead.get("Finance Setup", ""),
        "Cash Timing Risk": lead.get("cash_timing_risk", "") or lead.get("Cash Timing Risk", ""),
        "Key Signals": lead.get("key_signals", "") or lead.get("Key Signals", ""),
        "Timezone": tz,
        "Date Added": today,
        "Pushed to Smartreach": False,
    }

    # Content fields
    for f in CONTENT_FIELDS:
        val = lead.get(f, "")
        if val:
            fields[f] = val

    # Clean empty string values for select fields
    for sel_field in ["Priority", "SDR Owner", "AE Owner"]:
        if not fields.get(sel_field):
            del fields[sel_field]

    return fields

def main():
    parser = argparse.ArgumentParser(description="Push leads to Airtable Lead Gen 3.0")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview without pushing")
    args = parser.parse_args()

    config = load_config(args.config)
    base_id = config["airtable"]["base_id"]
    region = config["batch"]["region"]
    table_id = config["airtable"]["table_ids"][region]
    headers = {
        "Authorization": f"Bearer {config['airtable']['pat']}",
        "Content-Type": "application/json"
    }

    # Load leads
    with open(config["input"]["leads_file"]) as f:
        leads = json.load(f)

    # Assign owners
    leads = assign_owners(leads, config)

    print("=" * 60)
    print(f"AIRTABLE PUSH - {config['batch']['name']}")
    print("=" * 60)
    print(f"Region: {region} | Table: {table_id}")
    print(f"Leads: {len(leads)} | Dry run: {args.dry_run}")

    # Get existing records
    print("\n[1] Checking existing records...")
    existing = get_existing_emails(base_id, table_id, headers)
    print(f"  Existing records: {len(existing)}")

    # Build records
    print(f"\n[2] Building {len(leads)} records...")
    new_records = []
    update_records = []

    for lead in leads:
        fields = build_record(lead, config)
        email = (lead.get("contact_email", "") or lead.get("Contact Email", "")).strip().lower()
        if email in existing:
            update_records.append((existing[email], fields))
        else:
            new_records.append(fields)

    print(f"  New: {len(new_records)} | Updates: {len(update_records)}")

    if args.dry_run:
        print("\n[DRY RUN] Preview of first 3 records:")
        for i, rec in enumerate((new_records + [f for _, f in update_records])[:3]):
            print(f"\n  Record {i+1}: {rec.get('Company Name')} / {rec.get('Contact Name')}")
            for k, v in rec.items():
                if v and k not in CONTENT_FIELDS:
                    print(f"    {k}: {str(v)[:80]}")
            content_count = len([k for k in CONTENT_FIELDS if rec.get(k)])
            print(f"    [+ {content_count} content fields]")
        print("\n[DRY RUN] No records pushed.")
        return

    # Push new records
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
    created = 0
    if new_records:
        print(f"\n[3] Creating {len(new_records)} new records...")
        for i in range(0, len(new_records), 10):
            batch = [{"fields": r} for r in new_records[i:i+10]]
            resp = api_call("POST", url, headers, {"records": batch})
            if resp.status_code == 200:
                created += len(batch)
            else:
                print(f"    ERROR: {resp.status_code} {resp.text[:200]}")
            time.sleep(0.3)

    # Update existing
    updated = 0
    if update_records:
        print(f"\n[4] Updating {len(update_records)} existing records...")
        for i in range(0, len(update_records), 10):
            batch = [{"id": rid, "fields": fields} for rid, fields in update_records[i:i+10]]
            resp = api_call("PATCH", url, headers, {"records": batch})
            if resp.status_code == 200:
                updated += len(batch)
            else:
                print(f"    ERROR: {resp.status_code} {resp.text[:200]}")
            time.sleep(0.3)

    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"Created: {created} | Updated: {updated}")
    print(f"Total: {created + updated}/{len(leads)}")

if __name__ == "__main__":
    main()
