---
skill: liquidity_premium_calculator
category: quant
description: Approximates annual liquidity drag from bid-ask spreads and funding costs.
tier: free
inputs: assets
---

# Liquidity Premium Calculator

## Description
Approximates annual liquidity drag from bid-ask spreads and funding costs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assets` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "liquidity_premium_calculator",
  "arguments": {
    "assets": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "liquidity_premium_calculator"`.
