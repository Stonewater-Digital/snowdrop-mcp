---
skill: inventory_valuation
category: small_business
description: Runs FIFO, LIFO, and weighted-average calculations to derive COGS and ending inventory, highlighting gross profit differences between methods.
tier: free
inputs: purchases, sales, method
---

# Inventory Valuation

## Description
Runs FIFO, LIFO, and weighted-average calculations to derive COGS and ending inventory, highlighting gross profit differences between methods.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `purchases` | `array` | Yes | List of purchases {date, quantity, unit_cost}. |
| `sales` | `array` | Yes | List of sales {date, quantity}. |
| `method` | `string` | Yes | fifo, lifo, or weighted_avg. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "inventory_valuation",
  "arguments": {
    "purchases": [],
    "sales": [],
    "method": "<method>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inventory_valuation"`.
