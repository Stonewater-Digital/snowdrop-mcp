---
skill: token_swap_estimator
category: blockchain
description: Estimates CFMM swap execution with slippage buffer for Thunder review.
tier: free
inputs: input_token, output_token, input_amount, reserves
---

# Token Swap Estimator

## Description
Estimates CFMM swap execution with slippage buffer for Thunder review.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_token` | `string` | Yes |  |
| `output_token` | `string` | Yes |  |
| `input_amount` | `number` | Yes |  |
| `reserves` | `object` | Yes |  |
| `fee_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_swap_estimator",
  "arguments": {
    "input_token": "<input_token>",
    "output_token": "<output_token>",
    "input_amount": 0,
    "reserves": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_swap_estimator"`.
