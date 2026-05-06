---
skill: rwa_oracle_price_ladder_sanity_checker
category: crypto_rwa
description: Validates laddered price levels for order-book fed RWAs remain monotonic.
tier: free
inputs: payload
---

# Rwa Oracle Price Ladder Sanity Checker

## Description
Validates laddered price levels for order-book fed RWAs remain monotonic.

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
  "tool": "rwa_oracle_price_ladder_sanity_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_price_ladder_sanity_checker"`.
