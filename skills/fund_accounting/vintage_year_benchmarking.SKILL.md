---
skill: vintage_year_benchmarking
category: fund_accounting
description: Benchmarks a private equity fund's performance against vintage-year peer data. Calculates the Public Market Equivalent (PME) ratio as fund_tvpi / benchmark_median_tvpi, determines quartile rank (Q1=top), and produces a side-by-side comparison table for TVPI, DPI, and IRR.
tier: premium
inputs: fund_metrics, benchmark_data, vintage_year
---

# Vintage Year Benchmarking

## Description
Benchmarks a private equity fund's performance against vintage-year peer data. Calculates the Public Market Equivalent (PME) ratio as fund_tvpi / benchmark_median_tvpi, determines quartile rank (Q1=top), and produces a side-by-side comparison table for TVPI, DPI, and IRR. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_metrics` | `object` | Yes | Performance metrics for the fund being benchmarked, with keys `net_irr`, `tvpi`, and `dpi`. |
| `benchmark_data` | `object` | Yes | Vintage-year peer benchmark data with quartile breakpoints for `tvpi`, `dpi`, and `irr` (keys: `q1`, `median`, `q3`). |
| `vintage_year` | `number` | Yes | Vintage year of the fund being benchmarked (e.g. `2020`). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vintage_year_benchmarking",
  "arguments": {
    "fund_metrics": {
      "net_irr": 0.187,
      "tvpi": 1.85,
      "dpi": 0.60
    },
    "benchmark_data": {
      "tvpi": {"q1": 1.90, "median": 1.55, "q3": 1.25},
      "dpi": {"q1": 0.70, "median": 0.45, "q3": 0.20},
      "irr": {"q1": 0.20, "median": 0.14, "q3": 0.08}
    },
    "vintage_year": 2020
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vintage_year_benchmarking"`.
