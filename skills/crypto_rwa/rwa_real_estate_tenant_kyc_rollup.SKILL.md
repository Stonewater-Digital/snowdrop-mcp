---
skill: rwa_real_estate_tenant_kyc_rollup
category: crypto_rwa
description: Aggregates tenant KYC attestations to verify income streams backing lease tokens.
tier: free
inputs: payload
---

# Rwa Real Estate Tenant Kyc Rollup

## Description
Aggregates tenant KYC attestations to verify income streams backing lease tokens.

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
  "tool": "rwa_real_estate_tenant_kyc_rollup",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_tenant_kyc_rollup"`.
