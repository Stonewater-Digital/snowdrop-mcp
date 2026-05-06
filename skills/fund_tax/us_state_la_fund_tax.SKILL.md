---
skill: us_state_la_fund_tax
category: fund_tax
description: Computes Louisiana top marginal tax, elective PTE tax, and nonresident withholding for composite return compliance. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State La Fund Tax

## Description
Computes Louisiana top marginal tax, elective PTE tax, and nonresident withholding for composite return compliance. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_la_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_la_fund_tax"`.
