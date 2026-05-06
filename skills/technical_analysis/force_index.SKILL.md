---
skill: force_index
category: technical_analysis
description: Applies Elder's Force Index with optional EMA smoothing to detect bullish or bearish thrusts.
tier: free
inputs: closes, volumes, ema_period
---

# Force Index

## Description
Applies Elder's Force Index with optional EMA smoothing to detect bullish or bearish thrusts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `closes` | `array` | Yes | Close prices. |
| `volumes` | `array` | Yes | Volume per bar. |
| `ema_period` | `integer` | Yes | EMA smoothing period (default 13). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "force_index",
  "arguments": {
    "closes": [],
    "volumes": [],
    "ema_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "force_index"`.
