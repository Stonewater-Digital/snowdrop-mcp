---
skill: churn_rate_calculator
category: small_business
description: Calculate customer churn rate for a period and annualized churn rate.
tier: free
inputs: start_customers, lost_customers
---

# Churn Rate Calculator

## Description
Calculate customer churn rate for a period and annualized churn rate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `start_customers` | `integer` | Yes | Customers at start of period. |
| `lost_customers` | `integer` | Yes | Customers lost during the period. |
| `period_months` | `integer` | No | Period length in months (default 1). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "churn_rate_calculator",
  "arguments": {
    "start_customers": 0,
    "lost_customers": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "churn_rate_calculator"`.
