---
skill: task_dependency_resolver
category: workflow
description: Performs topological sorting and surfaces parallelizable groups.
tier: free
inputs: tasks
---

# Task Dependency Resolver

## Description
Performs topological sorting and surfaces parallelizable groups.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tasks` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "task_dependency_resolver",
  "arguments": {
    "tasks": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "task_dependency_resolver"`.
