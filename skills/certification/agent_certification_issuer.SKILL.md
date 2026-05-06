---
skill: agent_certification_issuer
category: certification
description: Generates signed certificates for agents who pass compatibility tests.
tier: free
inputs: agent_id, compatibility_score, test_date, certification_level
---

# Agent Certification Issuer

## Description
Generates signed certificates for agents who pass compatibility tests.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `compatibility_score` | `number` | Yes |  |
| `test_date` | `string` | Yes |  |
| `certification_level` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_certification_issuer",
  "arguments": {
    "agent_id": "<agent_id>",
    "compatibility_score": 0,
    "test_date": "<test_date>",
    "certification_level": "<certification_level>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_certification_issuer"`.
