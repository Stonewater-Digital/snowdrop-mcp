---
skill: rwa_yield_spread_analyzer
category: rwa_tokenization
description: Computes yield spreads relative to benchmark bonds and adjusts for duration risk.
tier: free
inputs: token_yield_pct, benchmark_yield_pct, duration_years
---

# Rwa Yield Spread Analyzer

## Description
Computes yield spreads relative to benchmark bonds and adjusts for duration risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `token_yield_pct` | `number` | Yes | Yield of the RWA token |
| `benchmark_yield_pct` | `number` | Yes | Comparable benchmark yield |
| `duration_years` | `number` | Yes | Effective duration |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_yield_spread_analyzer",
  "arguments": {
    "token_yield_pct": 0,
    "benchmark_yield_pct": 0,
    "duration_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_yield_spread_analyzer"`.
