---
skill: us_state_ga_fund_tax
category: fund_tax
description: Calculates Georgia income tax, SALT workaround election, and nonresident withholding pursuant to O.C.G.A. §§48-7-20 and 48-7-129.
tier: premium
inputs: none
---

# Us State Ga Fund Tax

## Description
Calculates Georgia income tax, SALT workaround election, and nonresident withholding pursuant to O.C.G.A. §§48-7-20 and 48-7-129. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ga_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ga_fund_tax"`.
