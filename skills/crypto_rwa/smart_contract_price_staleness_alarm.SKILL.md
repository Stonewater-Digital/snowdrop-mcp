---
skill: smart_contract_price_staleness_alarm
category: crypto_rwa
description: Calculates price feed staleness windows and raises alerts when data age exceeds limits.
tier: free
inputs: payload
---

# Smart Contract Price Staleness Alarm

## Description
Calculates price feed staleness windows and raises alerts when data age exceeds limits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "smart_contract_price_staleness_alarm",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_price_staleness_alarm"`.
