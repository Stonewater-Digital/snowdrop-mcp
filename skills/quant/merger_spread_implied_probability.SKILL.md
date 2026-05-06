---
skill: merger_spread_implied_probability
category: quant
description: Calculates M&A deal closing probability from market spread, offer price, and unaffected downside.
tier: free
inputs: target_ticker, offer_price, current_price, unaffected_price
---

# Merger Spread Implied Probability

## Description
Calculates M&A deal closing probability from market spread, offer price, and unaffected downside.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target_ticker` | `string` | Yes | Ticker symbol of the target company. |
| `offer_price` | `number` | Yes | Acquisition offer price per share. Must be > unaffected_price. |
| `current_price` | `number` | Yes | Current trading price of the target. Must be > 0. |
| `unaffected_price` | `number` | Yes | Estimated price if the deal breaks. Must be > 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "merger_spread_implied_probability",
  "arguments": {
    "target_ticker": "<target_ticker>",
    "offer_price": 0,
    "current_price": 0,
    "unaffected_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "merger_spread_implied_probability"`.
