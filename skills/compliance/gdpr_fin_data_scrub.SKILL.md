---
skill: gdpr_fin_data_scrub
category: compliance
description: Removes or pseudonymises PII from financial data records per GDPR Article 5(1)(e) (storage limitation) and Article 25 (data protection by design). Uses SHA-256 hashing for reversible pseudonymisation or full redaction, preserving non-PII financial fields.
tier: free
inputs: data_records
---

# Gdpr Fin Data Scrub

## Description
Removes or pseudonymises PII from financial data records per GDPR Article 5(1)(e) (storage limitation) and Article 25 (data protection by design). Uses SHA-256 hashing for reversible pseudonymisation or full redaction, preserving non-PII financial fields.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data_records` | `array` | Yes | List of financial record dicts potentially containing PII |
| `pii_fields` | `array` | No | Field names to treat as PII (will be hashed or redacted) |
| `mode` | `string` | No | Processing mode: 'hash' (SHA-256 pseudonymisation) or 'redact' (replace with [REDACTED]) |
| `salt` | `string` | No | Optional salt string for HMAC-style hashing (improves pseudonymisation security) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gdpr_fin_data_scrub",
  "arguments": {
    "data_records": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gdpr_fin_data_scrub"`.
