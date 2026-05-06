---
skill: us_state_ia_fund_tax
category: fund_tax
description: Implements Iowa flat tax transition, SALT election, and nonresident withholding thresholds. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Ia Fund Tax

## Description
Implements Iowa flat tax transition, SALT election, and nonresident withholding thresholds. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ia_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ia_fund_tax"`.
