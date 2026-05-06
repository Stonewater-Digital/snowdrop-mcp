---
skill: token_unlock_scheduler
category: blockchain_analytics
description: Analyzes vesting events to quantify unlock pace, dilution, and sell pressure windows.
tier: free
inputs: unlock_events, circulating_supply, price
---

# Token Unlock Scheduler

## Description
Analyzes vesting events to quantify unlock pace, dilution, and sell pressure windows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `unlock_events` | `array` | Yes | Scheduled unlocks [{date, amount, category}]. |
| `circulating_supply` | `number` | Yes | Current circulating supply. |
| `price` | `number` | Yes | Current token price in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_unlock_scheduler",
  "arguments": {
    "unlock_events": [],
    "circulating_supply": 0,
    "price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_unlock_scheduler"`.
