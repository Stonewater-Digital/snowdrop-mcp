---
skill: hardware_wallet_handshake
category: technical
description: Gate-keeps large on-chain transfers by requiring hardware wallet confirmation when a transaction exceeds the configured USD threshold. Generates a cryptographically random nonce and a confirmation request payload with a 5-minute expiry window.
tier: premium
inputs: none
---

# Hardware Wallet Handshake

## Description
Gate-keeps large on-chain transfers by requiring hardware wallet confirmation when a transaction exceeds the configured USD threshold. Generates a cryptographically random nonce and a confirmation request payload with a 5-minute expiry window. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "hardware_wallet_handshake",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "hardware_wallet_handshake"`.
