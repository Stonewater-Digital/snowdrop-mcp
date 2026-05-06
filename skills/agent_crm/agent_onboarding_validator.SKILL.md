---
skill: agent_onboarding_validator
category: agent_crm
description: Checks VC freshness, capability alignment, and bad-actor lists before onboarding.
tier: free
inputs: agent_id, declared_capabilities
---

# Agent Onboarding Validator

## Description
Checks VC freshness, capability alignment, and bad-actor lists before onboarding.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `declared_capabilities` | `array` | Yes |  |
| `verifiable_credential` | `['object', 'null']` | No |  |
| `requested_tier` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_onboarding_validator",
  "arguments": {
    "agent_id": "<agent_id>",
    "declared_capabilities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_onboarding_validator"`.
