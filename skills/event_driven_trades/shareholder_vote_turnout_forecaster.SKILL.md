---
skill: shareholder_vote_turnout_forecaster
category: event_driven_trades
description: Projects vote outcomes by modeling historical turnout, proxy advisor stances, and current register data.
tier: free
inputs: none
---

# Shareholder Vote Turnout Forecaster

## Description
Projects vote outcomes by modeling historical turnout, proxy advisor stances, and current register data.

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
  "tool": "shareholder_vote_turnout_forecaster",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "shareholder_vote_turnout_forecaster"`.
