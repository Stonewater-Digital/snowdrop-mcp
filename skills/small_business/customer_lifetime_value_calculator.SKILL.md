---
skill: customer_lifetime_value_calculator
category: small_business
description: Calculate Customer Lifetime Value: LTV = avg_purchase * purchase_frequency * customer_lifespan_years.
tier: free
inputs: avg_purchase, purchase_frequency, customer_lifespan_years
---

# Customer Lifetime Value Calculator

## Description
Calculate Customer Lifetime Value: LTV = avg_purchase * purchase_frequency * customer_lifespan_years.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `avg_purchase` | `number` | Yes | Average purchase value. |
| `purchase_frequency` | `number` | Yes | Average number of purchases per year. |
| `customer_lifespan_years` | `number` | Yes | Average customer lifespan in years. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "customer_lifetime_value_calculator",
  "arguments": {
    "avg_purchase": 0,
    "purchase_frequency": 0,
    "customer_lifespan_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "customer_lifetime_value_calculator"`.
