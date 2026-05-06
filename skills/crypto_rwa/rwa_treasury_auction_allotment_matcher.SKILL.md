---
skill: rwa_treasury_auction_allotment_matcher
category: crypto_rwa
description: Matches primary auction allotments to token mint quantities to prevent synthetic supply.
tier: free
inputs: none
---

# Rwa Treasury Auction Allotment Matcher

## Description
Matches primary auction allotments to token mint quantities to prevent synthetic supply.

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
  "tool": "rwa_treasury_auction_allotment_matcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_auction_allotment_matcher"`.
