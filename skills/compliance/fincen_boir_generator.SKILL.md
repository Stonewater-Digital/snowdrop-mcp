---
skill: fincen_boir_generator
category: compliance
description: Generates a FinCEN Beneficial Ownership Information Report (BOIR) under the Corporate Transparency Act (CTA) 31 U.S.C. § 5336 and 31 CFR Part 1010.380.
tier: premium
inputs: none
---

# Fincen Boir Generator

## Description
Generates a FinCEN Beneficial Ownership Information Report (BOIR) under the Corporate Transparency Act (CTA) 31 U.S.C. § 5336 and 31 CFR Part 1010.380. Validates all required fields, checks the 23 statutory exemption categories, and formats the payload for FinCEN BOIR online submission. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fincen_boir_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fincen_boir_generator"`.
