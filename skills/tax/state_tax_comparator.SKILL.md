---
skill: state_tax_comparator
category: tax
description: Compare effective state income tax rates for a given income across specified states. Hardcoded rates for the top 10 US states by population.
tier: free
inputs: income, states
---

# State Tax Comparator

## Description
Compare effective state income tax rates for a given income across specified states. Hardcoded rates for the top 10 US states by population.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `income` | `number` | Yes | Annual income in USD to compute state tax on. |
| `states` | `array` | Yes | List of state abbreviations to compare (e.g. ['CA', 'TX', 'NY']). Supported: CA, NY, TX, FL, WA, IL, PA, OH, NJ, MA. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "state_tax_comparator",
  "arguments": {
    "income": 0,
    "states": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "state_tax_comparator"`.
