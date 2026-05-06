---
skill: put_call_ratio
category: market_analytics
description: Tracks put/call ratios to identify fear vs greed sentiment zones.
tier: free
inputs: put_volume, call_volume, put_oi, call_oi
---

# Put Call Ratio

## Description
Tracks put/call ratios to identify fear vs greed sentiment zones.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `put_volume` | `number` | Yes | Daily put volume. |
| `call_volume` | `number` | Yes | Daily call volume. |
| `put_oi` | `number` | Yes | Put open interest. |
| `call_oi` | `number` | Yes | Call open interest. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "put_call_ratio",
  "arguments": {
    "put_volume": 0,
    "call_volume": 0,
    "put_oi": 0,
    "call_oi": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "put_call_ratio"`.
