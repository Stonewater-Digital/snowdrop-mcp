---
skill: dividend_reinstatement_detector
category: event_driven_trades
description: Screens for companies poised to restart dividends based on cash flow inflections and board language.
tier: free
inputs: none
---

# Dividend Reinstatement Detector

## Description
Screens for companies poised to restart dividends based on cash flow inflections and board language.

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
  "tool": "dividend_reinstatement_detector",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dividend_reinstatement_detector"`.
