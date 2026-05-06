---
skill: customer_retention_rate_calculator
category: small_business
description: Calculate customer retention rate: retained = end_customers - new_customers; rate = retained / start_customers * 100.
tier: free
inputs: start_customers, end_customers, new_customers
---

# Customer Retention Rate Calculator

## Description
Calculate customer retention rate: retained = end_customers - new_customers; rate = retained / start_customers * 100.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `start_customers` | `integer` | Yes | Customers at start of period. |
| `end_customers` | `integer` | Yes | Customers at end of period. |
| `new_customers` | `integer` | Yes | New customers acquired during the period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "customer_retention_rate_calculator",
  "arguments": {
    "start_customers": 0,
    "end_customers": 0,
    "new_customers": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "customer_retention_rate_calculator"`.
