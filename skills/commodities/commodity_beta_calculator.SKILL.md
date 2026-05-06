---
skill: commodity_beta_calculator
category: commodities
description: Estimates OLS beta, alpha, correlation, and annualized tracking error of a commodity return series against a benchmark. Returns are in decimal form (e.g.
tier: free
inputs: commodity_returns, benchmark_returns
---

# Commodity Beta Calculator

## Description
Estimates OLS beta, alpha, correlation, and annualized tracking error of a commodity return series against a benchmark. Returns are in decimal form (e.g. 0.02 = 2%).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `commodity_returns` | `array` | Yes | Periodic return series for the commodity (decimal, e.g. 0.01 = 1%). |
| `benchmark_returns` | `array` | Yes | Periodic return series for the benchmark (same length and frequency). |
| `periods_per_year` | `number` | No | Number of return periods per year for annualization (252=daily, 12=monthly). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "commodity_beta_calculator",
  "arguments": {
    "commodity_returns": [],
    "benchmark_returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commodity_beta_calculator"`.
