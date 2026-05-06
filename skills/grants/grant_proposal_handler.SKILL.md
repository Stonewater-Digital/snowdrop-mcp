---
skill: grant_proposal_handler
category: grants
description: Accepts, evaluates, and adjudicates Goodwill grant proposals.
tier: free
inputs: operation
---

# Grant Proposal Handler

## Description
Accepts, evaluates, and adjudicates Goodwill grant proposals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `proposal` | `['object', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "grant_proposal_handler",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "grant_proposal_handler"`.
