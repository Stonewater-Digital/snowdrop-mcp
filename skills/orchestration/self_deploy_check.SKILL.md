---
skill: self_deploy_check
category: orchestration
description: Detect unpushed commits on the current branch and push to origin/main to trigger Cloud Build CI/CD. Returns a summary of pushed commits or 'nothing to deploy' if HEAD matches origin/main.
tier: free
inputs: none
---

# Self Deploy Check

## Description
Detect unpushed commits on the current branch and push to origin/main to trigger Cloud Build CI/CD. Returns a summary of pushed commits or 'nothing to deploy' if HEAD matches origin/main.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dry_run` | `boolean` | No | If true, report unpushed commits without actually pushing. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "self_deploy_check",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "self_deploy_check"`.
