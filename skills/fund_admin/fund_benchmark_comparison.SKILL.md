---
skill: fund_benchmark_comparison
category: fund_admin
description: Compares a fund's KPIs to benchmark values and flags underperformance. Returns per-metric deltas, beat/miss flags, and overall hit rate.
tier: premium
inputs: none
---

# Fund Benchmark Comparison

## Description
Compares a fund's KPIs to benchmark values and flags underperformance. Returns per-metric deltas, beat/miss flags, and overall hit rate. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fund_benchmark_comparison",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_benchmark_comparison"`.
