---
skill: cln_pricer
category: structured_products
description: Discounts CLN coupons and principal with expected loss per Hull (2006) to estimate fair price and incremental spread. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Cln Pricer

## Description
Discounts CLN coupons and principal with expected loss per Hull (2006) to estimate fair price and incremental spread. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "cln_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cln_pricer"`.
