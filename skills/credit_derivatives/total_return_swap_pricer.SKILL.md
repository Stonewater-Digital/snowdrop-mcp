---
skill: total_return_swap_pricer
category: credit_derivatives
description: Computes total-return swap mark-to-market using standard equity TRS conventions: asset return minus funded leg with spread and dividends.
tier: free
inputs: previous_price, current_price, notional, funding_rate, funding_spread_bp, days_in_period, dividend_yield
---

# Total Return Swap Pricer

## Description
Computes total-return swap mark-to-market using standard equity TRS conventions: asset return minus funded leg with spread and dividends.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `previous_price` | `number` | Yes | Reference asset price at the start of the accrual period. |
| `current_price` | `number` | Yes | Reference asset price at valuation. |
| `notional` | `number` | Yes | Swap notional representing the financed position. |
| `funding_rate` | `number` | Yes | Annualized floating funding rate (decimal). |
| `funding_spread_bp` | `number` | Yes | Dealer spread over funding curve in basis points. |
| `days_in_period` | `number` | Yes | Accrual days used for day-count conversion (ACT/360). |
| `dividend_yield` | `number` | Yes | Continuous dividend yield of the reference asset (decimal). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "total_return_swap_pricer",
  "arguments": {
    "previous_price": 0,
    "current_price": 0,
    "notional": 0,
    "funding_rate": 0,
    "funding_spread_bp": 0,
    "days_in_period": 0,
    "dividend_yield": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "total_return_swap_pricer"`.
