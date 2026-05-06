---
skill: resampled_efficient_frontier
category: portfolio_construction
description: Applies Michaud resampling by bootstrapping mean-variance inputs and averaging allocations to produce confidence bands for the efficient frontier.
tier: free
inputs: expected_returns, covariance_matrix
---

# Resampled Efficient Frontier

## Description
Applies Michaud resampling by bootstrapping mean-variance inputs and averaging allocations to produce confidence bands for the efficient frontier.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expected_returns` | `array` | Yes | Vector of expected returns (decimal) for each asset. |
| `covariance_matrix` | `array` | Yes | Positive-definite covariance matrix corresponding to expected returns. |
| `sample_runs` | `integer` | No | Number of bootstrap draws for resampling (default 250). |
| `frontier_points` | `integer` | No | Granularity of frontier target returns (default 10). |
| `confidence_level` | `number` | No | Confidence level for dispersion bands (default 0.9). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "resampled_efficient_frontier",
  "arguments": {
    "expected_returns": [],
    "covariance_matrix": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "resampled_efficient_frontier"`.
