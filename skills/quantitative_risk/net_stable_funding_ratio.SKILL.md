---
skill: net_stable_funding_ratio
category: quantitative_risk
description: Calculates ASF and RSF weighted balances to determine NSFR compliance.
tier: free
inputs: available_stable_funding, required_stable_funding
---

# Net Stable Funding Ratio

## Description
Calculates ASF and RSF weighted balances to determine NSFR compliance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `available_stable_funding` | `array` | Yes | Items contributing to ASF with factors (0-100%). |
| `required_stable_funding` | `array` | Yes | Assets requiring funding with RSF factors (0-100%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "net_stable_funding_ratio",
  "arguments": {
    "available_stable_funding": [],
    "required_stable_funding": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "net_stable_funding_ratio"`.
