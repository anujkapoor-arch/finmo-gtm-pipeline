#!/usr/bin/env python3
"""
One-time script: Create new Airtable fields in Lead Gen 3.0 tables.
Adds AE Owner, email5-10, whatsapp fields. Removes Lead Category.

Usage:
  python3 lg3_create_airtable_fields.py --config config/config.json
  python3 lg3_create_airtable_fields.py --config config/config.json --dry-run
"""
import json
import argparse
import requests
import time
import sys

def load_config(path):
    with open(path) as f:
        return json.load(f)

def load_field_mappings():
    with open("config/field_mappings.json") as f:
        return json.load(f)

def get_existing_fields(base_id, table_id, headers):
    """Get list of existing field names in a table."""
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    for table in resp.json().get("tables", []):
        if table["id"] == table_id:
            return {f["name"]: f["id"] for f in table.get("fields", [])}
    return {}

def create_field(base_id, table_id, field_def, headers, dry_run=False):
    """Create a single field in a table."""
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields"
    if dry_run:
        print(f"    [DRY RUN] Would create: {field_def['name']} ({field_def['type']})")
        return True
    resp = requests.post(url, headers=headers, json=field_def)
    if resp.status_code == 200:
        return True
    elif resp.status_code == 422 and "already exists" in resp.text.lower():
        print(f"    Already exists: {field_def['name']}")
        return True
    else:
        print(f"    ERROR {resp.status_code}: {resp.text[:200]}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Create new Airtable fields for Lead Gen 3.0")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating")
    args = parser.parse_args()

    config = load_config(args.config)
    mappings = load_field_mappings()

    base_id = config["airtable"]["base_id"]
    headers = {
        "Authorization": f"Bearer {config['airtable']['pat']}",
        "Content-Type": "application/json"
    }

    new_fields = mappings["new_fields_to_create"]
    tables = config["airtable"]["table_ids"]

    print("=" * 60)
    print("AIRTABLE FIELD CREATION - Lead Gen 3.0")
    print("=" * 60)
    print(f"Base: {base_id}")
    print(f"Tables: {list(tables.keys())}")
    print(f"New fields: {len(new_fields)}")
    print(f"Dry run: {args.dry_run}")
    print()

    for region, table_id in tables.items():
        print(f"\n--- {region} ({table_id}) ---")

        # Check existing fields
        existing = get_existing_fields(base_id, table_id, headers)
        print(f"  Existing fields: {len(existing)}")

        created = 0
        skipped = 0
        errors = 0

        for field_def in new_fields:
            if field_def["name"] in existing:
                skipped += 1
                continue

            success = create_field(base_id, table_id, field_def, headers, dry_run=args.dry_run)
            if success:
                created += 1
            else:
                errors += 1
            time.sleep(0.3)

        print(f"  Created: {created}, Skipped (exists): {skipped}, Errors: {errors}")

    # Remove Lead Category field (manual step - Airtable API doesn't support field deletion)
    fields_to_remove = mappings.get("fields_to_remove", [])
    if fields_to_remove:
        print(f"\n--- MANUAL STEP REQUIRED ---")
        print(f"  Remove these fields manually in Airtable UI:")
        for f in fields_to_remove:
            print(f"    - {f}")
        print(f"  (Airtable API does not support field deletion)")

    print(f"\n{'=' * 60}")
    print("DONE")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
