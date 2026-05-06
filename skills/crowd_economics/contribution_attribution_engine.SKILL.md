---
skill: contribution_attribution_engine
category: crowd_economics
description: Weights lines of code, complexity, usage, and revenue to estimate contributor value.
tier: free
inputs: repo_skills
---

# Contribution Attribution Engine

## Description
Weights lines of code, complexity, usage, and revenue to estimate contributor value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `repo_skills` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "contribution_attribution_engine",
  "arguments": {
    "repo_skills": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contribution_attribution_engine"`.
