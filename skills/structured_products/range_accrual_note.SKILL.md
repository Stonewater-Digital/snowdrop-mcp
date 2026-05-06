---
skill: range_accrual_note
category: structured_products
description: Uses Black-style lognormal assumption for the reference rate to compute expected coupons on a range accrual structured note. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Range Accrual Note

## Description
Uses Black-style lognormal assumption for the reference rate to compute expected coupons on a range accrual structured note. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "range_accrual_note",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "range_accrual_note"`.
