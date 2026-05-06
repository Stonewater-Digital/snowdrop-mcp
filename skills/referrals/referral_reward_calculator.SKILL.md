---
skill: referral_reward_calculator
category: referrals
description: Determines referral tier, rate, and milestone bonuses.
tier: free
inputs: referrer_id, total_referrals, total_referred_spend
---

# Referral Reward Calculator

## Description
Determines referral tier, rate, and milestone bonuses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `referrer_id` | `string` | Yes |  |
| `total_referrals` | `integer` | Yes |  |
| `total_referred_spend` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "referral_reward_calculator",
  "arguments": {
    "referrer_id": "<referrer_id>",
    "total_referrals": 0,
    "total_referred_spend": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "referral_reward_calculator"`.
