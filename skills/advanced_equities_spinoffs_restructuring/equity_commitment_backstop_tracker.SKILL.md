---
skill: equity_commitment_backstop_tracker
category: advanced_equities_spinoffs_restructuring
description: Monitors rights backstop size, participants, and pricing fairness.
tier: free
inputs: none
---

# Equity Commitment Backstop Tracker

## Description
Monitors rights backstop size, participants, and pricing fairness.

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
  "tool": "equity_commitment_backstop_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "equity_commitment_backstop_tracker"`.
