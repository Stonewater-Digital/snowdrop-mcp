---
skill: prompt_injection_shield
category: social
description: Scans incoming agent requests for prompt injection attacks, role-play overrides, encoding tricks, and unauthorized tool access. Returns threat level and blocked tools.
tier: free
inputs: incoming_request
---

# Prompt Injection Shield

## Description
Scans incoming agent requests for prompt injection attacks, role-play overrides, encoding tricks, and unauthorized tool access. Returns threat level and blocked tools.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `incoming_request` | `object` | Yes | Dict with: source_agent_id (str), request_text (str), requested_tools (list[str]), auth_token (str, optional). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "prompt_injection_shield",
  "arguments": {
    "incoming_request": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "prompt_injection_shield"`.
