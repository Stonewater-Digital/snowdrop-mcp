---
skill: treynor_ratio_calculator
category: market_analytics
description: Computes Treynor ratio, beta, Jensen's alpha, and systematic risk contribution.
tier: free
inputs: returns, benchmark_returns, risk_free_rate
---

# Treynor Ratio Calculator

## Description
Computes Treynor ratio, beta, Jensen's alpha, and systematic risk contribution.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Portfolio returns (decimal). |
| `benchmark_returns` | `array` | Yes | Benchmark returns aligned with portfolio. |
| `risk_free_rate` | `number` | Yes | Annual risk-free rate. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "treynor_ratio_calculator",
  "arguments": {
    "returns": [],
    "benchmark_returns": [],
    "risk_free_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "treynor_ratio_calculator"`.
