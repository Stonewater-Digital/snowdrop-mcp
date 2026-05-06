---
skill: contribution_token_tracker
category: crowd_economics
description: Aggregates token usage by contributor type to measure leverage.
tier: free
inputs: contributions
---

# Contribution Token Tracker

## Description
Aggregates token usage by contributor type to measure leverage.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contributions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "contribution_token_tracker",
  "arguments": {
    "contributions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contribution_token_tracker"`.
