---
skill: real_asset_correlation_matrix
category: alternative_investments
description: Computes Pearson correlations across provided asset return series and compares tail-period correlations to detect crisis regimes. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: return_series, crisis_threshold
---

# Real Asset Correlation Matrix

## Description
Computes Pearson correlations across provided real asset return series and compares full-period to tail-period correlations to detect crisis regime correlation shifts. Useful for portfolio diversification analysis. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `return_series` | `object` | Yes | Dict mapping asset name to list of periodic returns (e.g. {"farmland": [...], "infrastructure": [...]}). |
| `crisis_threshold` | `number` | Yes | Return threshold below which a period is classified as a crisis (e.g. -0.05 for -5%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "real_asset_correlation_matrix",
  "arguments": {
    "return_series": {
      "farmland": [0.03, 0.02, 0.04, -0.01, 0.03],
      "infrastructure": [0.04, 0.03, -0.02, 0.05, 0.04],
      "timber": [0.02, 0.01, 0.03, -0.03, 0.02]
    },
    "crisis_threshold": -0.02
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "real_asset_correlation_matrix"`.
