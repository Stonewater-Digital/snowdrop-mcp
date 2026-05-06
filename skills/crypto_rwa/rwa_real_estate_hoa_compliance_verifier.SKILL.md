---
skill: rwa_real_estate_hoa_compliance_verifier
category: crypto_rwa
description: Checks HOA dues payments and covenant compliance before distributions are released.
tier: free
inputs: payload
---

# Rwa Real Estate Hoa Compliance Verifier

## Description
Checks HOA dues payments and covenant compliance before distributions are released.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_real_estate_hoa_compliance_verifier",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_hoa_compliance_verifier"`.
