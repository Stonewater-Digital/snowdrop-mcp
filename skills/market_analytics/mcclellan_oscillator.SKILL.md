---
skill: mcclellan_oscillator
category: market_analytics
description: Calculates McClellan Oscillator (EMA19-EMA39) and the Summation Index to gauge breadth thrusts.
tier: free
inputs: advances, declines
---

# Mcclellan Oscillator

## Description
Calculates McClellan Oscillator (EMA19-EMA39) and the Summation Index to gauge breadth thrusts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `advances` | `array` | Yes | Advancing issues. |
| `declines` | `array` | Yes | Declining issues. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mcclellan_oscillator",
  "arguments": {
    "advances": [],
    "declines": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mcclellan_oscillator"`.
