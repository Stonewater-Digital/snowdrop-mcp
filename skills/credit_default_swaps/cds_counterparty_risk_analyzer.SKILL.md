---
skill: cds_counterparty_risk_analyzer
category: credit_default_swaps
description: Evaluates CDS counterparty exposures versus assigned limits.
tier: free
inputs: counterparties
---

# Cds Counterparty Risk Analyzer

## Description
Evaluates CDS counterparty exposures versus assigned limits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `counterparties` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_counterparty_risk_analyzer",
  "arguments": {
    "counterparties": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_counterparty_risk_analyzer"`.
