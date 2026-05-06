---
skill: drawdown_constrained_optimizer
category: portfolio_construction
description: Performs scenario search across asset paths to maximize expected return while enforcing a user-specified maximum drawdown limit consistent with UCITS risk budgeting guidance.
tier: free
inputs: asset_paths, drawdown_limit
---

# Drawdown Constrained Optimizer

## Description
Performs scenario search across asset paths to maximize expected return while enforcing a user-specified maximum drawdown limit consistent with UCITS risk budgeting guidance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_paths` | `object` | Yes | Dictionary mapping asset to a path of periodic returns (decimal). |
| `drawdown_limit` | `number` | Yes | Maximum allowable drawdown in decimal terms (e.g., 0.2 for 20%). |
| `simulations` | `integer` | No | Number of random weight draws for search (default 2000). |
| `seed` | `integer` | No | Random seed for reproducibility. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "drawdown_constrained_optimizer",
  "arguments": {
    "asset_paths": {},
    "drawdown_limit": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "drawdown_constrained_optimizer"`.
