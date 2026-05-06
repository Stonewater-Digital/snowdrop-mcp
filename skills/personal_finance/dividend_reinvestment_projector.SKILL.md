---
skill: dividend_reinvestment_projector
category: personal_finance
description: Projects a dividend reinvestment plan by compounding dividends into new shares with growth assumptions for payouts and share price.
tier: free
inputs: initial_shares, share_price, annual_dividend_per_share, dividend_growth_rate, years, price_growth_rate
---

# Dividend Reinvestment Projector

## Description
Projects a dividend reinvestment plan by compounding dividends into new shares with growth assumptions for payouts and share price.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `initial_shares` | `number` | Yes | Starting share count. |
| `share_price` | `number` | Yes | Current share price in dollars. |
| `annual_dividend_per_share` | `number` | Yes | Current annual dividend per share. |
| `dividend_growth_rate` | `number` | Yes | Expected annual dividend growth rate as decimal. |
| `years` | `number` | Yes | Projection horizon in years. |
| `price_growth_rate` | `number` | Yes | Annual share price growth rate as decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dividend_reinvestment_projector",
  "arguments": {
    "initial_shares": 0,
    "share_price": 0,
    "annual_dividend_per_share": 0,
    "dividend_growth_rate": 0,
    "years": 0,
    "price_growth_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dividend_reinvestment_projector"`.
