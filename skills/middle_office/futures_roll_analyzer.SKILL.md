---
skill: futures_roll_analyzer
category: middle_office
description: Evaluates roll cost, carry, and recommendation for futures positions.
tier: free
inputs: front_price, back_price, days_to_expiry, position_size, contract_value
---

# Futures Roll Analyzer

## Description
Evaluates roll cost, carry, and recommendation for futures positions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `front_price` | `number` | Yes |  |
| `back_price` | `number` | Yes |  |
| `days_to_expiry` | `integer` | Yes |  |
| `position_size` | `number` | Yes |  |
| `contract_value` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "futures_roll_analyzer",
  "arguments": {
    "front_price": 0,
    "back_price": 0,
    "days_to_expiry": 0,
    "position_size": 0,
    "contract_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "futures_roll_analyzer"`.
