---
skill: tax_aware_rebalancer
category: portfolio_construction
description: Constructs a tax-lot aware rebalance plan that respects capital gains budgets, wash-sale windows, and differentiates long- vs short-term tax rates per IRS Publication 550 guidance.
tier: free
inputs: positions, target_weights
---

# Tax Aware Rebalancer

## Description
Constructs a tax-lot aware rebalance plan that respects capital gains budgets, wash-sale windows, and differentiates long- vs short-term tax rates per IRS Publication 550 guidance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes | List of positions with quantity, cost basis, and acquisition date. |
| `target_weights` | `object` | Yes | Desired post-trade weights keyed by ticker (must sum to <=1). |
| `cash_allocation` | `number` | No | Optional target cash weight; residual allocated proportionally if omitted. |
| `long_term_rate` | `number` | No | Tax rate applied to positions held > 365 days (decimal). |
| `short_term_rate` | `number` | No | Tax rate applied to positions held <= 365 days (decimal). |
| `tax_budget` | `number` | No | Maximum cash tax to realize for the rebalance; defaults unlimited. |
| `as_of_date` | `string` | No | ISO-8601 date to evaluate holding period and wash sale window (default today). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tax_aware_rebalancer",
  "arguments": {
    "positions": [],
    "target_weights": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tax_aware_rebalancer"`.
