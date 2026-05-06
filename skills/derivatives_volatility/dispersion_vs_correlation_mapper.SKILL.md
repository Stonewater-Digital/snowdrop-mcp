---
skill: dispersion_vs_correlation_mapper
category: derivatives_volatility
description: Relates single-name vol to index implied correlation for dispersion plays.
tier: free
inputs: none
---

# Dispersion Vs Correlation Mapper

## Description
Relates single-name vol to index implied correlation for dispersion plays.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tickers` | `array` | No | Tickers or identifiers relevant to the analysis focus. |
| `lookback_days` | `integer` | No | Historical window (days) for synthetic / free-data calculations. |
| `analysis_notes` | `string` | No | Optional qualitative context to embed in the response. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dispersion_vs_correlation_mapper",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dispersion_vs_correlation_mapper"`.
