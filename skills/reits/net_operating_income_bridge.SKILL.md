---
skill: net_operating_income_bridge
category: reits
description: Builds an NOI bridge showing contributions from volume, rate, occupancy, and opex.
tier: free
inputs: prior_noi, volume_change, rate_change, occupancy_change, expense_change
---

# Net Operating Income Bridge

## Description
Builds an NOI bridge showing contributions from volume, rate, occupancy, and opex.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prior_noi` | `number` | Yes |  |
| `volume_change` | `number` | Yes |  |
| `rate_change` | `number` | Yes |  |
| `occupancy_change` | `number` | Yes |  |
| `expense_change` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "net_operating_income_bridge",
  "arguments": {
    "prior_noi": 0,
    "volume_change": 0,
    "rate_change": 0,
    "occupancy_change": 0,
    "expense_change": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "net_operating_income_bridge"`.
