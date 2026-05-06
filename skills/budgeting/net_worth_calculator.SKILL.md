---
skill: net_worth_calculator
category: budgeting
description: Calculates net worth by subtracting total liabilities from total assets.
tier: free
inputs: assets, liabilities
---

# Net Worth Calculator

## Description
Calculates net worth by subtracting total liabilities from total assets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assets` | `array` | Yes | List of assets with name and value. |
| `liabilities` | `array` | Yes | List of liabilities with name and value. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "net_worth_calculator",
  "arguments": {
    "assets": [],
    "liabilities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "net_worth_calculator"`.
