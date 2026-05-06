---
skill: total_return_swap_pricer
category: structured_products
description: Discounts realized equity leg cashflows against floating leg funding to output PVs, breakeven spread, and sensitivity. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Total Return Swap Pricer

## Description
Discounts realized equity leg cashflows against floating leg funding to output PVs, breakeven spread, and sensitivity. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "total_return_swap_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "total_return_swap_pricer"`.
