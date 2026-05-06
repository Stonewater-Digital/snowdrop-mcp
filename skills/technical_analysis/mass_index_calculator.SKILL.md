---
skill: mass_index_calculator
category: technical_analysis
description: Calculate the Mass Index, which uses the high-low range to identify trend reversals through 'reversal bulges'. A bulge above 27 followed by drop below 26.5 signals reversal.
tier: free
inputs: highs, lows
---

# Mass Index Calculator

## Description
Calculate the Mass Index, which uses the high-low range to identify trend reversals through 'reversal bulges'. A bulge above 27 followed by drop below 26.5 signals reversal.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `period` | `integer` | No | Summation period for the Mass Index. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mass_index_calculator",
  "arguments": {
    "highs": [],
    "lows": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mass_index_calculator"`.
