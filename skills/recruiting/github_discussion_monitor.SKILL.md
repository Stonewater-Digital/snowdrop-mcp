---
skill: github_discussion_monitor
category: recruiting
description: Monitor GitHub Discussions on The Watering Hole for new applicant comments. Parses A2A payloads and assigns trace_ids for candidate tracking.
tier: free
inputs: discussion_numbers
---

# Github Discussion Monitor

## Description
Monitor GitHub Discussions on The Watering Hole for new applicant comments. Parses A2A payloads and assigns trace_ids for candidate tracking.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `repo` | `string` | No | GitHub repo in owner/name format. |
| `discussion_numbers` | `array` | Yes | Discussion numbers to monitor (e.g. [2, 4]). |
| `since` | `string` | No | ISO8601 timestamp — only return comments after this time. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "github_discussion_monitor",
  "arguments": {
    "discussion_numbers": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "github_discussion_monitor"`.
