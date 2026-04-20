#!/usr/bin/env python3
"""
Push prospects + content to SmartReach campaigns.

Usage:
  python3 lg3_push_to_smartreach.py --config config/config.json
  python3 lg3_push_to_smartreach.py --config config/config.json --dry-run
"""
import json
import argparse
import requests
import time
from itertools import cycle

def load_config(path):
    with open(path) as f:
        return json.load(f)

def split_name(full_name):
    clean = full_name.split(",")[0].strip()
    parts = clean.strip().split(" ", 1)
    first = parts[0] if parts else ""
    last = parts[1] if len(parts) > 1 else ""
    return first, last

SR_CONTENT_FIELDS = [
    "custom_subject1", "custom_email1", "custom_email2", "custom_email3", "custom_email4",
    "custom_linkedin_cr", "custom_linkedin1", "custom_linkedin2", "custom_linkedin3", "custom_linkedin4",
]

def build_prospect(lead):
    contact_name = lead.get("contact_name", "") or lead.get("Contact Name", "")
    first, last = split_name(contact_name)
    hq = lead.get("hq_location", "") or lead.get("HQ Location", "")

    prospect = {
        "email": (lead.get("contact_email", "") or lead.get("Contact Email", "")).strip(),
        "first_name": first,
        "last_name": last,
        "company": lead.get("company_name", "") or lead.get("Company Name", ""),
        "designation": lead.get("contact_title", "") or lead.get("Contact Title", ""),
        "city": hq.split(",")[0].strip() if hq else "",
        "linkedin_url": lead.get("contact_linkedin", "") or lead.get("Contact LinkedIn", ""),
    }

    # Custom fields for content
    custom_fields = {}
    for f in SR_CONTENT_FIELDS:
        val = lead.get(f, "")
        if val:
            custom_fields[f] = val
    if custom_fields:
        prospect["custom_fields"] = custom_fields

    return prospect

def sr_request(method, url, headers, json_data=None, retries=3):
    for attempt in range(retries):
        if method == "POST":
            resp = requests.post(url, headers=headers, json=json_data)
        elif method == "PUT":
            resp = requests.put(url, headers=headers, json=json_data)
        else:
            resp = requests.get(url, headers=headers)
        if resp.status_code == 429:
            wait = 30 * (attempt + 1)
            print(f"    Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue
        return resp
    return resp

def main():
    parser = argparse.ArgumentParser(description="Push prospects to SmartReach")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview without pushing")
    args = parser.parse_args()

    config = load_config(args.config)
    sr_config = config["smartreach"]

    headers = {
        "X-API-KEY": sr_config["api_key"],
        "Content-Type": "application/json"
    }
    team_id = sr_config["team_id"]
    campaign_ids = sr_config["campaign_ids"]

    # Validate campaign IDs
    for sdr, cid in campaign_ids.items():
        if not cid:
            print(f"ERROR: No campaign ID for {sdr}. Update config.json smartreach.campaign_ids first.")
            return

    with open(config["input"]["leads_file"]) as f:
        leads = json.load(f)

    # Assign SDRs if not set
    sdrs = cycle(config["owners"]["sdrs"])
    for lead in leads:
        if not lead.get("sdr") and not lead.get("SDR Owner"):
            lead["sdr"] = next(sdrs)

    print("=" * 60)
    print(f"SMARTREACH PUSH - {config['batch']['name']}")
    print("=" * 60)
    print(f"Leads: {len(leads)} | Dry run: {args.dry_run}")
    print(f"Campaigns: {campaign_ids}")

    # Split by SDR
    sdr_leads = {}
    for lead in leads:
        sdr = lead.get("sdr", "") or lead.get("SDR Owner", "")
        if sdr not in sdr_leads:
            sdr_leads[sdr] = []
        sdr_leads[sdr].append(lead)

    for sdr, sdr_list in sdr_leads.items():
        print(f"  {sdr}: {len(sdr_list)} leads -> Campaign {campaign_ids.get(sdr, 'MISSING')}")

    if args.dry_run:
        print("\n[DRY RUN] Preview:")
        for sdr, sdr_list in sdr_leads.items():
            for lead in sdr_list[:2]:
                p = build_prospect(lead)
                print(f"  {p['first_name']} {p['last_name']} ({p['email']}) -> {sdr}")
                print(f"    Custom fields: {len(p.get('custom_fields', {}))}")
        print("\n[DRY RUN] No prospects pushed.")
        return

    # Push per SDR
    for sdr, sdr_list in sdr_leads.items():
        cid = campaign_ids.get(sdr)
        if not cid:
            print(f"\n  SKIP {sdr}: No campaign ID")
            continue

        print(f"\n{'=' * 40}")
        print(f"[{sdr}] Campaign {cid}: {len(sdr_list)} leads")
        print(f"{'=' * 40}")

        created_ids = []
        errors = []

        for i, lead in enumerate(sdr_list):
            prospect = build_prospect(lead)
            if not prospect["email"]:
                continue

            url = f"https://api.smartreach.io/api/v3/prospects?team_id={team_id}"
            resp = sr_request("POST", url, headers, [prospect])

            if resp.status_code in (200, 201):
                data = resp.json()
                pid = None
                if isinstance(data, dict):
                    pid = data.get("data", {}).get("id") or data.get("id")
                elif isinstance(data, list) and data:
                    pid = data[0].get("id")
                created_ids.append(pid)
            elif resp.status_code == 409:
                print(f"  EXISTS: {prospect['first_name']} {prospect['last_name']}")
            else:
                err = str(resp.text)[:150]
                print(f"  ERROR {resp.status_code}: {prospect['email']} - {err}")
                errors.append(prospect["email"])

            time.sleep(0.3)
            if (i + 1) % 10 == 0:
                print(f"  [{i+1}/{len(sdr_list)}] Created: {len(created_ids)}")

        # Assign to campaign
        valid_ids = [pid for pid in created_ids if pid]
        if valid_ids:
            print(f"\n  Assigning {len(valid_ids)} to campaign {cid}...")
            for j in range(0, len(valid_ids), 50):
                batch = valid_ids[j:j+50]
                url = f"https://api.smartreach.io/api/v3/campaigns/{cid}/prospects?team_id={team_id}"
                resp = sr_request("POST", url, headers, {"prospect_ids": batch})
                if resp.status_code == 200:
                    print(f"    Assigned batch: {len(batch)}")
                else:
                    print(f"    ASSIGN ERROR: {resp.status_code}")
                time.sleep(0.5)

        print(f"\n  [{sdr}] Created: {len(created_ids)}, Errors: {len(errors)}")

    print(f"\n{'=' * 60}")
    print("DONE")

if __name__ == "__main__":
    main()
