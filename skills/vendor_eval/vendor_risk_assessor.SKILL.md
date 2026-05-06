---
skill: vendor_risk_assessor
category: vendor_eval
description: Evaluates concentration risk, SPOFs, and diversification across vendors.
tier: free
inputs: vendors
---

# Vendor Risk Assessor

## Description
Evaluates concentration risk, SPOFs, and diversification across vendors.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `vendors` | `array` | Yes | List of vendor objects, each with `name` (string), `spend_pct` (float, 0–100 share of total spend), `is_sole_provider` (bool), and `redundancy_level` (string: "none", "partial", "full"). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vendor_risk_assessor",
  "arguments": {
    "vendors": [
      {"name": "OpenRouter", "spend_pct": 65, "is_sole_provider": false, "redundancy_level": "partial"},
      {"name": "Anthropic", "spend_pct": 35, "is_sole_provider": false, "redundancy_level": "full"}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vendor_risk_assessor"`.
