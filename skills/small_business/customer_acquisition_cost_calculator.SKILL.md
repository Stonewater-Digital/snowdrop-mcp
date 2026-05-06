---
skill: customer_acquisition_cost_calculator
category: small_business
description: Calculate Customer Acquisition Cost: CAC = total_marketing_spend / new_customers. Optionally compute LTV:CAC ratio.
tier: free
inputs: total_marketing_spend, new_customers
---

# Customer Acquisition Cost Calculator

## Description
Calculate Customer Acquisition Cost: CAC = total_marketing_spend / new_customers. Optionally compute LTV:CAC ratio.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_marketing_spend` | `number` | Yes | Total marketing and sales spend. |
| `new_customers` | `integer` | Yes | Number of new customers acquired. |
| `ltv` | `number` | No | Optional Customer Lifetime Value for LTV:CAC ratio. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "customer_acquisition_cost_calculator",
  "arguments": {
    "total_marketing_spend": 0,
    "new_customers": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "customer_acquisition_cost_calculator"`.
