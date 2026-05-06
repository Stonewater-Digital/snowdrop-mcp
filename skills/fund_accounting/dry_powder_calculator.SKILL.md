---
skill: dry_powder_calculator
category: fund_accounting
description: Calculates available dry powder (uninvested capital), deployment rate, and deployment runway for a private equity fund. Dry powder = total_commitments - capital_called - reserves.
tier: premium
inputs: none
---

# Dry Powder Calculator

## Description
Calculates available dry powder (uninvested capital), deployment rate, and deployment runway for a private equity fund. Dry powder = total_commitments - capital_called - reserves. If monthly_deployment_rate is provided, runway_months = dry_powder / rate. Useful for fund pacing, LP reporting, and GP investment planning. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "dry_powder_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dry_powder_calculator"`.
