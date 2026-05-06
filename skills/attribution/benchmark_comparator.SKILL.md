---
skill: benchmark_comparator
category: attribution
description: Calculates alpha, beta, tracking error, and rolling alpha versus benchmark.
tier: free
inputs: portfolio_values, benchmark_values, period_label
---

# Benchmark Comparator

## Description
Calculates alpha, beta, tracking error, and rolling alpha versus benchmark.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_values` | `array` | Yes |  |
| `benchmark_values` | `array` | Yes |  |
| `period_label` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "benchmark_comparator",
  "arguments": {
    "portfolio_values": [],
    "benchmark_values": [],
    "period_label": "<period_label>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "benchmark_comparator"`.
