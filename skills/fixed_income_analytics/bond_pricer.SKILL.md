---
skill: bond_pricer
category: fixed_income_analytics
description: Prices a fixed-rate bond using standard street-convention accrued interest under 30/360, ACT/ACT, or ACT/360 day-count with support for semi-annual or quarterly coupons. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Bond Pricer

## Description
Prices a fixed-rate bond using standard street-convention accrued interest under 30/360, ACT/ACT, or ACT/360 day-count with support for semi-annual or quarterly coupons. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "bond_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bond_pricer"`.
