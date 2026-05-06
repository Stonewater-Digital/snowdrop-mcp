---
skill: mean_cvar_optimizer
category: portfolio_construction
description: Minimizes portfolio conditional VaR via Rockafellar-Uryasev subgradient descent with simplex projection and optional target return constraint.
tier: free
inputs: scenario_returns, confidence_level
---

# Mean Cvar Optimizer

## Description
Minimizes portfolio conditional VaR via Rockafellar-Uryasev subgradient descent with simplex projection and optional target return constraint.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `scenario_returns` | `array` | Yes | Matrix of scenario returns (rows=scenarios, cols=assets) in decimals. |
| `confidence_level` | `number` | Yes | Tail confidence (e.g., 0.95) used for VaR / CVaR calculation. |
| `target_return` | `number` | No | Optional minimum expected return target; penalty enforced if breached. |
| `min_weight` | `number` | No | Lower bound for each asset weight (default 0). |
| `max_weight` | `number` | No | Upper bound per asset (default 1). |
| `learning_rate` | `number` | No | Gradient step size for CVaR minimization (default 0.05). |
| `iterations` | `integer` | No | Number of gradient iterations (default 250). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mean_cvar_optimizer",
  "arguments": {
    "scenario_returns": [],
    "confidence_level": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mean_cvar_optimizer"`.
