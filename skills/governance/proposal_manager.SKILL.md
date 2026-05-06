---
skill: proposal_manager
category: governance
description: Submits, lists, fetches, or closes proposals per Snowdrop governance rules.
tier: free
inputs: operation
---

# Proposal Manager

## Description
Submits, lists, fetches, or closes proposals per Snowdrop governance rules.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `proposal` | `['object', 'null']` | No |  |
| `proposal_id` | `['string', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "proposal_manager",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "proposal_manager"`.
