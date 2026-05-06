---
skill: correlation_matrix_builder
category: market_analytics
description: Computes Pearson correlations across multiple return series to assess diversification.
tier: free
inputs: return_series
---

# Correlation Matrix Builder

## Description
Computes Pearson correlations across multiple return series to assess diversification.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `return_series` | `object` | Yes | Mapping of asset name to return list. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "correlation_matrix_builder",
  "arguments": {
    "return_series": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "correlation_matrix_builder"`.
