---
skill: inventory_turnover_calculator
category: accounting
description: Calculates inventory turnover ratio and average days to sell inventory.
tier: free
inputs: cogs, avg_inventory
---

# Inventory Turnover Calculator

## Description
Calculates inventory turnover ratio and average days to sell inventory.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cogs` | `number` | Yes | Cost of goods sold for the period. |
| `avg_inventory` | `number` | Yes | Average inventory value for the period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "inventory_turnover_calculator",
  "arguments": {
    "cogs": 0,
    "avg_inventory": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inventory_turnover_calculator"`.
