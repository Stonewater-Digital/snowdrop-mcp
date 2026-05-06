---
skill: agent_funnel_analyzer
category: analytics
description: Calculates conversion rates across registration, activation, engagement, and upgrade.
tier: free
inputs: agents
---

# Agent Funnel Analyzer

## Description
Calculates conversion rates across registration, activation, engagement, and upgrade.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agents` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_funnel_analyzer",
  "arguments": {
    "agents": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_funnel_analyzer"`.
