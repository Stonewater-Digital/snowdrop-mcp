---
skill: dividend_capture_screener
category: advanced_equities_spinoffs_restructuring
description: Ranks capture setups using effective tax rate, borrow cost, and vol-adjusted decay.
tier: free
inputs: none
---

# Dividend Capture Screener

## Description
Ranks capture setups using effective tax rate, borrow cost, and vol-adjusted decay.

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
  "tool": "dividend_capture_screener",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dividend_capture_screener"`.
