---
skill: brexit_passporting_check
category: compliance
description: Post-Brexit cross-border licensing analysis for UK and EU financial services. Confirms that EEA passporting is definitively unavailable since 31 December 2020, evaluates available equivalence decisions, and determines local authorisation requirements per target market and licence type.
tier: premium
inputs: entity_data
---

# Brexit Passporting Check

## Description
Post-Brexit cross-border licensing analysis for UK and EU financial services. Confirms that EEA passporting is definitively unavailable since 31 December 2020, evaluates available equivalence decisions, and determines local authorisation requirements per target market and licence type. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity_data` | `object` | Yes | Entity details including home jurisdiction, licence type, and target EU/UK markets for passporting analysis |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "brexit_passporting_check",
  "arguments": {
    "entity_data": {
      "home_jurisdiction": "UK",
      "licence_type": "MiFID_II_investment_firm",
      "target_markets": ["DE", "FR", "NL"]
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "brexit_passporting_check"`.
