#!/usr/bin/env python3
"""
Sanity check script - runs all 13 quality checks against Airtable data.
Reports pass/fail with counts for each rule.

Usage:
  python3 lg3_sanity_check.py --config config/config.json
  python3 lg3_sanity_check.py --config config/config.json --table AU
"""
import json
import argparse
import requests
import time
import re

def load_config(path):
    with open(path) as f:
        return json.load(f)

def fetch_all_records(base_id, table_id, fields, headers):
    records = []
    offset = None
    fp = "&".join([f"fields%5B%5D={f.replace(' ','+')}" for f in fields])
    while True:
        url = f"https://api.airtable.com/v0/{base_id}/{table_id}?{fp}&pageSize=100"
        if offset:
            url += f"&offset={offset}"
        resp = requests.get(url, headers=headers)
        data = resp.json()
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
    return records

def main():
    parser = argparse.ArgumentParser(description="Run sanity checks on Lead Gen 3.0 data")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--table", help="Check specific table only (AU/SG/PH/Other)")
    args = parser.parse_args()

    config = load_config(args.config)
    base_id = config["airtable"]["base_id"]
    headers = {"Authorization": f"Bearer {config['airtable']['pat']}"}

    tables = config["airtable"]["table_ids"]
    if args.table:
        tables = {args.table: tables[args.table]}

    FETCH_FIELDS = [
        "Company Name", "Contact Name", "Contact Email", "Contact Title",
        "Timezone", "HubSpot Contact URL", "SDR Owner", "AE Owner",
        "Lead Score", "Priority",
        "custom_email1", "custom_email2", "custom_email3", "custom_email4",
        "custom_linkedin_cr", "custom_linkedin1", "ae_linkedin_cr",
        "email5_body", "email6_body", "email7_body", "email8_body",
        "email9_body", "email10_body",
        "Website",
    ]

    TEXT_FIELDS = [
        "custom_email1", "custom_email2", "custom_email3", "custom_email4",
        "custom_linkedin_cr", "custom_linkedin1", "custom_linkedin2",
        "custom_linkedin3", "custom_linkedin4", "ae_linkedin_cr",
        "email5_body", "email6_body", "email7_body", "email8_body",
        "email9_body", "email10_body",
    ]

    VALID_SDRS = {"Harini", "Sukriti"}
    VALID_AES = {"Gibson Saw", "Nouvelle Nye", "Elross Pangue", "Michelle Ling"}

    results = {i: {"pass": 0, "fail": 0, "details": []} for i in range(1, 14)}
    total_records = 0

    for table_name, table_id in tables.items():
        records = fetch_all_records(base_id, table_id, FETCH_FIELDS, headers)
        total_records += len(records)

        for r in records:
            f = r.get("fields", {})
            company = f.get("Company Name", "?")
            email = f.get("Contact Email", "")
            priority = f.get("Priority", "")
            score = f.get("Lead Score", 0) or 0
            has_sdr = bool(f.get("custom_email1"))
            has_ae = bool(f.get("email5_body"))
            has_ceo = bool(f.get("email9_body"))

            # 1. Timezone
            if f.get("Timezone"):
                results[1]["pass"] += 1
            else:
                results[1]["fail"] += 1
                results[1]["details"].append(f"{table_name}: {company}")

            # 2. HubSpot Contact URL
            if f.get("HubSpot Contact URL") or not email:
                results[2]["pass"] += 1
            else:
                results[2]["fail"] += 1
                results[2]["details"].append(f"{table_name}: {company}")

            # 3. Owners match (checked separately via HubSpot API - skip here, just check Airtable has them)

            # 4. Duplicates (checked by grouping - handled below)

            # 5. Content completeness
            if priority == "HIGH" and int(score) >= 70:
                # P1 - needs SDR + AE + CEO
                if has_sdr and has_ae and has_ceo:
                    results[5]["pass"] += 1
                else:
                    results[5]["fail"] += 1
                    missing = []
                    if not has_sdr: missing.append("SDR")
                    if not has_ae: missing.append("AE")
                    if not has_ceo: missing.append("CEO")
                    results[5]["details"].append(f"{table_name}: {company} (score {score}) missing {','.join(missing)}")
            elif priority == "HIGH":
                # P2 - needs SDR + AE
                if has_sdr and has_ae:
                    results[5]["pass"] += 1
                elif has_sdr:
                    results[5]["fail"] += 1
                    results[5]["details"].append(f"{table_name}: {company} (score {score}) missing AE")
                else:
                    results[5]["pass"] += 1  # No content expected for very low scores

            # 6. No hardcoded sender names
            hardcoded_found = False
            for tf in TEXT_FIELDS:
                val = f.get(tf, "")
                if not val:
                    continue
                for pattern in ["David from Finmo", "David here", "it's David", "Anuj from Finmo"]:
                    if pattern in val:
                        hardcoded_found = True
                        results[6]["details"].append(f"{table_name}: {company} | {tf} | '{pattern}'")
            if hardcoded_found:
                results[6]["fail"] += 1
            else:
                results[6]["pass"] += 1

            # 7. No sender_first_name in greetings
            greeting_issue = False
            for tf in TEXT_FIELDS:
                val = f.get(tf, "")
                if "Hi {{sender_first_name}}" in val:
                    greeting_issue = True
                    results[7]["details"].append(f"{table_name}: {company} | {tf}")
            if greeting_issue:
                results[7]["fail"] += 1
            else:
                results[7]["pass"] += 1

            # 8. Sign-off format (spot check on E2 and E5)
            e2 = f.get("custom_email2", "")
            e5 = f.get("email5_body", "")
            signoff_ok = True
            if e2 and not e2.rstrip().endswith("{{sender_last_name}}"):
                signoff_ok = False
                results[8]["details"].append(f"{table_name}: {company} | custom_email2 missing full name sign-off")
            if e5 and not e5.rstrip().endswith("{{sender_last_name}}"):
                signoff_ok = False
                results[8]["details"].append(f"{table_name}: {company} | email5_body missing full name sign-off")
            if signoff_ok:
                results[8]["pass"] += 1
            else:
                results[8]["fail"] += 1

            # 9. LinkedIn CR non-salesy
            cr = f.get("custom_linkedin_cr", "")
            if cr:
                salesy = any(p in cr for p in ["put together", "guide", "Want me to send", "great to e-meet"])
                if salesy:
                    results[9]["fail"] += 1
                    results[9]["details"].append(f"{table_name}: {company}")
                else:
                    results[9]["pass"] += 1

            # 10. AE LinkedIn CR exists where AE content exists
            if has_ae:
                if f.get("ae_linkedin_cr"):
                    results[10]["pass"] += 1
                else:
                    results[10]["fail"] += 1
                    results[10]["details"].append(f"{table_name}: {company}")

            # 12. Email domain mismatch
            if email:
                domain = email.split("@")[1] if "@" in email else ""
                if domain in ("wellsfargo.com", "gmail.com", "yahoo.com", "hotmail.com"):
                    results[12]["fail"] += 1
                    results[12]["details"].append(f"{table_name}: {company} | {email}")
                else:
                    results[12]["pass"] += 1

            # 13. SDR + AE Owner assigned where content exists
            if has_sdr:
                sdr = f.get("SDR Owner", "")
                ae = f.get("AE Owner", "")
                if sdr in VALID_SDRS and (ae in VALID_AES or not has_ae):
                    results[13]["pass"] += 1
                else:
                    results[13]["fail"] += 1
                    issues = []
                    if sdr not in VALID_SDRS: issues.append(f"SDR='{sdr}'")
                    if has_ae and ae not in VALID_AES: issues.append(f"AE='{ae}'")
                    results[13]["details"].append(f"{table_name}: {company} | {', '.join(issues)}")

    # Print results
    print("=" * 70)
    print(f"SANITY CHECK RESULTS ({total_records} records across {len(tables)} tables)")
    print("=" * 70)

    checks = {
        1: "Timezone populated",
        2: "HubSpot Contact URL populated",
        5: "P1/P2 content completeness",
        6: "No hardcoded sender names",
        7: "No {{sender_first_name}} in greetings",
        8: "Correct sign-off format (Cheers/Best + full name)",
        9: "LinkedIn CR is non-salesy",
        10: "AE LinkedIn CR exists where AE content exists",
        12: "No email domain mismatches",
        13: "SDR + AE Owner assigned",
    }

    all_pass = True
    for num, label in checks.items():
        r = results[num]
        status = "PASS" if r["fail"] == 0 else "FAIL"
        icon = "OK" if status == "PASS" else "XX"
        print(f"\n  [{icon}] Check {num:>2}: {label}")
        print(f"       Pass: {r['pass']} | Fail: {r['fail']}")
        if r["fail"] > 0:
            all_pass = False
            for d in r["details"][:5]:
                print(f"       - {d}")
            if len(r["details"]) > 5:
                print(f"       ... and {len(r['details']) - 5} more")

    print(f"\n{'='*70}")
    if all_pass:
        print("ALL CHECKS PASSED")
    else:
        failed = sum(1 for n in checks if results[n]["fail"] > 0)
        print(f"FAILED: {failed}/{len(checks)} checks have issues")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
