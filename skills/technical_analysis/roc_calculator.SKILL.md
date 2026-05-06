---
skill: roc_calculator
category: technical_analysis
description: Computes percentage rate of change and optional SMA smoothing to track acceleration.
tier: free
inputs: prices, period
---

# Roc Calculator

## Description
Computes percentage rate of change and optional SMA smoothing to track acceleration.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price list (oldest first). |
| `period` | `integer` | Yes | Lookback used for ROC (e.g., 12). |
| `smoothing_period` | `integer` | No | Optional SMA smoothing length for ROC. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "roc_calculator",
  "arguments": {
    "prices": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "roc_calculator"`.
