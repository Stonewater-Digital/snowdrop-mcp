---
skill: cds_curve_steepener_analyzer
category: credit_default_swaps
description: Evaluates CDS curve slope and roll yield for steepener trades.
tier: free
inputs: tenors_years, spreads_bps
---

# Cds Curve Steepener Analyzer

## Description
Evaluates CDS curve slope and roll yield for steepener trades.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tenors_years` | `array` | Yes |  |
| `spreads_bps` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_curve_steepener_analyzer",
  "arguments": {
    "tenors_years": [],
    "spreads_bps": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_curve_steepener_analyzer"`.
