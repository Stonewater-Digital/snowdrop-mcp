---
skill: monthly_recurring_revenue_calculator
category: small_business
description: Calculate Monthly Recurring Revenue (MRR) and Annual Recurring Revenue (ARR) from a list of subscription plans.
tier: free
inputs: subscriptions
---

# Monthly Recurring Revenue Calculator

## Description
Calculate Monthly Recurring Revenue (MRR) and Annual Recurring Revenue (ARR) from a list of subscription plans.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `subscriptions` | `array` | Yes | List of subscription plans. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "monthly_recurring_revenue_calculator",
  "arguments": {
    "subscriptions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "monthly_recurring_revenue_calculator"`.
