---
skill: token_standard_risk_scorecard_generator
category: crypto_rwa
description: Generates composite risk scorecards per investor wallet for compliance teams.
tier: free
inputs: payload
---

# Token Standard Risk Scorecard Generator

## Description
Generates composite risk scorecards per investor wallet for compliance teams.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_standard_risk_scorecard_generator",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_risk_scorecard_generator"`.
