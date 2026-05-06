---
skill: convertible_arbitrage_analytics
category: alternative_investments
description: Computes share hedge, gamma exposure, and credit/borrow carry for convert arb positions. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: cb_price, stock_price, delta, gamma, credit_spread, borrow_cost
---

# Convertible Arbitrage Analytics

## Description
Computes share hedge ratio, gamma exposure, and credit/borrow carry for convertible bond arbitrage positions. Outputs net P&L attribution across equity delta, credit spread, and financing components. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cb_price` | `number` | Yes | Current convertible bond price (dollars per bond). |
| `stock_price` | `number` | Yes | Current underlying stock price (dollars per share). |
| `delta` | `number` | Yes | Equity delta of the convertible bond (0–1). |
| `gamma` | `number` | Yes | Gamma of the embedded option (change in delta per unit stock move). |
| `credit_spread` | `number` | Yes | Issuer credit spread as a decimal (e.g. 0.03 for 300 bps). |
| `borrow_cost` | `number` | Yes | Stock borrow cost as an annual decimal (e.g. 0.005 for 50 bps). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "convertible_arbitrage_analytics",
  "arguments": {
    "cb_price": 1050.0,
    "stock_price": 42.50,
    "delta": 0.65,
    "gamma": 0.012,
    "credit_spread": 0.025,
    "borrow_cost": 0.004
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "convertible_arbitrage_analytics"`.
