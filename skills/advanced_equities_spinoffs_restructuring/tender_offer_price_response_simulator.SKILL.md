---
skill: tender_offer_price_response_simulator
category: advanced_equities_spinoffs_restructuring
description: Projects price paths for issuer/third-party tender offers across acceptance levels.
tier: free
inputs: none
---

# Tender Offer Price Response Simulator

## Description
Projects price paths for issuer/third-party tender offers across acceptance levels.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tickers` | `array` | No | Tickers or identifiers relevant to the analysis focus. |
| `lookback_days` | `integer` | No | Historical window (days) for synthetic / free-data calculations. |
| `analysis_notes` | `string` | No | Optional qualitative context to embed in the response. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tender_offer_price_response_simulator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tender_offer_price_response_simulator"`.
