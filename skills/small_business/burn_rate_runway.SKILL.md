---
skill: burn_rate_runway
category: small_business
description: Computes gross and net burn rates, cash runway, and projected zero-cash date accounting for compounding revenue growth.
tier: free
inputs: monthly_revenue, monthly_expenses, cash_on_hand, revenue_growth_rate
---

# Burn Rate Runway

## Description
Computes gross and net burn rates, cash runway, and projected zero-cash date accounting for compounding revenue growth.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_revenue` | `number` | Yes | Current recurring revenue per month. |
| `monthly_expenses` | `number` | Yes | Operating expenses per month. |
| `cash_on_hand` | `number` | Yes | Cash reserves available. |
| `revenue_growth_rate` | `number` | Yes | Expected monthly revenue growth rate as decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "burn_rate_runway",
  "arguments": {
    "monthly_revenue": 0,
    "monthly_expenses": 0,
    "cash_on_hand": 0,
    "revenue_growth_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "burn_rate_runway"`.
