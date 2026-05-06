---
skill: poison_pill_trigger_analyzer
category: advanced_equities_spinoffs_restructuring
description: Tests thresholds and dilution math for outstanding shareholder rights plans.
tier: free
inputs: none
---

# Poison Pill Trigger Analyzer

## Description
Tests thresholds and dilution math for outstanding shareholder rights plans.

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
  "tool": "poison_pill_trigger_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "poison_pill_trigger_analyzer"`.
