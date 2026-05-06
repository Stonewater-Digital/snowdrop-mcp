---
skill: rwa_treasury_maturity_schedule_guardian
category: crypto_rwa
description: Checks that token maturity ladders align with underlying Treasury maturity dates.
tier: free
inputs: none
---

# Rwa Treasury Maturity Schedule Guardian

## Description
Checks that token maturity ladders align with underlying Treasury maturity dates.

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
  "tool": "rwa_treasury_maturity_schedule_guardian",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_maturity_schedule_guardian"`.
