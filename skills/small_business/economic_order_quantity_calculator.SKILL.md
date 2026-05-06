---
skill: economic_order_quantity_calculator
category: small_business
description: Calculate the Economic Order Quantity (EOQ): the optimal order size that minimizes total inventory costs. EOQ = sqrt(2 * annual_demand * order_cost / holding_cost).
tier: free
inputs: annual_demand, order_cost, holding_cost
---

# Economic Order Quantity Calculator

## Description
Calculate the Economic Order Quantity (EOQ): the optimal order size that minimizes total inventory costs. EOQ = sqrt(2 * annual_demand * order_cost / holding_cost).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_demand` | `number` | Yes | Annual unit demand. |
| `order_cost` | `number` | Yes | Cost per order placed. |
| `holding_cost` | `number` | Yes | Annual holding cost per unit. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "economic_order_quantity_calculator",
  "arguments": {
    "annual_demand": 0,
    "order_cost": 0,
    "holding_cost": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "economic_order_quantity_calculator"`.
