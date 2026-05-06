---
skill: rwa_treasury_rebate_payment_tracker
category: crypto_rwa
description: Tracks rebate and coupon-equivalent flows into token treasury accounts.
tier: free
inputs: payload
---

# Rwa Treasury Rebate Payment Tracker

## Description
Tracks rebate and coupon-equivalent flows into token treasury accounts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_treasury_rebate_payment_tracker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_rebate_payment_tracker"`.
