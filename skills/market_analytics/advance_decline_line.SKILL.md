---
skill: advance_decline_line
category: market_analytics
description: Builds the cumulative Advance-Decline line and optional McClellan oscillator signal.
tier: free
inputs: advances, declines
---

# Advance Decline Line

## Description
Builds the cumulative Advance-Decline line and optional McClellan oscillator signal.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `advances` | `array` | Yes | Number of advancing issues per day. |
| `declines` | `array` | Yes | Number of declining issues per day. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "advance_decline_line",
  "arguments": {
    "advances": [],
    "declines": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "advance_decline_line"`.
