---
skill: us_state_pa_fund_tax
category: fund_tax
description: Calculates Pennsylvania nonresident withholding and flat tax exposure per 72 P.S. §§7302 and 7335.
tier: premium
inputs: none
---

# Us State Pa Fund Tax

## Description
Calculates Pennsylvania nonresident withholding and flat tax exposure per 72 P.S. §§7302 and 7335. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_pa_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_pa_fund_tax"`.
