---
skill: us_state_ok_fund_tax
category: fund_tax
description: Calculates Oklahoma top marginal tax, elective entity-level tax, and Form 512-S withholding obligations. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Ok Fund Tax

## Description
Calculates Oklahoma top marginal tax, elective entity-level tax, and Form 512-S withholding obligations. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ok_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ok_fund_tax"`.
