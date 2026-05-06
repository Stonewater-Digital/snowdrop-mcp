---
skill: longevity_swap_pricer
category: structured_products
description: Transforms mortality qx inputs into a survival curve, discounts the floating and fixed legs, and reports PV and longevity risk premium. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Longevity Swap Pricer

## Description
Transforms mortality qx inputs into a survival curve, discounts the floating and fixed legs, and reports PV and longevity risk premium. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "longevity_swap_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "longevity_swap_pricer"`.
