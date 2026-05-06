---
skill: earnings_gap_playbook
category: event_driven_trades
description: Quantifies historical post-earnings gaps vs. implied move to flag asymmetric setups using free price feeds.
tier: free
inputs: none
---

# Earnings Gap Playbook

## Description
Quantifies historical post-earnings gaps vs. implied move to flag asymmetric setups using free price feeds.

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
  "tool": "earnings_gap_playbook",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "earnings_gap_playbook"`.
