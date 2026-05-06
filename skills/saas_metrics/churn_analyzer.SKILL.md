---
skill: churn_analyzer
category: saas_metrics
description: Analyzes churn patterns, cohort retention, and at-risk agents.
tier: free
inputs: agents, analysis_date
---

# Churn Analyzer

## Description
Analyzes churn patterns, cohort retention, and at-risk agents.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agents` | `array` | Yes | Agent records with agent_id, signup_date, last_active_date, total_spend, and tier. |
| `analysis_date` | `string` | Yes | ISO timestamp used to determine churn windows. |
| `churn_window_days` | `integer` | No | Days of inactivity before an agent is considered churned. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "churn_analyzer",
  "arguments": {
    "agents": [],
    "analysis_date": "<analysis_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "churn_analyzer"`.
