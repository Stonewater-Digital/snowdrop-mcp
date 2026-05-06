---
skill: marketplace_take_rate_analyzer
category: small_business
description: Calculates marketplace take rate, per-order contribution, estimated buyer/seller LTV, and a liquidity score using GMV, revenue, and CAC inputs.
tier: free
inputs: gmv, revenue, buyer_cac, seller_cac, orders, avg_order_value
---

# Marketplace Take Rate Analyzer

## Description
Calculates marketplace take rate, per-order contribution, estimated buyer/seller LTV, and a liquidity score using GMV, revenue, and CAC inputs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gmv` | `number` | Yes | Gross merchandise value processed in the period. |
| `revenue` | `number` | Yes | Marketplace revenue (fees) over the same period. |
| `buyer_cac` | `number` | Yes | Average cost to acquire one buyer. |
| `seller_cac` | `number` | Yes | Average cost to onboard one seller. |
| `orders` | `number` | Yes | Number of completed transactions. |
| `avg_order_value` | `number` | Yes | Average GMV per order. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "marketplace_take_rate_analyzer",
  "arguments": {
    "gmv": 0,
    "revenue": 0,
    "buyer_cac": 0,
    "seller_cac": 0,
    "orders": 0,
    "avg_order_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "marketplace_take_rate_analyzer"`.
