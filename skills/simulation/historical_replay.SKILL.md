---
skill: historical_replay
category: simulation
description: Applies historical drawdowns to portfolio weights to estimate losses.
tier: free
inputs: portfolio, historical_period
---

# Historical Replay

## Description
Applies historical drawdowns to portfolio weights to estimate losses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio` | `array` | Yes |  |
| `historical_period` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "historical_replay",
  "arguments": {
    "portfolio": [],
    "historical_period": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "historical_replay"`.
