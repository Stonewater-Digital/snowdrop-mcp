---
skill: rwa_oracle_stress_scenario_projector
category: crypto_rwa
description: Applies stress shocks to oracle inputs to preview NAV drawdowns before they post.
tier: free
inputs: none
---

# Rwa Oracle Stress Scenario Projector

## Description
Applies stress shocks to oracle inputs to preview NAV drawdowns before they post.

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
  "tool": "rwa_oracle_stress_scenario_projector",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_stress_scenario_projector"`.
