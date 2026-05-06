---
skill: energy_efficiency_calculator
category: energy_finance
description: Calculate energy efficiency (useful output / energy input) as a percentage and compare to common benchmarks for various energy systems.
tier: free
inputs: energy_input, useful_output
---

# Energy Efficiency Calculator

## Description
Calculate energy efficiency (useful output / energy input) as a percentage and compare to common benchmarks for various energy systems.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `energy_input` | `number` | Yes | Total energy input (in any consistent unit). |
| `useful_output` | `number` | Yes | Useful energy output (same unit as input). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "energy_efficiency_calculator",
  "arguments": {
    "energy_input": 0,
    "useful_output": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "energy_efficiency_calculator"`.
