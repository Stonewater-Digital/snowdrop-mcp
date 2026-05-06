---
skill: black_litterman_optimizer
category: portfolio_construction
description: Computes Black-Litterman posterior returns and optimal weights using CAPM equilibrium implied returns blended with confidence-weighted views per He and Litterman (1999).
tier: free
inputs: market_weights, covariance_matrix, views
---

# Black Litterman Optimizer

## Description
Computes Black-Litterman posterior returns and optimal weights using CAPM equilibrium implied returns blended with confidence-weighted views per He and Litterman (1999).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `market_weights` | `array` | Yes | Market capitalization weights representing the equilibrium portfolio. |
| `covariance_matrix` | `array` | Yes | Positive-definite covariance matrix of asset returns (decimal). |
| `views` | `array` | Yes | List of views, each with assets dict (asset->exposure), view_return, and confidence (0-1). |
| `risk_aversion` | `number` | No | Risk aversion (lambda) typically estimated from market Sharpe (default 3). |
| `tau` | `number` | No | Scalar scaling prior uncertainty; standard BL uses small value like 0.05. |
| `asset_labels` | `array` | No | Optional labels for assets; defaults to indices. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "black_litterman_optimizer",
  "arguments": {
    "market_weights": [],
    "covariance_matrix": [],
    "views": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "black_litterman_optimizer"`.
