---
skill: options_open_interest_rotation_monitor
category: derivatives_volatility
description: Identifies large OI rolls indicating positioning shifts.
tier: free
inputs: none
---

# Options Open Interest Rotation Monitor

## Description
Identifies large OI rolls indicating positioning shifts.

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
  "tool": "options_open_interest_rotation_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_open_interest_rotation_monitor"`.
