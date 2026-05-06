---
skill: gcp_cloud_scheduler
category: gcp
description: Create, list, or delete Google Cloud Scheduler cron jobs. Use this to schedule Snowdrop's autonomous recurring tasks: hourly Moltbook feed checks, daily GitHub activity scans, weekly ecosystem radar sweeps, or timed content posting.
tier: free
inputs: action
---

# Gcp Cloud Scheduler

## Description
Create, list, or delete Google Cloud Scheduler cron jobs. Use this to schedule Snowdrop's autonomous recurring tasks: hourly Moltbook feed checks, daily GitHub activity scans, weekly ecosystem radar sweeps, or timed content posting. Jobs can trigger HTTP endpoints (like the MCP server) or Pub/Sub topics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes |  |
| `job_name` | `string` | No |  |
| `schedule` | `string` | No |  |
| `timezone_str` | `string` | No |  |
| `http_url` | `string` | No |  |
| `http_body` | `object` | No |  |
| `http_method` | `string` | No |  |
| `description` | `string` | No |  |
| `project_id` | `string` | No |  |
| `region` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gcp_cloud_scheduler",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gcp_cloud_scheduler"`.
