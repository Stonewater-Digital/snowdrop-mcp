---
skill: mcp_discovery_beacon
category: technical
description: Packages a list of Snowdrop skills into MCP-compatible advertisement payloads and generates the beacon configuration required for periodic self-registration on the MCP network. Calculates a visibility score (0–100) based on skill count and category diversity.
tier: free
inputs: skills_to_advertise
---

# Mcp Discovery Beacon

## Description
Packages a list of Snowdrop skills into MCP-compatible advertisement payloads and generates the beacon configuration required for periodic self-registration on the MCP network. Calculates a visibility score (0–100) based on skill count and category diversity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skills_to_advertise` | `array` | Yes |  |
| `beacon_interval_seconds` | `integer` | No | How often the beacon re-registers with the MCP network (seconds). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mcp_discovery_beacon",
  "arguments": {
    "skills_to_advertise": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mcp_discovery_beacon"`.
