---
skill: rwa_oracle_forestry_land_value_checker
category: crypto_rwa
description: Compares forestry land appraisal indexes with oracle quotes backing timber tokens.
tier: free
inputs: payload
---

# Rwa Oracle Forestry Land Value Checker

## Description
Compares forestry land appraisal indexes with oracle quotes backing timber tokens.

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
  "tool": "rwa_oracle_forestry_land_value_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_forestry_land_value_checker"`.
