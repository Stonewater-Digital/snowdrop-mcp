---
skill: stress_test_capital_trajectory
category: regulatory_capital
description: Projects CET1 ratio quarter-by-quarter under supervisory stress inputs.
tier: free
inputs: starting_cet1_capital, starting_rwa, quarterly_losses, quarterly_ppnr, rwa_growth_path_pct
---

# Stress Test Capital Trajectory

## Description
Projects CET1 ratio quarter-by-quarter under supervisory stress inputs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `starting_cet1_capital` | `number` | Yes | Starting CET1 capital. |
| `starting_rwa` | `number` | Yes | Starting risk-weighted assets. |
| `quarterly_losses` | `array` | Yes | Credit losses per quarter. |
| `quarterly_ppnr` | `array` | Yes | Pre-provision net revenue per quarter. |
| `rwa_growth_path_pct` | `array` | Yes | Percentage RWA change per quarter. |
| `deferred_tax_assets` | `array` | No | DTA write-down/add-back per quarter. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "stress_test_capital_trajectory",
  "arguments": {
    "starting_cet1_capital": 0,
    "starting_rwa": 0,
    "quarterly_losses": [],
    "quarterly_ppnr": [],
    "rwa_growth_path_pct": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "stress_test_capital_trajectory"`.
