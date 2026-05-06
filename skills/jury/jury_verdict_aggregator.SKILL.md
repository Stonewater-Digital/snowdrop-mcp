---
skill: jury_verdict_aggregator
category: jury
description: Roll up model verdicts with dynamic confidence weighting and escalation logic.
tier: free
inputs: verdicts
---

# Jury Verdict Aggregator

## Description
Roll up model verdicts with dynamic confidence weighting and escalation logic.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `verdicts` | `array` | Yes | List of verdict dicts (model, position, confidence, reasoning). |
| `weights` | `object` | No | Custom model vote multipliers. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "jury_verdict_aggregator",
  "arguments": {
    "verdicts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "jury_verdict_aggregator"`.
