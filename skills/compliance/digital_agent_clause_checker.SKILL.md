---
skill: digital_agent_clause_checker
category: compliance
description: Evaluates actions against identity, spend, and communication rules. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Digital Agent Clause Checker

## Description
Evaluates actions against identity, spend, and communication rules. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "digital_agent_clause_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "digital_agent_clause_checker"`.
