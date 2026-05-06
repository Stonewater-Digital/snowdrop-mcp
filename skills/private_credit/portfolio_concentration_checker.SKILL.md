---
skill: portfolio_concentration_checker
category: private_credit
description: Flags concentration exposures versus policy limits.
tier: free
inputs: borrower_exposure, sector_exposure, geography_exposure
---

# Portfolio Concentration Checker

## Description
Flags concentration exposures versus policy limits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `borrower_exposure` | `array` | Yes |  |
| `sector_exposure` | `array` | Yes |  |
| `geography_exposure` | `array` | Yes |  |
| `borrower_limit_pct` | `number` | No |  |
| `sector_limit_pct` | `number` | No |  |
| `geography_limit_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_concentration_checker",
  "arguments": {
    "borrower_exposure": [],
    "sector_exposure": [],
    "geography_exposure": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_concentration_checker"`.
