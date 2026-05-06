---
skill: vix_term_structure_analyzer
category: technical_analysis
description: Analyzes VIX futures prices by expiry to identify contango/backwardation and roll yield.
tier: free
inputs: vix_prices
---

# Vix Term Structure Analyzer

## Description
Analyzes VIX futures prices by expiry to identify contango/backwardation and roll yield.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `vix_prices` | `array` | Yes | List of objects with expiry_days and price for VIX futures. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vix_term_structure_analyzer",
  "arguments": {
    "vix_prices": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vix_term_structure_analyzer"`.
