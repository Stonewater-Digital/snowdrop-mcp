---
skill: portfolio_beta_calculator
category: middle_office
description: Calculates weighted average beta from constituent betas and weights.
tier: free
inputs: positions
---

# Portfolio Beta Calculator

## Description
Calculates weighted average beta from constituent betas and weights.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_beta_calculator",
  "arguments": {
    "positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_beta_calculator"`.
