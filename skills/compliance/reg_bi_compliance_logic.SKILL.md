---
skill: reg_bi_compliance_logic
category: compliance
description: Evaluates a broker-dealer recommendation against SEC Regulation Best Interest (17 CFR § 240.15l-1) four-obligation framework: Disclosure, Care, Conflict of Interest, and Compliance. Scores each obligation and identifies documentation requirements.
tier: premium
inputs: none
---

# Reg Bi Compliance Logic

## Description
Evaluates a broker-dealer recommendation against SEC Regulation Best Interest (17 CFR § 240.15l-1) four-obligation framework: Disclosure, Care, Conflict of Interest, and Compliance. Scores each obligation and identifies documentation requirements. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "reg_bi_compliance_logic",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reg_bi_compliance_logic"`.
