---
skill: regime_aware_allocator
category: portfolio_construction
description: Fits a two-state hidden Markov model to realized returns and allocates according to risk-on/risk-off regime targets similar to Norges Bank's conditional allocation process.
tier: free
inputs: return_series, regime_allocations
---

# Regime Aware Allocator

## Description
Fits a two-state hidden Markov model to realized returns and allocates according to risk-on/risk-off regime targets similar to Norges Bank's conditional allocation process.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `return_series` | `array` | Yes | Chronological list of realized portfolio returns (decimal). |
| `regime_allocations` | `object` | Yes | Mapping of regime label to asset weight dictionary. |
| `transition_matrix` | `array` | No | 2x2 Markov transition matrix [[p00,p01],[p10,p11]]. |
| `observation_vol` | `number` | No | Scaling parameter for observation noise (default estimated from data). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "regime_aware_allocator",
  "arguments": {
    "return_series": [],
    "regime_allocations": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "regime_aware_allocator"`.
