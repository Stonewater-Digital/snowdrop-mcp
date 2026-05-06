---
skill: partner_revenue_share_calculator
category: partners
description: Computes revenue share payouts per partner tier.
tier: free
inputs: partners, period
---

# Partner Revenue Share Calculator

## Description
Computes revenue share payouts per partner tier.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `partners` | `array` | Yes |  |
| `period` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "partner_revenue_share_calculator",
  "arguments": {
    "partners": [],
    "period": "<period>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "partner_revenue_share_calculator"`.
