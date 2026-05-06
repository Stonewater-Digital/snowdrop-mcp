---
skill: us_state_nc_fund_tax
category: fund_tax
description: Handles North Carolina flat tax, SALT election, and nonresident withholding compliance. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Nc Fund Tax

## Description
Handles North Carolina flat tax, SALT election, and nonresident withholding compliance. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_nc_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_nc_fund_tax"`.
