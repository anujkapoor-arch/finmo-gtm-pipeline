#!/usr/bin/env python3
"""
Push leads to HubSpot contacts with research notes in marketing_notes.

Usage:
  python3 lg3_push_to_hubspot.py --config config/config.json
  python3 lg3_push_to_hubspot.py --config config/config.json --dry-run
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

def parse_location(hq_location):
    if not hq_location:
        return "", ""
    parts = [p.strip() for p in hq_location.split(",")]
    city = parts[0] if parts else ""
    state = parts[1] if len(parts) > 1 else ""
    return city, state

def build_research_notes(lead):
    """Build structured research notes for HubSpot marketing_notes field."""
    sections = []

    # Research summary
    summary = lead.get("research_summary", "")
    if summary:
        sections.append(f"[Research Summary]\n{summary}")

    # Company profile
    profile_parts = []
    for key in ["countries", "Countries"]:
        val = lead.get(key, "")
        if val:
            profile_parts.append(f"Countries: {val}")
            break
    for key in ["currencies", "Currencies"]:
        val = lead.get(key, "")
        if val:
            profile_parts.append(f"Currencies: {val}")
            break
    for key in ["business_model", "Business Model"]:
        val = lead.get(key, "")
        if val:
            profile_parts.append(f"Business Model: {val}")
            break
    for key in ["revenue", "Revenue"]:
        val = lead.get(key, "")
        if val:
            profile_parts.append(f"Revenue: {val}")
            break
    if profile_parts:
        sections.append("[Company Profile]\n" + "\n".join(profile_parts))

    # Scoring
    score = lead.get("lead_score", lead.get("Lead Score", ""))
    icp = lead.get("icp_fit", lead.get("ICP Fit", ""))
    priority = lead.get("priority", lead.get("Priority", ""))
    if score:
        sections.append(f"[Scoring]\nLead Score: {score}/100 | ICP Fit: {icp}/5 | Priority: {priority}")

    # Pain points
    pain = lead.get("pain_points", lead.get("Pain Points", ""))
    if pain:
        sections.append(f"[Pain Points]\n{pain}")

    # Outreach angle
    angle = lead.get("outreach_angle", lead.get("Outreach Angle", ""))
    if angle:
        sections.append(f"[Outreach Angle]\n{angle}")

    # Finance setup
    setup = lead.get("finance_setup", lead.get("Finance Setup", ""))
    if setup:
        sections.append(f"[Finance Setup]\n{setup}")

    # Key signals
    signals = lead.get("key_signals", lead.get("Key Signals", ""))
    if signals:
        sections.append(f"[Key Signals]\n{signals}")

    # Growth signals
    growth = lead.get("growth_signals", lead.get("Growth Signals", ""))
    if growth:
        sections.append(f"[Growth Signals]\n{growth}")

    return "\n\n".join(sections) if sections else ""

TIMEZONE_MAP = {
    "Australia/Sydney": "australia_slash_sydney",
    "Asia/Singapore": "asia_slash_singapore",
    "Asia/Manila": "asia_slash_manila",
    "UTC": "utc",
}

def build_properties(lead, config):
    contact_name = lead.get("contact_name", "") or lead.get("Contact Name", "")
    first, last = split_name(contact_name)
    hq = lead.get("hq_location", "") or lead.get("HQ Location", "")
    city, state = parse_location(hq)

    sdr = lead.get("sdr", "") or lead.get("SDR Owner", "")
    owner_id = config["owners"]["hubspot_owner_ids"].get(sdr, "")

    region = config["batch"]["region"]
    tz_raw = config["timezones"].get(region, "UTC")
    tz = TIMEZONE_MAP.get(tz_raw, "utc")

    props = {}
    if first: props["firstname"] = first
    if last: props["lastname"] = last

    email = (lead.get("contact_email", "") or lead.get("Contact Email", "")).strip()
    if email: props["email"] = email

    title = lead.get("contact_title", "") or lead.get("Contact Title", "")
    if title: props["jobtitle"] = title

    company = lead.get("company_name", "") or lead.get("Company Name", "")
    if company: props["company"] = company

    website = lead.get("website", "") or lead.get("Website", "")
    if website: props["website"] = website

    linkedin = lead.get("contact_linkedin", "") or lead.get("Contact LinkedIn", "")
    if linkedin and linkedin.startswith("http"):
        props["linkedin_profile_url"] = linkedin

    countries = lead.get("countries", "") or lead.get("Countries", "")
    if city: props["city"] = city
    if state: props["state"] = state
    if countries: props["country"] = countries

    props["hs_timezone"] = tz
    props["mql_type"] = "TOFU"

    team_size = lead.get("team_size", "") or lead.get("Team Size", "")
    if team_size: props["company_size"] = str(team_size)

    if owner_id: props["hubspot_owner_id"] = owner_id

    # Research notes
    notes = build_research_notes(lead)
    if notes: props["marketing_notes"] = notes

    return props

def hs_request(method, url, headers, json_data=None, retries=4):
    for attempt in range(retries):
        if method == "POST":
            resp = requests.post(url, headers=headers, json=json_data)
        elif method == "PATCH":
            resp = requests.patch(url, headers=headers, json=json_data)
        else:
            resp = requests.get(url, headers=headers)
        if resp.status_code == 429:
            wait = [2, 3, 5, 9][min(attempt, 3)]
            time.sleep(wait)
            continue
        return resp
    return resp

def find_contact(email, headers):
    url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
    payload = {
        "filterGroups": [{"filters": [{"propertyName": "email", "operator": "EQ", "value": email}]}],
        "limit": 1
    }
    resp = hs_request("POST", url, headers, payload)
    if resp.status_code == 200:
        results = resp.json().get("results", [])
        if results:
            return results[0]["id"]
    return None

def main():
    parser = argparse.ArgumentParser(description="Push leads to HubSpot")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview without pushing")
    args = parser.parse_args()

    config = load_config(args.config)
    headers = {
        "Authorization": f"Bearer {config['hubspot']['token']}",
        "Content-Type": "application/json"
    }

    with open(config["input"]["leads_file"]) as f:
        leads = json.load(f)

    # Assign owners if not already set
    sdrs = cycle(config["owners"]["sdrs"])
    for lead in leads:
        if not lead.get("sdr") and not lead.get("SDR Owner"):
            lead["sdr"] = next(sdrs)

    print("=" * 60)
    print(f"HUBSPOT PUSH - {config['batch']['name']}")
    print("=" * 60)
    print(f"Leads: {len(leads)} | Dry run: {args.dry_run}")

    if args.dry_run:
        print("\n[DRY RUN] Preview of first 3 records:")
        for lead in leads[:3]:
            props = build_properties(lead, config)
            name = f"{props.get('firstname', '')} {props.get('lastname', '')}"
            print(f"\n  {name} ({props.get('email', '')})")
            print(f"    Company: {props.get('company', '')}")
            print(f"    Notes length: {len(props.get('marketing_notes', ''))} chars")
        print("\n[DRY RUN] No records pushed.")
        return

    created = 0
    updated = 0
    skipped = 0
    errors = []

    for i, lead in enumerate(leads):
        email = (lead.get("contact_email", "") or lead.get("Contact Email", "")).strip()
        company = lead.get("company_name", "") or lead.get("Company Name", "")
        contact = lead.get("contact_name", "") or lead.get("Contact Name", "")

        if not email:
            skipped += 1
            continue

        props = build_properties(lead, config)
        hs_id = find_contact(email, headers)
        time.sleep(0.12)

        if hs_id:
            resp = hs_request("PATCH", f"https://api.hubapi.com/crm/v3/objects/contacts/{hs_id}",
                            headers, {"properties": props})
            if resp.status_code == 200:
                updated += 1
            else:
                err = resp.json().get("message", str(resp.text))[:150]
                errors.append(f"{contact}: Update {resp.status_code} - {err}")
        else:
            resp = hs_request("POST", "https://api.hubapi.com/crm/v3/objects/contacts",
                            headers, {"properties": props})
            if resp.status_code == 201:
                created += 1
            else:
                err = resp.json().get("message", str(resp.text))[:150]
                errors.append(f"{contact}: Create {resp.status_code} - {err}")

        time.sleep(0.12)

        if (i + 1) % 25 == 0:
            print(f"  [{i+1}/{len(leads)}] Created: {created}, Updated: {updated}, Errors: {len(errors)}")

    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"Created: {created} | Updated: {updated} | Skipped: {skipped} | Errors: {len(errors)}")
    if errors:
        print("\nErrors:")
        for e in errors[:10]:
            print(f"  {e}")

if __name__ == "__main__":
    main()
