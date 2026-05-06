---
skill: development_pipeline_tracker
category: reits
description: Summarizes pipeline by stage, budget, and delivery exposure.
tier: free
inputs: projects
---

# Development Pipeline Tracker

## Description
Summarizes pipeline by stage, budget, and delivery exposure.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `projects` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "development_pipeline_tracker",
  "arguments": {
    "projects": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "development_pipeline_tracker"`.
