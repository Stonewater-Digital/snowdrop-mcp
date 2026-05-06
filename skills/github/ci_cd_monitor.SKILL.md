---
skill: ci_cd_monitor
category: github
description: Monitor GitHub Actions CI/CD workflows. Returns strict JSON summaries of workflow statuses and failures, avoiding massive raw log dumps.
tier: free
inputs: owner_repo, action
---

# Ci Cd Monitor

## Description
Monitor GitHub Actions CI/CD workflows. Returns strict JSON summaries of workflow statuses and failures, avoiding massive raw log dumps.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `owner_repo` | `string` | Yes | The repository owner/name (e.g., 'Stonewater-Digital/snowdrop-core'). |
| `action` | `string` | Yes | Operation to perform: 'latest_runs' or 'run_details'. |
| `run_id` | `integer` | No | Workflow run ID. Required if action is 'run_details'. |
| `limit` | `integer` | No | Number of runs to return for 'latest_runs'. Default 5. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ci_cd_monitor",
  "arguments": {
    "owner_repo": "<owner_repo>",
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ci_cd_monitor"`.
