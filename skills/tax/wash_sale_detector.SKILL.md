---
skill: wash_sale_detector
category: tax
description: Flags loss sales with repurchases inside the 30-day wash window.
tier: free
inputs: transactions
---

# Wash Sale Detector

## Description
Flags loss sales with repurchases inside the 30-day wash window.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transactions` | `array` | Yes | Transactions with asset, action, date, amount, price. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "wash_sale_detector",
  "arguments": {
    "transactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "wash_sale_detector"`.
