---
skill: real_asset_correlation_matrix
category: alternative_investments
description: Computes Pearson correlations across provided asset return series and compares tail-period correlations to detect crisis regimes. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Real Asset Correlation Matrix

## Description
Computes Pearson correlations across provided asset return series and compares tail-period correlations to detect crisis regimes. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "real_asset_correlation_matrix",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "real_asset_correlation_matrix"`.
