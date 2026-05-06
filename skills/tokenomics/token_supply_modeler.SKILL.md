---
skill: token_supply_modeler
category: tokenomics
description: Projects circulating supply month by month with mint and burn events.
tier: free
inputs: initial_supply, mint_schedule, burn_events, months_to_project
---

# Token Supply Modeler

## Description
Projects circulating supply month by month with mint and burn events.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `initial_supply` | `number` | Yes |  |
| `mint_schedule` | `array` | Yes |  |
| `burn_events` | `array` | Yes |  |
| `months_to_project` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_supply_modeler",
  "arguments": {
    "initial_supply": 0,
    "mint_schedule": [],
    "burn_events": [],
    "months_to_project": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_supply_modeler"`.
