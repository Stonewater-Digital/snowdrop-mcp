---
skill: token_burn_deflation
category: blockchain_analytics
description: Analyzes burn events vs emissions to classify token supply behavior.
tier: free
inputs: total_supply, circulating_supply, burn_events, annual_emission
---

# Token Burn Deflation

## Description
Analyzes burn events vs emissions to classify token supply behavior.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_supply` | `number` | Yes | Total supply minted |
| `circulating_supply` | `number` | Yes | Current circulating supply |
| `burn_events` | `array` | Yes | List of burn events {date, amount} |
| `annual_emission` | `number` | Yes | Tokens minted per year |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_burn_deflation",
  "arguments": {
    "total_supply": 0,
    "circulating_supply": 0,
    "burn_events": [],
    "annual_emission": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_burn_deflation"`.
