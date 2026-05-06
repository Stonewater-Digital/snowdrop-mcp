---
skill: github_issue_tracker
category: integrations
description: Fetches labeled GitHub issues and estimates difficulty.
tier: free
inputs: repo
---

# Github Issue Tracker

## Description
Fetches labeled GitHub issues and estimates difficulty.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `repo` | `string` | Yes |  |
| `labels` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "github_issue_tracker",
  "arguments": {
    "repo": "<repo>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "github_issue_tracker"`.
