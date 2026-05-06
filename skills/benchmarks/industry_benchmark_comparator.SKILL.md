---
skill: industry_benchmark_comparator
category: benchmarks
description: Ranks Snowdrop metrics versus benchmark percentiles to highlight strengths and gaps.
tier: free
inputs: our_metrics, benchmarks
---

# Industry Benchmark Comparator

## Description
Ranks Snowdrop metrics versus benchmark percentiles to highlight strengths and gaps.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `our_metrics` | `object` | Yes |  |
| `benchmarks` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "industry_benchmark_comparator",
  "arguments": {
    "our_metrics": {},
    "benchmarks": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "industry_benchmark_comparator"`.
