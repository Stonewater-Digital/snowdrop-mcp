---
skill: supervoting_conversion_timer
category: advanced_equities_spinoffs_restructuring
description: Tracks super-voting share collapse triggers to anticipate governance shifts.
tier: free
inputs: none
---

# Supervoting Conversion Timer

## Description
Tracks super-voting share collapse triggers to anticipate governance shifts.

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
  "tool": "supervoting_conversion_timer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "supervoting_conversion_timer"`.
