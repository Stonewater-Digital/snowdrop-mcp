---
skill: us_state_ny_fund_tax
category: fund_tax
description: Calculates New York State PTE tax, NYC UBT surrogate, and nonresident withholding under Tax Law §§601, 658 and Article 24-A (2021). (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Ny Fund Tax

## Description
Calculates New York State PTE tax, NYC UBT surrogate, and nonresident withholding under Tax Law §§601, 658 and Article 24-A (2021). (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ny_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ny_fund_tax"`.
