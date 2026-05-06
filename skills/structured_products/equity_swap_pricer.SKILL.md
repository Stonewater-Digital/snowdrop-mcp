---
skill: equity_swap_pricer
category: structured_products
description: Discounts realized equity leg returns against fixed rate leg to compute PV, DV01, and carry. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Equity Swap Pricer

## Description
Discounts realized equity leg returns against fixed rate leg to compute PV, DV01, and carry. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "equity_swap_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "equity_swap_pricer"`.
