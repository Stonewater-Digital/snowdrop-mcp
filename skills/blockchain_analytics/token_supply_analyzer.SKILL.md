---
skill: token_supply_analyzer
category: blockchain_analytics
description: Analyzes emission schedules and burn rates to forecast supply paths and inflation.
tier: free
inputs: current_supply, max_supply, emission_schedule, burn_rate
---

# Token Supply Analyzer

## Description
Analyzes emission schedules and burn rates to forecast supply paths and inflation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_supply` | `number` | Yes | Circulating supply today. |
| `max_supply` | `number` | Yes | Maximum supply cap. |
| `emission_schedule` | `array` | Yes | Future annual emissions [{year, new_tokens}]. |
| `burn_rate` | `number` | Yes | Annual burn rate in tokens. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_supply_analyzer",
  "arguments": {
    "current_supply": 0,
    "max_supply": 0,
    "emission_schedule": [],
    "burn_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_supply_analyzer"`.
