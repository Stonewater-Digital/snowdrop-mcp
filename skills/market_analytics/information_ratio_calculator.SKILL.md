---
skill: information_ratio_calculator
category: market_analytics
description: Computes Information Ratio, tracking error, active return, and hit rate.
tier: free
inputs: portfolio_returns, benchmark_returns
---

# Information Ratio Calculator

## Description
Computes Information Ratio, tracking error, active return, and hit rate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_returns` | `array` | Yes | Portfolio returns (decimal). |
| `benchmark_returns` | `array` | Yes | Benchmark returns aligned with portfolio. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "information_ratio_calculator",
  "arguments": {
    "portfolio_returns": [],
    "benchmark_returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "information_ratio_calculator"`.
