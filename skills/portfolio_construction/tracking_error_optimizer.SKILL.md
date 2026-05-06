---
skill: tracking_error_optimizer
category: portfolio_construction
description: Minimizes ex-ante tracking error relative to the benchmark while enforcing factor exposure targets via Lagrangian solution of the quadratic optimization problem.
tier: free
inputs: benchmark_weights, covariance_matrix, factor_loadings, target_factor_exposure
---

# Tracking Error Optimizer

## Description
Minimizes ex-ante tracking error relative to the benchmark while enforcing factor exposure targets via Lagrangian solution of the quadratic optimization problem.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `benchmark_weights` | `array` | Yes | Benchmark weights summing to 1. |
| `covariance_matrix` | `array` | Yes | Return covariance matrix used for tracking error calculations. |
| `factor_loadings` | `object` | Yes | Matrix of factor loadings keyed by factor name. |
| `target_factor_exposure` | `object` | Yes | Desired total factor exposure for each factor after optimization. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tracking_error_optimizer",
  "arguments": {
    "benchmark_weights": [],
    "covariance_matrix": [],
    "factor_loadings": {},
    "target_factor_exposure": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tracking_error_optimizer"`.
