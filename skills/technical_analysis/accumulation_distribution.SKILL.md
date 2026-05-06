---
skill: accumulation_distribution
category: technical_analysis
description: Calculates accumulation/distribution via money flow multiplier and cumulative volume flow.
tier: free
inputs: highs, lows, closes, volumes
---

# Accumulation Distribution

## Description
Calculates accumulation/distribution via money flow multiplier and cumulative volume flow.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `volumes` | `array` | Yes | Volume per period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "accumulation_distribution",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "volumes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "accumulation_distribution"`.
