---
skill: fiat_to_crypto_onramp_audit
category: sovereign
description: Audits fiat-to-crypto on-ramp transactions for volume, fees, velocity, and anomalous spikes.
tier: free
inputs: onramp_data, period_days
---

# Fiat To Crypto Onramp Audit

## Description
Audits fiat-to-crypto on-ramp transactions for volume, fees, velocity, and anomalous spikes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `onramp_data` | `array` | Yes | List of on-ramp transaction records |
| `period_days` | `integer` | Yes | Analysis window in days |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fiat_to_crypto_onramp_audit",
  "arguments": {
    "onramp_data": [],
    "period_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fiat_to_crypto_onramp_audit"`.
