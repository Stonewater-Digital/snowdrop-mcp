---
skill: moic_calculator
category: fund_admin
description: Computes MOIC (Multiple on Invested Capital) as total value (realized + unrealized) divided by invested capital. Also returns gain/loss in dollar terms.
tier: premium
inputs: invested_capital, realized_value, unrealized_value
---

# Moic Calculator

## Description
Computes MOIC (Multiple on Invested Capital) as total value (realized + unrealized) divided by invested capital. Also returns gain/loss in dollar terms. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| invested_capital | number | Yes | Total capital invested at cost (denominator for MOIC calculation, USD) |
| realized_value | number | No | Cash proceeds already distributed from realized investments (default: 0.0) |
| unrealized_value | number | No | Current fair market value of remaining unrealized portfolio positions (default: 0.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moic_calculator",
  "arguments": {
    "invested_capital": 40000000,
    "realized_value": 28000000,
    "unrealized_value": 46000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moic_calculator"`.
