---
skill: ambassador_reward_calculator
category: ambassadors
description: Computes base rewards and bonuses for ambassador activity.
tier: free
inputs: ambassador_id, monthly_metrics
---

# Ambassador Reward Calculator

## Description
Computes base rewards and bonuses for ambassador activity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ambassador_id` | `string` | Yes |  |
| `monthly_metrics` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ambassador_reward_calculator",
  "arguments": {
    "ambassador_id": "<ambassador_id>",
    "monthly_metrics": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ambassador_reward_calculator"`.
