---
skill: merger_arbitrage_spread
category: alternative_investments
description: Computes dollar and annualized spread along with implied deal probability from price-break analysis. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: target_price, offer_price, expected_close_days, risk_free_rate, break_price
---

# Merger Arbitrage Spread

## Description
Computes dollar and annualized merger arbitrage spread along with implied deal probability from price-break analysis. Outputs expected return, annualized spread, and deal/break probability weighting. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target_price` | `number` | Yes | Current market price of the target company (dollars per share). |
| `offer_price` | `number` | Yes | Announced acquisition offer price (dollars per share). |
| `expected_close_days` | `integer` | Yes | Estimated business days until deal closes. |
| `risk_free_rate` | `number` | Yes | Risk-free rate as a decimal (e.g. 0.05 for 5% annualized). |
| `break_price` | `number` | No | Estimated stock price if the deal breaks (defaults to pre-announcement level). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "merger_arbitrage_spread",
  "arguments": {
    "target_price": 47.80,
    "offer_price": 50.00,
    "expected_close_days": 90,
    "risk_free_rate": 0.05,
    "break_price": 38.00
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "merger_arbitrage_spread"`.
