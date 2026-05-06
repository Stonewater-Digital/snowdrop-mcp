---
skill: withholding_obligation_tracker
category: tax
description: Compute gross vs. net distributions and withholding requirements per LP.
tier: free
inputs: distributions
---

# Withholding Obligation Tracker

## Description
Compute gross vs. net distributions and withholding requirements per LP.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `distributions` | `array` | Yes | Entries with lp_name, amount, residency, and classification. |
| `default_rate` | `number` | No | Fallback withholding rate when no treaty override exists. |
| `treaty_overrides` | `object` | No | Map of residency or LP name to withholding rate. |
| `base_currency` | `string` | No | Currency label for reporting. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "withholding_obligation_tracker",
  "arguments": {
    "distributions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "withholding_obligation_tracker"`.
