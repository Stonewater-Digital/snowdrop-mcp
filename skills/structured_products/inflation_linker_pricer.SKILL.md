---
skill: inflation_linker_pricer
category: structured_products
description: Discounts inflation-linked coupons on the real yield curve and reports price and duration versus inflation assumptions. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Inflation Linker Pricer

## Description
Discounts inflation-linked coupons on the real yield curve and reports price and duration versus inflation assumptions. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "inflation_linker_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inflation_linker_pricer"`.
