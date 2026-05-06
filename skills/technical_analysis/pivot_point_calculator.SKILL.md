---
skill: pivot_point_calculator
category: technical_analysis
description: Computes pivot points and support/resistance for Standard, Fibonacci, Woodie, Camarilla, and DeMark methods.
tier: free
inputs: high, low, close, open, method
---

# Pivot Point Calculator

## Description
Computes pivot points and support/resistance for Standard, Fibonacci, Woodie, Camarilla, and DeMark methods.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `high` | `number` | Yes | Prior high price. |
| `low` | `number` | Yes | Prior low price. |
| `close` | `number` | Yes | Prior close price. |
| `open` | `number` | Yes | Current/open price (required by Woodie, DeMark). |
| `method` | `string` | Yes | standard/fibonacci/woodie/camarilla/demark. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pivot_point_calculator",
  "arguments": {
    "high": 0,
    "low": 0,
    "close": 0,
    "open": 0,
    "method": "<method>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pivot_point_calculator"`.
