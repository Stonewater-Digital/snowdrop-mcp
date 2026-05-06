---
skill: token_standard_mica_utility_token_guardrail
category: crypto_rwa
description: Checks MiCA utility token criteria to ensure consumer disclosures are adequate.
tier: free
inputs: payload
---

# Token Standard Mica Utility Token Guardrail

## Description
Checks MiCA utility token criteria to ensure consumer disclosures are adequate.

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
  "tool": "token_standard_mica_utility_token_guardrail",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_mica_utility_token_guardrail"`.
