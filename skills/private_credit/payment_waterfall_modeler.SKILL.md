---
skill: payment_waterfall_modeler
category: private_credit
description: Distributes cash through tranche priorities covering interest then principal.
tier: free
inputs: cash_available, tranches
---

# Payment Waterfall Modeler

## Description
Distributes cash through tranche priorities covering interest then principal.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash_available` | `number` | Yes |  |
| `tranches` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "payment_waterfall_modeler",
  "arguments": {
    "cash_available": 0,
    "tranches": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "payment_waterfall_modeler"`.
