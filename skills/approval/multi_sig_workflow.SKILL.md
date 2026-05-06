---
skill: multi_sig_workflow
category: approval
description: Classifies an action into auto, 2FA, or multi-sig approval paths.
tier: free
inputs: action
---

# Multi Sig Workflow

## Description
Classifies an action into auto, 2FA, or multi-sig approval paths.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `object` | Yes |  |
| `approval_rules` | `object` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "multi_sig_workflow",
  "arguments": {
    "action": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "multi_sig_workflow"`.
