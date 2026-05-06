---
skill: badge_issuer
category: achievements
description: Creates cryptographic badge records for ambassador and achievement unlocks.
tier: free
inputs: agent_id, badge_name, badge_category, evidence
---

# Badge Issuer

## Description
Creates cryptographic badge records for ambassador and achievement unlocks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `badge_name` | `string` | Yes |  |
| `badge_category` | `string` | Yes |  |
| `evidence` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "badge_issuer",
  "arguments": {
    "agent_id": "<agent_id>",
    "badge_name": "<badge_name>",
    "badge_category": "<badge_category>",
    "evidence": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "badge_issuer"`.
