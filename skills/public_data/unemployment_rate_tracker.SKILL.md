---
skill: unemployment_rate_tracker
category: public_data
description: Track the US unemployment rate (BLS series LNS14000000). Uses BLS API if BLS_API_KEY is set, otherwise returns static recent data.
tier: free
inputs: none
---

# Unemployment Rate Tracker

## Description
Track the US unemployment rate (BLS series LNS14000000). Uses BLS API if BLS_API_KEY is set, otherwise returns static recent data.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `months` | `integer` | No | Number of recent months of data to return. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "unemployment_rate_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "unemployment_rate_tracker"`.
