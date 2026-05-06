---
skill: portfolio_concentration_risk
category: middle_office
description: Flags single-name, sector, and factor concentration breaches.
tier: free
inputs: positions, limits
---

# Portfolio Concentration Risk

## Description
Flags single-name, sector, and factor concentration breaches.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `limits` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_concentration_risk",
  "arguments": {
    "positions": [],
    "limits": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_concentration_risk"`.
