---
skill: total_return_calculator
category: portfolio
description: Calculates total return as a percentage, including both capital appreciation and dividend income.
tier: free
inputs: begin_value, end_value
---

# Total Return Calculator

## Description
Calculates total return as a percentage, including both capital appreciation and dividend income.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `begin_value` | `number` | Yes | Beginning investment value. |
| `end_value` | `number` | Yes | Ending investment value. |
| `dividends` | `number` | No | Total dividends received (default 0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "total_return_calculator",
  "arguments": {
    "begin_value": 0,
    "end_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "total_return_calculator"`.
