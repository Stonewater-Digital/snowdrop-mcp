---
skill: statistical_arbitrage_zscore
category: alternative_investments
description: Performs OLS regression of X on Y to compute hedge ratio, z-score, and Ornstein-Uhlenbeck half-life for pairs trading. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: series_x, series_y, entry_z, exit_z
---

# Statistical Arbitrage Z-Score

## Description
Performs OLS regression of X on Y to compute hedge ratio, spread z-score, and Ornstein-Uhlenbeck mean-reversion half-life for pairs trading. Identifies entry and exit signals based on z-score thresholds. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `series_x` | `array` | Yes | Price series for asset X (the hedge leg). |
| `series_y` | `array` | Yes | Price series for asset Y (the long/short leg). Must be same length as series_x. |
| `entry_z` | `number` | Yes | Z-score threshold to trigger entry (e.g. 2.0). |
| `exit_z` | `number` | Yes | Z-score threshold to trigger exit / mean reversion (e.g. 0.5). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "statistical_arbitrage_zscore",
  "arguments": {
    "series_x": [50.1, 50.5, 51.0, 51.2, 50.8, 51.5, 52.0],
    "series_y": [100.2, 101.0, 101.8, 102.5, 101.0, 103.0, 104.2],
    "entry_z": 2.0,
    "exit_z": 0.5
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "statistical_arbitrage_zscore"`.
