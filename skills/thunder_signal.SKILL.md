---
skill: thunder_signal
category: root
description: Sends a severity-tiered Telegram alert to Thunder (the Operator). Severity levels: CRITICAL (vault breach, reconciliation failure), WARNING (Sybil infiltration, threshold breach), INTEL (general updates, Great Day).
tier: free
inputs: severity, message
---

# Thunder Signal

## Description
Sends a severity-tiered Telegram alert to Thunder (the Operator). Severity levels: CRITICAL (vault breach, reconciliation failure), WARNING (Sybil infiltration, threshold breach), INTEL (general updates, Great Day).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `severity` | `string` | Yes | Alert severity tier. |
| `message` | `string` | Yes | The body of the alert message to deliver to Thunder. |
| `buttons` | `array` | No | Optional interactive inline buttons. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "thunder_signal",
  "arguments": {
    "severity": "<severity>",
    "message": "<message>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "thunder_signal"`.
