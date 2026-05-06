---
skill: rwa_treasury_maturity_schedule_guardian
category: crypto_rwa
description: Checks that token maturity ladders align with underlying Treasury maturity dates.
tier: free
inputs: payload
---

# Rwa Treasury Maturity Schedule Guardian

## Description
Checks that token maturity ladders align with underlying Treasury maturity dates.

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
  "tool": "rwa_treasury_maturity_schedule_guardian",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_maturity_schedule_guardian"`.
