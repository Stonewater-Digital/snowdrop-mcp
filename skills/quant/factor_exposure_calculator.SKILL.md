---
skill: factor_exposure_calculator
category: quant
description: Calculates factor betas and contribution to variance per factor.
tier: free
inputs: asset_returns, factor_returns
---

# Factor Exposure Calculator

## Description
Calculates factor betas and contribution to variance per factor.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_returns` | `array` | Yes |  |
| `factor_returns` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "factor_exposure_calculator",
  "arguments": {
    "asset_returns": [],
    "factor_returns": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "factor_exposure_calculator"`.
