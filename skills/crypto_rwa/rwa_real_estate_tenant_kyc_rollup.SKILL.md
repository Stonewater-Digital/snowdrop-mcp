---
skill: rwa_real_estate_tenant_kyc_rollup
category: crypto_rwa
description: Aggregates tenant KYC attestations to verify income streams backing lease tokens.
tier: free
inputs: none
---

# Rwa Real Estate Tenant Kyc Rollup

## Description
Aggregates tenant KYC attestations to verify income streams backing lease tokens.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_real_estate_tenant_kyc_rollup",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_tenant_kyc_rollup"`.
