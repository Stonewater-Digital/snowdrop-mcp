---
skill: portfolio_beta_calculator
category: portfolio
description: Calculates portfolio beta as covariance(portfolio, market) / variance(market), measuring sensitivity to market movements.
tier: free
inputs: portfolio_returns, market_returns
---

# Portfolio Beta Calculator

## Description
Calculates portfolio beta as covariance(portfolio, market) / variance(market), measuring sensitivity to market movements.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_returns` | `array` | Yes | List of portfolio periodic returns. |
| `market_returns` | `array` | Yes | List of market periodic returns (same length). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_beta_calculator",
  "arguments": {
    "portfolio_returns": [],
    "market_returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_beta_calculator"`.
