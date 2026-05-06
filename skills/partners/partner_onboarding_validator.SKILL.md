---
skill: partner_onboarding_validator
category: partners
description: Ensures partner submissions meet baseline technical and compliance requirements.
tier: free
inputs: partner
---

# Partner Onboarding Validator

## Description
Ensures partner submissions meet baseline technical and compliance requirements.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `partner` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "partner_onboarding_validator",
  "arguments": {
    "partner": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "partner_onboarding_validator"`.
