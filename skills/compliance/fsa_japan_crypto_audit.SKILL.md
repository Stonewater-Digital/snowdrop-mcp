---
skill: fsa_japan_crypto_audit
category: compliance
description: Audits a Japanese crypto-asset exchange against FSA (Financial Services Agency) requirements under the Payment Services Act (資金決済に関する法律), specifically cold storage minimums, asset segregation, and operational security controls. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: exchange_data
---

# Fsa Japan Crypto Audit

## Description
Audits a Japanese crypto-asset exchange against FSA (Financial Services Agency) requirements under the Payment Services Act (資金決済に関する法律), specifically cold storage minimums, asset segregation, and operational security controls. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exchange_data` | `object` | Yes | Exchange operational data including cold storage ratio, asset segregation status, and security control documentation for FSA audit |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fsa_japan_crypto_audit",
  "arguments": {
    "exchange_data": {
      "exchange_name": "SakuraCrypto KK",
      "cold_storage_ratio": 0.95,
      "asset_segregation": true,
      "registered_assets": ["BTC", "ETH", "XRP"]
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fsa_japan_crypto_audit"`.
