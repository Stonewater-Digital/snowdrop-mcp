---
skill: moving_average_ribbon
category: technical_analysis
description: Calculates SMA values for multiple periods to form a ribbon and detect trend/squeeze signals.
tier: free
inputs: prices, periods
---

# Moving Average Ribbon

## Description
Calculates SMA values for multiple periods to form a ribbon and detect trend/squeeze signals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price series. |
| `periods` | `array` | Yes | List of SMA periods (e.g., [10,20,30...]). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moving_average_ribbon",
  "arguments": {
    "prices": [],
    "periods": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moving_average_ribbon"`.
