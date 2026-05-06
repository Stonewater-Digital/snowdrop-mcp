---
skill: dynamic_discount_calculator
category: pricing
description: Applies tiered volume and loyalty discounts for agents.
tier: free
inputs: agent_id, monthly_spend, months_active, total_lifetime_spend
---

# Dynamic Discount Calculator

## Description
Applies tiered volume and loyalty discounts for agents.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `monthly_spend` | `number` | Yes |  |
| `months_active` | `integer` | Yes |  |
| `total_lifetime_spend` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dynamic_discount_calculator",
  "arguments": {
    "agent_id": "<agent_id>",
    "monthly_spend": 0,
    "months_active": 0,
    "total_lifetime_spend": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dynamic_discount_calculator"`.
