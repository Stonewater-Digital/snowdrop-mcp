---
skill: expected_shortfall_decomposition
category: quantitative_risk
description: Basel III ES attribution by computing conditional tail expectations and factor contributions.
tier: free
inputs: portfolio_pnl, factor_exposures, factor_returns
---

# Expected Shortfall Decomposition

## Description
Basel III ES attribution by computing conditional tail expectations and factor contributions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_pnl` | `array` | Yes | Historical or simulated P&L series in base currency. |
| `factor_exposures` | `object` | Yes | Factor betas or sensitivities keyed by factor name. |
| `factor_returns` | `object` | Yes | Dictionary of factor return series aligned with portfolio P&L observations. |
| `confidence_level` | `number` | No | Tail probability threshold (default 0.975 as per FRTB). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "expected_shortfall_decomposition",
  "arguments": {
    "portfolio_pnl": [],
    "factor_exposures": {},
    "factor_returns": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "expected_shortfall_decomposition"`.
