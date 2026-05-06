---
skill: tracking_error_calculator
category: market_analytics
description: Computes tracking error, active return, and a rough active-share proxy from return differences.
tier: free
inputs: portfolio_returns, benchmark_returns
---

# Tracking Error Calculator

## Description
Computes tracking error, active return, and a rough active-share proxy from return differences.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_returns` | `array` | Yes | Portfolio returns (decimal). |
| `benchmark_returns` | `array` | Yes | Benchmark returns (decimal). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tracking_error_calculator",
  "arguments": {
    "portfolio_returns": [],
    "benchmark_returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tracking_error_calculator"`.
