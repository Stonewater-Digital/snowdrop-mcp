---
skill: rwa_oracle_treasury_curve_reconciler
category: crypto_rwa
description: Compares oracle Treasury curves with FRED benchmarks to ensure discount factors match.
tier: free
inputs: none
---

# Rwa Oracle Treasury Curve Reconciler

## Description
Compares oracle Treasury curves with FRED benchmarks to ensure discount factors match.

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
  "tool": "rwa_oracle_treasury_curve_reconciler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_treasury_curve_reconciler"`.
