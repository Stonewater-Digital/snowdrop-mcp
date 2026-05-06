---
skill: fibonacci_retracement
category: technical_analysis
description: Computes common Fibonacci retracement prices (23.6%, 38.2%, 50%, 61.8%, 78.6%) for trend analysis.
tier: free
inputs: swing_high, swing_low, trend
---

# Fibonacci Retracement

## Description
Computes common Fibonacci retracement prices (23.6%, 38.2%, 50%, 61.8%, 78.6%) for trend analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `swing_high` | `number` | Yes | Recent swing high price. |
| `swing_low` | `number` | Yes | Recent swing low price. |
| `trend` | `string` | Yes | Direction of move being measured: up or down. |
| `current_price` | `number` | No | Optional current price to identify nearest retracement. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fibonacci_retracement",
  "arguments": {
    "swing_high": 0,
    "swing_low": 0,
    "trend": "<trend>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fibonacci_retracement"`.
