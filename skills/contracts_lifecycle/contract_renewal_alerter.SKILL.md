---
skill: contract_renewal_alerter
category: contracts_lifecycle
description: Identifies contracts requiring renewal action and quantifies value at risk.
tier: free
inputs: contracts, current_date
---

# Contract Renewal Alerter

## Description
Identifies contracts requiring renewal action and quantifies value at risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contracts` | `array` | Yes |  |
| `current_date` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "contract_renewal_alerter",
  "arguments": {
    "contracts": [],
    "current_date": "<current_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contract_renewal_alerter"`.
