---
skill: drawdown_analyzer
category: fund_admin
description: Computes drawdown metrics from an equity curve or NAV series. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Drawdown Analyzer

## Description
Computes drawdown metrics from an equity curve or NAV series. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "drawdown_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "drawdown_analyzer"`.
