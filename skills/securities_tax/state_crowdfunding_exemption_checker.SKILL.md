---
skill: state_crowdfunding_exemption_checker
category: securities_tax
description: Determines state crowdfunding eligibility based on issuer location and raise size.
tier: free
inputs: issuer_state, investor_state, offering_amount
---

# State Crowdfunding Exemption Checker

## Description
Determines state crowdfunding eligibility based on issuer location and raise size.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `issuer_state` | `string` | Yes |  |
| `investor_state` | `string` | Yes |  |
| `offering_amount` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "state_crowdfunding_exemption_checker",
  "arguments": {
    "issuer_state": "<issuer_state>",
    "investor_state": "<investor_state>",
    "offering_amount": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "state_crowdfunding_exemption_checker"`.
