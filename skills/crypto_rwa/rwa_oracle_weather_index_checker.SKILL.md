---
skill: rwa_oracle_weather_index_checker
category: crypto_rwa
description: Validates weather derivative indexes powering parametric insurance tokens.
tier: free
inputs: payload
---

# Rwa Oracle Weather Index Checker

## Description
Validates weather derivative indexes powering parametric insurance tokens.

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
  "tool": "rwa_oracle_weather_index_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_weather_index_checker"`.
