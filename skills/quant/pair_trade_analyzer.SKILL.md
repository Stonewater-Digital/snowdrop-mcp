---
skill: pair_trade_analyzer
category: quant
description: Computes ratio z-scores, correlation, OLS half-life, and trade signals for price pairs.
tier: free
inputs: series_a, series_b
---

# Pair Trade Analyzer

## Description
Computes ratio z-scores, correlation, OLS half-life, and trade signals for price pairs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `series_a` | `array` | Yes | Price series for asset A (>= 10 observations). |
| `series_b` | `array` | Yes | Price series for asset B (same length as series_a). |
| `labels` | `array` | No | Optional date labels. |
| `entry_z` | `number` | No | Z-score threshold for entry. |
| `exit_z` | `number` | No | Z-score threshold for exit. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pair_trade_analyzer",
  "arguments": {
    "series_a": [],
    "series_b": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pair_trade_analyzer"`.
