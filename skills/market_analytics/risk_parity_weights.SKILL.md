---
skill: risk_parity_weights
category: market_analytics
description: Approximates risk-parity allocation via inverse volatility and reports risk contributions.
tier: free
inputs: returns_matrix, asset_names
---

# Risk Parity Weights

## Description
Approximates risk-parity allocation via inverse volatility and reports risk contributions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns_matrix` | `array` | Yes | List of asset return series. |
| `asset_names` | `array` | Yes | Names corresponding to each asset. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "risk_parity_weights",
  "arguments": {
    "returns_matrix": [],
    "asset_names": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "risk_parity_weights"`.
