---
skill: reit_compliance_tester
category: reits
description: Evaluates income/asset/shareholder tests for REIT status.
tier: free
inputs: income_sources, assets, distributions, shareholders
---

# Reit Compliance Tester

## Description
Evaluates income/asset/shareholder tests for REIT status.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `income_sources` | `array` | Yes |  |
| `assets` | `array` | Yes |  |
| `distributions` | `object` | Yes |  |
| `shareholders` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reit_compliance_tester",
  "arguments": {
    "income_sources": [],
    "assets": [],
    "distributions": {},
    "shareholders": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reit_compliance_tester"`.
