---
skill: mortality_table_lookup
category: insurance_analytics
description: Returns representative 2017 CSO mortality assumptions (qx, lx, and curtate life expectancy) for a given age, gender, and smoker status. Interpolates to the nearest available age bucket.
tier: free
inputs: age, gender
---

# Mortality Table Lookup

## Description
Returns representative 2017 CSO mortality assumptions (qx, lx, and curtate life expectancy) for a given age, gender, and smoker status. Interpolates to the nearest available age bucket.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `age` | `integer` | Yes | Attained age of the insured. Must be 0–120. |
| `gender` | `string` | Yes | Biological sex for CSO table selection. |
| `smoker_status` | `string` | No | Smoker classification. 'aggregate' blends smoker/nonsmoker for non-underwritten products. Default: 'aggregate'. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mortality_table_lookup",
  "arguments": {
    "age": 0,
    "gender": "<gender>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mortality_table_lookup"`.
