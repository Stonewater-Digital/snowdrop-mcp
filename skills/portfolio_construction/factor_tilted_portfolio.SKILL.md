---
skill: factor_tilted_portfolio
category: portfolio_construction
description: Implements Barra-style factor tilting by solving a constrained least-squares system to match target factor shifts while minimizing benchmark deviation.
tier: free
inputs: benchmark_weights, factor_exposures, target_shifts
---

# Factor Tilted Portfolio

## Description
Implements Barra-style factor tilting by solving a constrained least-squares system to match target factor shifts while minimizing benchmark deviation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `benchmark_weights` | `array` | Yes | Benchmark constituent weights summing to unity. |
| `factor_exposures` | `object` | Yes | Factor exposure matrix keyed by factor name with values per asset. |
| `target_shifts` | `object` | Yes | Desired exposure change for each factor (positive = overweight). |
| `covariance_matrix` | `array` | No | Optional covariance matrix for tracking error estimation. |
| `max_active_weight` | `number` | No | Absolute cap on deviation from benchmark for each asset (default 0.05). |
| `regularization` | `number` | No | Ridge penalty applied to weight changes (default 1e-4). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "factor_tilted_portfolio",
  "arguments": {
    "benchmark_weights": [],
    "factor_exposures": {},
    "target_shifts": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "factor_tilted_portfolio"`.
