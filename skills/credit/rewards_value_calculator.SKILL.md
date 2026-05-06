---
skill: rewards_value_calculator
category: credit
description: Calculate the annual dollar value of credit card rewards based on monthly spending, rewards rate, and point value.
tier: free
inputs: monthly_spend, rewards_rate_pct
---

# Rewards Value Calculator

## Description
Calculate the annual dollar value of credit card rewards based on monthly spending, rewards rate, and point value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_spend` | `number` | Yes | Average monthly credit card spending. |
| `rewards_rate_pct` | `number` | Yes | Rewards earning rate as percentage (e.g., 2.0 for 2%). |
| `point_value` | `number` | No | Dollar value per point/mile (default 0.01). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rewards_value_calculator",
  "arguments": {
    "monthly_spend": 0,
    "rewards_rate_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rewards_value_calculator"`.
