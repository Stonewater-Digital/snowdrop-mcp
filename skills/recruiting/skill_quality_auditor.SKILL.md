---
skill: skill_quality_auditor
category: recruiting
description: AST-based security and quality audit for submitted skill code. Checks for dangerous imports, unsafe builtins, and TOOL_META compliance.
tier: free
inputs: code, trace_id
---

# Skill Quality Auditor

## Description
AST-based security and quality audit for submitted skill code. Checks for dangerous imports, unsafe builtins, and TOOL_META compliance. Returns A2A-compliant feedback for revision requests.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `code` | `string` | Yes | Python source code to audit. |
| `trace_id` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_quality_auditor",
  "arguments": {
    "code": "<code>",
    "trace_id": "<trace_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_quality_auditor"`.
