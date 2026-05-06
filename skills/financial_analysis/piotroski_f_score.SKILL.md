---
skill: piotroski_f_score
category: financial_analysis
description: Evaluates the nine Piotroski signals to rate financial strength.
tier: free
inputs: current, prior
---

# Piotroski F Score

## Description
Evaluates the nine Piotroski signals to rate financial strength.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current` | `object` | Yes |  |
| `prior` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "piotroski_f_score",
  "arguments": {
    "current": {},
    "prior": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "piotroski_f_score"`.
