---
skill: fund_benchmark_comparison
category: fund_admin
description: Compares a fund's KPIs to benchmark values and flags underperformance. Returns per-metric deltas, beat/miss flags, and overall hit rate.
tier: premium
inputs: fund_metrics, benchmark_metrics
---

# Fund Benchmark Comparison

## Description
Compares a fund's KPIs to benchmark values and flags underperformance. Returns per-metric deltas, beat/miss flags, and overall hit rate. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| fund_metrics | object | Yes | Dictionary of the fund's actual KPI values keyed by metric name (e.g. `{"irr": 14.2, "moic": 1.9, "dpi": 0.7}`) |
| benchmark_metrics | object | Yes | Dictionary of benchmark or peer-median KPI values keyed by the same metric names for comparison |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fund_benchmark_comparison",
  "arguments": {
    "fund_metrics": {
      "irr": 14.2,
      "moic": 1.9,
      "dpi": 0.72,
      "tvpi": 1.85
    },
    "benchmark_metrics": {
      "irr": 12.5,
      "moic": 1.75,
      "dpi": 0.80,
      "tvpi": 1.70
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_benchmark_comparison"`.
