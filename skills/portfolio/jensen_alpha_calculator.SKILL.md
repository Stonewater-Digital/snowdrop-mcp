---
skill: jensen_alpha_calculator
category: portfolio
description: Calculates Jensen's alpha, the excess return of a portfolio over the expected return predicted by the CAPM.
tier: free
inputs: portfolio_return, risk_free_rate, beta, market_return
---

# Jensen Alpha Calculator

## Description
Calculates Jensen's alpha, the excess return of a portfolio over the expected return predicted by the CAPM.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_return` | `number` | Yes | Actual portfolio return (decimal). |
| `risk_free_rate` | `number` | Yes | Risk-free rate (decimal). |
| `beta` | `number` | Yes | Portfolio beta. |
| `market_return` | `number` | Yes | Market return (decimal). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "jensen_alpha_calculator",
  "arguments": {
    "portfolio_return": 0,
    "risk_free_rate": 0,
    "beta": 0,
    "market_return": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "jensen_alpha_calculator"`.
