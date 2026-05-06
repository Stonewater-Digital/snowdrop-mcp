---
skill: reit_dividend_reinvestment_logic
category: technical
description: Executes Dividend Reinvestment Plan (DRIP) logic for a REIT distribution. Calculates whole and fractional shares purchasable at the current share price, computes the blended new cost basis per share, and produces a reinvestment summary suitable for ledger entry.
tier: free
inputs: dividend
---

# Reit Dividend Reinvestment Logic

## Description
Executes Dividend Reinvestment Plan (DRIP) logic for a REIT distribution. Calculates whole and fractional shares purchasable at the current share price, computes the blended new cost basis per share, and produces a reinvestment summary suitable for ledger entry.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dividend` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reit_dividend_reinvestment_logic",
  "arguments": {
    "dividend": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reit_dividend_reinvestment_logic"`.
