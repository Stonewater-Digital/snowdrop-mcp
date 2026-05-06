---
skill: ulcer_index
category: technical_analysis
description: Computes the Ulcer Index and related drawdown metrics to capture downside pain.
tier: free
inputs: prices, period
---

# Ulcer Index

## Description
Computes the Ulcer Index and related drawdown metrics to capture downside pain.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price or NAV series. |
| `period` | `integer` | Yes | Lookback for drawdown window. |
| `risk_free_rate` | `number` | No | Optional annual risk-free rate in percent. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ulcer_index",
  "arguments": {
    "prices": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ulcer_index"`.
