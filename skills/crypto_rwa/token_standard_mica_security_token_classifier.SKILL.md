---
skill: token_standard_mica_security_token_classifier
category: crypto_rwa
description: Runs MiCA tests to classify tokens as financial instruments requiring passporting.
tier: free
inputs: payload
---

# Token Standard Mica Security Token Classifier

## Description
Runs MiCA tests to classify tokens as financial instruments requiring passporting.

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
  "tool": "token_standard_mica_security_token_classifier",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_mica_security_token_classifier"`.
