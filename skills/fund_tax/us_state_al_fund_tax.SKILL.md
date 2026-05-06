---
skill: us_state_al_fund_tax
category: fund_tax
description: Computes Alabama pass-through entity tax, nonresident withholding, and composite filing triggers pursuant to Ala. Code §§40-18-14 and 40-18-24.
tier: premium
inputs: none
---

# Us State Al Fund Tax

## Description
Computes Alabama pass-through entity tax, nonresident withholding, and composite filing triggers pursuant to Ala. Code §§40-18-14 and 40-18-24. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_al_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_al_fund_tax"`.
