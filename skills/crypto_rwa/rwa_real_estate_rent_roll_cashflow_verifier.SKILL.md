---
skill: rwa_real_estate_rent_roll_cashflow_verifier
category: crypto_rwa
description: Audits rent-roll statements against stablecoin remittance data for income-backed tokens.
tier: free
inputs: payload
---

# Rwa Real Estate Rent Roll Cashflow Verifier

## Description
Audits rent-roll statements against stablecoin remittance data for income-backed tokens.

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
  "tool": "rwa_real_estate_rent_roll_cashflow_verifier",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_real_estate_rent_roll_cashflow_verifier"`.
