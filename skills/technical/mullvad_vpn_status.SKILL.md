---
skill: mullvad_vpn_status
category: technical
description: Constructs Mullvad account queries and summarizes connection health.
tier: free
inputs: none
---

# Mullvad Vpn Status

## Description
Constructs Mullvad account queries and summarizes connection health.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `api_response` | `object` | No | Optional Mullvad response. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mullvad_vpn_status",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mullvad_vpn_status"`.
