---
skill: performance_attribution_tool
category: middle_office
description: Performs allocation, selection, and interaction attribution vs a benchmark.
tier: free
inputs: portfolio_weights, benchmark_weights, portfolio_returns, benchmark_returns
---

# Performance Attribution Tool

## Description
Performs allocation, selection, and interaction attribution vs a benchmark.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_weights` | `object` | Yes |  |
| `benchmark_weights` | `object` | Yes |  |
| `portfolio_returns` | `object` | Yes |  |
| `benchmark_returns` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "performance_attribution_tool",
  "arguments": {
    "portfolio_weights": {},
    "benchmark_weights": {},
    "portfolio_returns": {},
    "benchmark_returns": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "performance_attribution_tool"`.
