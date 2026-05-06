---
skill: vintage_year_benchmarking
category: fund_accounting
description: Benchmarks a private equity fund's performance against vintage-year peer data. Calculates the Public Market Equivalent (PME) ratio as fund_tvpi / benchmark_median_tvpi, determines quartile rank (Q1=top), and produces a side-by-side comparison table for TVPI, DPI, and IRR.
tier: premium
inputs: none
---

# Vintage Year Benchmarking

## Description
Benchmarks a private equity fund's performance against vintage-year peer data. Calculates the Public Market Equivalent (PME) ratio as fund_tvpi / benchmark_median_tvpi, determines quartile rank (Q1=top), and produces a side-by-side comparison table for TVPI, DPI, and IRR. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "vintage_year_benchmarking",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vintage_year_benchmarking"`.
