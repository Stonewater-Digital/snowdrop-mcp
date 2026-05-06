---
skill: agentic_syndication_logic
category: social
description: Assembles an optimal bot syndicate for a given mission by filtering candidates on availability and trust, matching skills to requirements, and minimizing cost while maximizing skill coverage.
tier: free
inputs: mission, candidates
---

# Agentic Syndication Logic

## Description
Assembles an optimal bot syndicate for a given mission by filtering candidates on availability and trust, matching skills to requirements, and minimizing cost while maximizing skill coverage.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mission` | `object` | Yes | Dict with: objective (str), required_skills (list[str]), min_trust_score (float), budget (float in USD). |
| `candidates` | `array` | Yes | List of candidate agent dicts with: agent_id (str), skills (list[str]), trust_score (float), hourly_rate (float), availability (bool). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agentic_syndication_logic",
  "arguments": {
    "mission": {},
    "candidates": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agentic_syndication_logic"`.
