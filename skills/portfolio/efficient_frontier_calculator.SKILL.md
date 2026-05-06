---
skill: efficient_frontier_calculator
category: portfolio
description: Generates random portfolios to approximate the efficient frontier and key points.
tier: free
inputs: assets, correlation_matrix
---

# Efficient Frontier Calculator

## Description
Generates random portfolios to approximate the efficient frontier and key points.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assets` | `array` | Yes |  |
| `correlation_matrix` | `object` | Yes |  |
| `num_portfolios` | `integer` | No |  |
| `risk_free_rate` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "efficient_frontier_calculator",
  "arguments": {
    "assets": [],
    "correlation_matrix": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "efficient_frontier_calculator"`.
