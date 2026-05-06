---
skill: tracking_error_calculator
category: portfolio
description: Calculates the annualized tracking error (standard deviation of active returns) between a portfolio and its benchmark.
tier: free
inputs: portfolio_returns, benchmark_returns
---

# Tracking Error Calculator

## Description
Calculates the annualized tracking error (standard deviation of active returns) between a portfolio and its benchmark.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_returns` | `array` | Yes | List of portfolio periodic returns. |
| `benchmark_returns` | `array` | Yes | List of benchmark periodic returns (same length). |

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
