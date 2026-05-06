---
skill: statistical_arbitrage_signal
category: quant
description: Computes OLS hedge ratio, spread z-score, and entry/exit guidance for a pair.
tier: free
inputs: series_x, series_y
---

# Statistical Arbitrage Signal

## Description
Computes OLS hedge ratio, spread z-score, and entry/exit guidance for a pair.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `series_x` | `array` | Yes | Price series for asset X (>= 10 observations). |
| `series_y` | `array` | Yes | Price series for asset Y (same length as series_x). |
| `entry_z` | `number` | No | Z-score threshold for trade entry. |
| `exit_z` | `number` | No | Z-score threshold for trade exit. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "statistical_arbitrage_signal",
  "arguments": {
    "series_x": [],
    "series_y": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "statistical_arbitrage_signal"`.
