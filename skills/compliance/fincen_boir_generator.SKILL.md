---
skill: fincen_boir_generator
category: compliance
description: Generates a FinCEN Beneficial Ownership Information Report (BOIR) under the Corporate Transparency Act (CTA) 31 U.S.C. § 5336 and 31 CFR Part 1010.380.
tier: premium
inputs: entity_data
---

# Fincen Boir Generator

## Description
Generates a FinCEN Beneficial Ownership Information Report (BOIR) under the Corporate Transparency Act (CTA) 31 U.S.C. § 5336 and 31 CFR Part 1010.380. Validates all required fields, checks the 23 statutory exemption categories, and formats the payload for FinCEN BOIR online submission. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_data` | `object` | Yes | Reporting company and beneficial owner details required for FinCEN BOIR including legal name, EIN, jurisdiction, and beneficial ownership information |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fincen_boir_generator",
  "arguments": {
    "entity_data": {
      "legal_name": "Acme Holdings LLC",
      "ein": "12-3456789",
      "jurisdiction": "Delaware",
      "beneficial_owners": [
        {"name": "Jane Smith", "dob": "1980-05-15", "ownership_pct": 55}
      ]
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fincen_boir_generator"`.
