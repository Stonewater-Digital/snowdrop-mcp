---
skill: cost_basis_averaging_logic
category: technical
description: Calculate cost basis using FIFO, LIFO, average cost, or specific-lot method. Identifies tax-loss harvesting opportunities and wash sale risk.
tier: free
inputs: lots, current_price, method
---

# Cost Basis Averaging Logic

## Description
Calculate cost basis using FIFO, LIFO, average cost, or specific-lot method. Identifies tax-loss harvesting opportunities and wash sale risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lots` | `array` | Yes | List of tax lots, each with: purchase_date (ISO date str), quantity (float), price_per_unit (float), fees (float). |
| `current_price` | `number` | Yes | Current market price per unit. |
| `method` | `string` | Yes | Cost basis calculation method: 'fifo', 'lifo', 'average', or 'specific'. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cost_basis_averaging_logic",
  "arguments": {
    "lots": [],
    "current_price": 0,
    "method": "<method>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cost_basis_averaging_logic"`.
