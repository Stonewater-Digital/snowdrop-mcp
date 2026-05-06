---
skill: referral_tracker
category: referrals
description: Aggregates referral spend and issues credits to promoters.
tier: free
inputs: referrals
---

# Referral Tracker

## Description
Aggregates referral spend and issues credits to promoters.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `referrals` | `array` | Yes |  |
| `credit_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "referral_tracker",
  "arguments": {
    "referrals": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "referral_tracker"`.
