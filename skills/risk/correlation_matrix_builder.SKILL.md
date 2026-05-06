---
skill: correlation_matrix_builder
category: risk
description: Build Pearson correlation matrices from asset price histories.
tier: free
inputs: price_series
---

# Correlation Matrix Builder

## Description
Computes pairwise Pearson correlation coefficients between assets using their historical price series. Internally converts prices to daily returns before computing correlations, so raw price levels (not pre-computed returns) should be provided. Returns the full N x N correlation matrix, a list of highly correlated pairs (correlation >= 0.8), and a list of inversely correlated pairs (correlation <= -0.5). Requires at least two assets and at least two price points per asset. Use for portfolio diversification analysis and identifying concentration risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `price_series` | `object` | Yes | Dictionary mapping asset ticker strings to arrays of historical prices as numbers. Each array must have at least 2 price points. Example: `{"BTC": [40000, 41000, ...], "ETH": [2800, 2850, ...]}`. At least 2 assets required. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

Data fields: `matrix` (nested object of pairwise correlations), `highly_correlated` (array of pair objects with correlation >= 0.8), `inversely_correlated` (array of pair objects with correlation <= -0.5).

## Example
```json
{
  "tool": "correlation_matrix_builder",
  "arguments": {
    "price_series": {
      "BTC": [40000, 41200, 39800, 42500, 43000, 41800, 44000],
      "ETH": [2800, 2870, 2760, 2950, 2990, 2880, 3050],
      "SOL": [120, 118, 115, 125, 130, 122, 135]
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "correlation_matrix_builder"`.
