---
skill: proxy_fight_vote_pathfinder
category: event_driven_trades
description: Visualizes proxy math, record dates, and swing ballots for live contested meetings.
tier: free
inputs: none
---

# Proxy Fight Vote Pathfinder

## Description
Visualizes proxy math, record dates, and swing ballots for live contested meetings.

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
  "tool": "proxy_fight_vote_pathfinder",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "proxy_fight_vote_pathfinder"`.
