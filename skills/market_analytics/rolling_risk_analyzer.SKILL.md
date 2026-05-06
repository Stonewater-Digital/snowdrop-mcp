---
skill: rolling_risk_analyzer
category: market_analytics
description: Computes rolling Sharpe, max drawdown, beta (optional), and detects volatility regime shifts.
tier: free
inputs: returns, window_size
---

# Rolling Risk Analyzer

## Description
Computes rolling Sharpe, max drawdown, beta (optional), and detects volatility regime shifts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Return series. |
| `window_size` | `integer` | Yes | Rolling window length. |
| `benchmark_returns` | `array` | No | Optional benchmark returns for beta. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rolling_risk_analyzer",
  "arguments": {
    "returns": [],
    "window_size": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rolling_risk_analyzer"`.
