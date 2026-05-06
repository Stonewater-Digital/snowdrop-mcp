---
skill: token_standard_risk_scorecard_generator
category: crypto_rwa
description: Generates composite risk scorecards per investor wallet for compliance teams.
tier: free
inputs: none
---

# Token Standard Risk Scorecard Generator

## Description
Generates composite risk scorecards per investor wallet for compliance teams.

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
  "tool": "token_standard_risk_scorecard_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_risk_scorecard_generator"`.
