---
skill: rwa_treasury_auction_allotment_matcher
category: crypto_rwa
description: Matches primary auction allotments to token mint quantities to prevent synthetic supply.
tier: free
inputs: payload
---

# Rwa Treasury Auction Allotment Matcher

## Description
Matches primary auction allotments to token mint quantities to prevent synthetic supply.

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
  "tool": "rwa_treasury_auction_allotment_matcher",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_auction_allotment_matcher"`.
