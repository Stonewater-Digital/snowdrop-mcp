---
skill: sovereign_debt_yield_curve
category: sovereign
description: Computes sovereign bond spreads over US Treasuries, builds yield curves, and identifies inversions for Global South debt analysis.
tier: free
inputs: bonds, benchmark_yields
---

# Sovereign Debt Yield Curve

## Description
Computes sovereign bond spreads over US Treasuries, builds yield curves, and identifies inversions for Global South debt analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `bonds` | `array` | Yes | List of sovereign bond instruments |
| `benchmark_yields` | `object` | Yes | US Treasury yields keyed by maturity in years (e.g. {2: 4.5, 5: 4.3, 10: 4.2}) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sovereign_debt_yield_curve",
  "arguments": {
    "bonds": [],
    "benchmark_yields": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sovereign_debt_yield_curve"`.
