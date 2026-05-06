---
skill: infrastructure_project_finance
category: alternative_investments
description: Constructs a single-asset project model to evaluate DSCR, LLCR, and equity IRR against capex and leverage assumptions. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Infrastructure Project Finance

## Description
Constructs a single-asset project model to evaluate DSCR, LLCR, and equity IRR against capex and leverage assumptions. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "infrastructure_project_finance",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "infrastructure_project_finance"`.
