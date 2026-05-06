---
skill: information_ratio_calculator
category: portfolio
description: Calculates the information ratio, measuring a portfolio manager's ability to generate excess returns relative to a benchmark per unit of tracking error.
tier: free
inputs: portfolio_returns, benchmark_returns
---

# Information Ratio Calculator

## Description
Calculates the information ratio, measuring a portfolio manager's ability to generate excess returns relative to a benchmark per unit of tracking error.

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
  "tool": "information_ratio_calculator",
  "arguments": {
    "portfolio_returns": [],
    "benchmark_returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "information_ratio_calculator"`.
