---
skill: performance_attribution
category: attribution
description: Decomposes active return into allocation, selection, and interaction components.
tier: free
inputs: portfolio_weights, portfolio_returns, benchmark_weights, benchmark_returns
---

# Performance Attribution

## Description
Decomposes active return into allocation, selection, and interaction components.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_weights` | `object` | Yes |  |
| `portfolio_returns` | `object` | Yes |  |
| `benchmark_weights` | `object` | Yes |  |
| `benchmark_returns` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "performance_attribution",
  "arguments": {
    "portfolio_weights": {},
    "portfolio_returns": {},
    "benchmark_weights": {},
    "benchmark_returns": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "performance_attribution"`.
