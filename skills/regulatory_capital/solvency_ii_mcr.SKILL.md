---
skill: solvency_ii_mcr
category: regulatory_capital
description: Derives MCR using Solvency II linear formula (Life + Non-life) and SCR floor/cap.
tier: free
inputs: technical_provisions, written_premiums, scr
---

# Solvency Ii Mcr

## Description
Derives MCR using Solvency II linear formula (Life + Non-life) and SCR floor/cap.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `technical_provisions` | `number` | Yes | Net technical provisions. |
| `written_premiums` | `number` | Yes | Net written premiums of last 12 months. |
| `scr` | `number` | Yes | Solvency capital requirement. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "solvency_ii_mcr",
  "arguments": {
    "technical_provisions": 0,
    "written_premiums": 0,
    "scr": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "solvency_ii_mcr"`.
