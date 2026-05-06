---
skill: brazil_pix_settlement_logic
category: compliance
description: Applies Banco Central do Brasil (BCB) Pix rules per Resolução BCB nº 1 (2020) and subsequent circulars. Validates transaction limits (nightly R$1,000 cap for PF), fee structures, settlement times (10 seconds 24/7), and transaction type restrictions.
tier: free
inputs: transaction
---

# Brazil Pix Settlement Logic

## Description
Applies Banco Central do Brasil (BCB) Pix rules per Resolução BCB nº 1 (2020) and subsequent circulars. Validates transaction limits (nightly R$1,000 cap for PF), fee structures, settlement times (10 seconds 24/7), and transaction type restrictions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transaction` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "brazil_pix_settlement_logic",
  "arguments": {
    "transaction": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "brazil_pix_settlement_logic"`.
