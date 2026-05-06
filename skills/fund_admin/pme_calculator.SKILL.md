---
skill: pme_calculator
category: fund_admin
description: Calculates Kaplan-Schoar PME (Public Market Equivalent) by discounting fund contributions and distributions using the compounded index return path. PME > 1.0 means the fund outperformed the public market benchmark.
tier: premium
inputs: none
---

# Pme Calculator

## Description
Calculates Kaplan-Schoar PME (Public Market Equivalent) by discounting fund contributions and distributions using the compounded index return path. PME > 1.0 means the fund outperformed the public market benchmark. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "pme_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pme_calculator"`.
