---
skill: elder_ray_index
category: technical_analysis
description: Computes Elder-Ray Bull/Bear Power relative to an EMA trend baseline.
tier: free
inputs: highs, lows, closes, ema_period
---

# Elder Ray Index

## Description
Computes Elder-Ray Bull/Bear Power relative to an EMA trend baseline.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `ema_period` | `integer` | Yes | EMA period (default 13). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "elder_ray_index",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "ema_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "elder_ray_index"`.
