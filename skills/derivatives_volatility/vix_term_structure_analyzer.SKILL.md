---
skill: vix_term_structure_analyzer
category: derivatives_volatility
description: Charts VIX futures curve shape vs. realized vol to identify steepening trades.
tier: free
inputs: none
---

# Vix Term Structure Analyzer

## Description
Charts VIX futures curve shape vs. realized vol to identify steepening trades.

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
  "tool": "vix_term_structure_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vix_term_structure_analyzer"`.
