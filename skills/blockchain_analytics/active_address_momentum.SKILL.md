---
skill: active_address_momentum
category: blockchain_analytics
description: Analyzes daily active address series, applying momentum and Metcalfe's Law valuation hints.
tier: free
inputs: daily_active_addresses
---

# Active Address Momentum

## Description
Analyzes daily active address series, applying momentum and Metcalfe's Law valuation hints.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daily_active_addresses` | `array` | Yes | Time-ordered list of daily active addresses counts (>=14 data points recommended). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "active_address_momentum",
  "arguments": {
    "daily_active_addresses": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "active_address_momentum"`.
