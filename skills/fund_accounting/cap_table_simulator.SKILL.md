---
skill: cap_table_simulator
category: fund_accounting
description: Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Cap Table Simulator

## Description
Models equity dilution across funding rounds, tracking ownership percentages per stakeholder with option pool. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "cap_table_simulator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cap_table_simulator"`.
