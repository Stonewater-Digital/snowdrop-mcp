---
skill: state_nexus_analyzer
category: fund_tax
description: Assesses economic and physical nexus triggers for hedge funds under Wayfair and marketplace sourcing rules. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# State Nexus Analyzer

## Description
Assesses economic and physical nexus triggers for hedge funds under Wayfair and marketplace sourcing rules. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "state_nexus_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "state_nexus_analyzer"`.
