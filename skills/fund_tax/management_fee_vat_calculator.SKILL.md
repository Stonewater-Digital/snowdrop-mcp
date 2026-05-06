---
skill: management_fee_vat_calculator
category: fund_tax
description: Determines VAT/GST on management fees and whether exemptions/zero-rating apply. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Management Fee Vat Calculator

## Description
Determines VAT/GST on management fees and whether exemptions/zero-rating apply. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "management_fee_vat_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "management_fee_vat_calculator"`.
