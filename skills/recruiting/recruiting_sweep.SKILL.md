---
skill: recruiting_sweep
category: recruiting
description: Autonomous recruiting pipeline orchestrator. Monitors GitHub Discussions, classifies comments, runs intake/interview/audit/evaluation, and advances candidates through the pipeline.
tier: free
inputs: none
---

# Recruiting Sweep

## Description
Autonomous recruiting pipeline orchestrator. Monitors GitHub Discussions, classifies comments, runs intake/interview/audit/evaluation, and advances candidates through the pipeline. Called by systemd timer.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `discussion_numbers` | `array` | No | Discussion numbers to monitor. |
| `dry_run` | `boolean` | No | If true, log actions but don't execute them. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "recruiting_sweep",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "recruiting_sweep"`.
