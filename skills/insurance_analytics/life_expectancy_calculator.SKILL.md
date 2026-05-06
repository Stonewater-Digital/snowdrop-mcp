---
skill: life_expectancy_calculator
category: insurance_analytics
description: Calculates curtate life expectancy (e_x), complete life expectancy (ê_x), and median future lifetime from a list of annual qx mortality rates. Uses exact actuarial recursion: t_px = product of (1 - q_{x+k}) for k=0..t-1.
tier: free
inputs: qx_rates, start_age
---

# Life Expectancy Calculator

## Description
Calculates curtate life expectancy (e_x), complete life expectancy (ê_x), and median future lifetime from a list of annual qx mortality rates. Uses exact actuarial recursion: t_px = product of (1 - q_{x+k}) for k=0..t-1.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `qx_rates` | `array` | Yes | Ordered list of annual probabilities of death q_{x}, q_{x+1}, …, q_{x+n-1}. Each value must be in [0, 1]. The list represents successive ages from start_age. |
| `start_age` | `integer` | Yes | Attained age corresponding to the first element of qx_rates. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "life_expectancy_calculator",
  "arguments": {
    "qx_rates": [],
    "start_age": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "life_expectancy_calculator"`.
