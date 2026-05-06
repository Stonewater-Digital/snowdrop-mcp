---
skill: multi_repo_executor
category: github
description: Executes a shell command across all Stonewater-Digital repositories locally, handling cloning/pulling if necessary.
tier: free
inputs: command
---

# Multi Repo Executor

## Description
Executes a shell command across all Stonewater-Digital repositories locally, handling cloning/pulling if necessary.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `command` | `string` | Yes | The shell command to execute in each repository (e.g., 'git status') |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "multi_repo_executor",
  "arguments": {
    "command": "<command>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "multi_repo_executor"`.
