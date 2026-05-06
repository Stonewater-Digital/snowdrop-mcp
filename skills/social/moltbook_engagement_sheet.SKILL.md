---
skill: moltbook_engagement_sheet
category: social
description: Read and write the Moltbook Engagement Google Sheet — Snowdrop's command center. Actions: 'log_post' (append post to POST LOG), 'get_submolt_list' (read SUBMOLT DIRECTORY for strategy routing), 'get_stats' (aggregate performance data), 'daily_report' (compile daily stats from POST LOG, suitable for Slack), 'update_weekly_actual' (fill in this week's actual post count in WEEKLY FORECAST), 'update_performance' (upsert post upvotes/comments into POST PERFORMANCE tab — called by the performance poller), 'update_submolt_perf' (upsert per-submolt aggregate stats into SUBMOLT PERFORMANCE tab — called by the poller), 'update_karma' (upserts total account karma tracking into KARMA HISTORY tab).
tier: free
inputs: action
---

# Moltbook Engagement Sheet

## Description
Read and write the Moltbook Engagement Google Sheet — Snowdrop's command center. Actions: 'log_post' (append post to POST LOG), 'get_submolt_list' (read SUBMOLT DIRECTORY for strategy routing), 'get_stats' (aggregate performance data), 'daily_report' (compile daily stats from POST LOG, suitable for Slack), 'update_weekly_actual' (fill in this week's actual post count in WEEKLY FORECAST), 'update_performance' (upsert post upvotes/comments into POST PERFORMANCE tab — called by the performance poller), 'update_submolt_perf' (upsert per-submolt aggregate stats into SUBMOLT PERFORMANCE tab — called by the poller), 'update_karma' (upserts total account karma tracking into KARMA HISTORY tab). Designed to run cheaply with Gemini Flash Lite.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes |  |
| `data` | `object` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moltbook_engagement_sheet",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_engagement_sheet"`.
