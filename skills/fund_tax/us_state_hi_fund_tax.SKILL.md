---
skill: us_state_hi_fund_tax
category: fund_tax
description: Calculates Hawaii individual tax, nonresident withholding, and GET cash drag on management fees. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Hi Fund Tax

## Description
Calculates Hawaii individual tax, nonresident withholding, and GET cash drag on management fees. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_hi_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_hi_fund_tax"`.
