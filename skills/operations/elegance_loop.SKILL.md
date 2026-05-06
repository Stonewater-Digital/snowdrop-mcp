---
skill: elegance_loop
category: operations
description: Compares planned actions against executed results, quantifies drift, and flags when discrepancies breach the 1% tolerance.
tier: free
inputs: planned_actions, executed_results
---

# Elegance Loop

## Description
Compares planned actions against executed results, quantifies drift, and flags when discrepancies breach the 1% tolerance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `planned_actions` | `array` | Yes | Actions Snowdrop intended to execute. |
| `executed_results` | `array` | Yes | Observed execution logs or API receipts. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "elegance_loop",
  "arguments": {
    "planned_actions": [],
    "executed_results": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "elegance_loop"`.
