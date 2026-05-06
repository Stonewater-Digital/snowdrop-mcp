---
skill: benchmark_relative_performance
category: market_analytics
description: Calculates performance statistics versus a benchmark including capture ratios and tracking error.
tier: free
inputs: asset_returns, benchmark_returns, risk_free_rate
---

# Benchmark Relative Performance

## Description
Calculates performance statistics versus a benchmark including capture ratios and tracking error.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_returns` | `array` | Yes | Portfolio returns. |
| `benchmark_returns` | `array` | Yes | Benchmark returns. |
| `risk_free_rate` | `number` | Yes | Annual risk-free rate. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "benchmark_relative_performance",
  "arguments": {
    "asset_returns": [],
    "benchmark_returns": [],
    "risk_free_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "benchmark_relative_performance"`.
