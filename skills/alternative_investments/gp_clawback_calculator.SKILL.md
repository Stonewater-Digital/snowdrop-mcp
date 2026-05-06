---
skill: gp_clawback_calculator
category: alternative_investments
description: Compares distributed carry versus catch-up waterfall to determine outstanding clawback and recommended escrow percentage. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Gp Clawback Calculator

## Description
Compares distributed carry versus catch-up waterfall to determine outstanding clawback and recommended escrow percentage. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "gp_clawback_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gp_clawback_calculator"`.
