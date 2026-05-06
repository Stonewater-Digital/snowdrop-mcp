---
skill: rwa_oracle_real_estate_sale_comp_checker
category: crypto_rwa
description: Confirms sale comparables feeding residential tokens align with MLS data.
tier: free
inputs: payload
---

# Rwa Oracle Real Estate Sale Comp Checker

## Description
Confirms sale comparables feeding residential tokens align with MLS data.

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
  "tool": "rwa_oracle_real_estate_sale_comp_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_real_estate_sale_comp_checker"`.
