---
skill: gcp_cloud_scheduler
category: gcp
description: Create, list, or delete Google Cloud Scheduler cron jobs. Use this to schedule Snowdrop's autonomous recurring tasks: hourly Moltbook feed checks, daily GitHub activity scans, weekly ecosystem radar sweeps, or timed content posting.
tier: free
inputs: none
---

# Gcp Cloud Scheduler

## Description
Create, list, or delete Google Cloud Scheduler cron jobs. Use this to schedule Snowdrop's autonomous recurring tasks: hourly Moltbook feed checks, daily GitHub activity scans, weekly ecosystem radar sweeps, or timed content posting. Jobs can trigger HTTP endpoints (like the MCP server) or Pub/Sub topics.

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
  "tool": "gcp_cloud_scheduler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gcp_cloud_scheduler"`.
