---
skill: sma_calculator
category: technical_analysis
description: Calculates rolling simple moving averages to identify price alignment with key trend periods.
tier: free
inputs: prices, period
---

# Sma Calculator

## Description
Calculates rolling simple moving averages to identify price alignment with key trend periods.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Chronological list of closing prices (oldest first). |
| `period` | `integer` | Yes | Primary SMA lookback period (e.g., 20). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sma_calculator",
  "arguments": {
    "prices": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sma_calculator"`.
