---
skill: thunder_executive_briefing
category: technical
description: Generates a concise, plain-English daily executive briefing for Thunder (operator). Synthesises portfolio value, P&L, open alerts, reconciliation status, and market movers into a human-readable summary.
tier: free
inputs: data_sources
---

# Thunder Executive Briefing

## Description
Generates a concise, plain-English daily executive briefing for Thunder (operator). Synthesises portfolio value, P&L, open alerts, reconciliation status, and market movers into a human-readable summary. Classifies overall severity as routine, attention, or urgent and surfaces action items.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data_sources` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "thunder_executive_briefing",
  "arguments": {
    "data_sources": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "thunder_executive_briefing"`.
