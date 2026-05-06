---
skill: smart_contract_liquidation_waterfall_checker
category: crypto_rwa
description: Validates liquidation waterfalls respect seniority rules across tranches.
tier: free
inputs: payload
---

# Smart Contract Liquidation Waterfall Checker

## Description
Validates liquidation waterfalls respect seniority rules across tranches.

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
  "tool": "smart_contract_liquidation_waterfall_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_liquidation_waterfall_checker"`.
