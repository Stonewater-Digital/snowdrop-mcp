---
skill: approval_chain_builder
category: approval
description: Builds escalated approval chains based on action context and risk.
tier: free
inputs: action_type
---

# Approval Chain Builder

## Description
Builds escalated approval chains based on action context and risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action_type` | `string` | Yes |  |
| `amount` | `number` | No |  |
| `risk_level` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "approval_chain_builder",
  "arguments": {
    "action_type": "<action_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "approval_chain_builder"`.
