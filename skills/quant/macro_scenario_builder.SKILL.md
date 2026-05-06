---
skill: macro_scenario_builder
category: quant
description: Applies macro factor shocks to exposures to estimate scenario returns.
tier: free
inputs: factor_exposures, factor_shocks
---

# Macro Scenario Builder

## Description
Applies macro factor shocks to exposures to estimate scenario returns.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `factor_exposures` | `object` | Yes |  |
| `factor_shocks` | `object` | Yes |  |
| `base_return_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "macro_scenario_builder",
  "arguments": {
    "factor_exposures": {},
    "factor_shocks": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "macro_scenario_builder"`.
