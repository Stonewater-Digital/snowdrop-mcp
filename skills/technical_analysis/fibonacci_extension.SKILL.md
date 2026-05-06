---
skill: fibonacci_extension
category: technical_analysis
description: Computes Fibonacci extension projections (100%–261.8%) for trend continuation targets.
tier: free
inputs: swing_low, swing_high, retracement_low
---

# Fibonacci Extension

## Description
Computes Fibonacci extension projections (100%–261.8%) for trend continuation targets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `swing_low` | `number` | Yes | Low preceding the impulse move. |
| `swing_high` | `number` | Yes | High of the impulse move. |
| `retracement_low` | `number` | Yes | Low after retracement used as starting point for projections. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fibonacci_extension",
  "arguments": {
    "swing_low": 0,
    "swing_high": 0,
    "retracement_low": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fibonacci_extension"`.
