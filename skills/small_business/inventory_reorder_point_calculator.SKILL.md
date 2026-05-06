---
skill: inventory_reorder_point_calculator
category: small_business
description: Calculate the inventory reorder point: ROP = daily_demand * lead_time_days + safety_stock.
tier: free
inputs: daily_demand, lead_time_days
---

# Inventory Reorder Point Calculator

## Description
Calculate the inventory reorder point: ROP = daily_demand * lead_time_days + safety_stock.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daily_demand` | `number` | Yes | Average daily unit demand. |
| `lead_time_days` | `number` | Yes | Supplier lead time in days. |
| `safety_stock` | `number` | No | Safety stock units (default 0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "inventory_reorder_point_calculator",
  "arguments": {
    "daily_demand": 0,
    "lead_time_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inventory_reorder_point_calculator"`.
