---
skill: staking_reward_tracker
category: defi
description: Summarizes staking rewards, projected income, and outstanding claims per validator.
tier: free
inputs: stakes
---

# Staking Reward Tracker

## Description
Summarizes staking rewards, projected income, and outstanding claims per validator.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `stakes` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "staking_reward_tracker",
  "arguments": {
    "stakes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "staking_reward_tracker"`.
