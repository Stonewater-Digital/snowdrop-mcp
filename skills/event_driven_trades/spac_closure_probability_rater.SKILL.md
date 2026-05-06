---
skill: spac_closure_probability_rater
category: event_driven_trades
description: Scores SPAC deals using redemption levels, sponsor incentives, and regulatory risk.
tier: free
inputs: none
---

# Spac Closure Probability Rater

## Description
Scores SPAC deals using redemption levels, sponsor incentives, and regulatory risk.

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
  "tool": "spac_closure_probability_rater",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "spac_closure_probability_rater"`.
