---
skill: github_activity_monitor
category: social
description: Monitor Snowdrop's GitHub repos (snowdrop-mcp, the-watering-hole) for new activity: new stars, forks, discussion replies, issues, and pull requests. Returns a prioritized feed of items that warrant a response.
tier: free
inputs: none
---

# Github Activity Monitor

## Description
Monitor Snowdrop's GitHub repos (snowdrop-mcp, the-watering-hole) for new activity: new stars, forks, discussion replies, issues, and pull requests. Returns a prioritized feed of items that warrant a response. Also checks any additional repos specified. Run as a periodic vigilance check.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "github_activity_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "github_activity_monitor"`.
