---
skill: imf_sdr_allocation_tracker
category: sovereign
description: Tracks IMF Special Drawing Rights (SDR) holdings vs allocations for a country, converts to USD, and assesses quota adequacy.
tier: free
inputs: country_data, sdr_usd_rate
---

# Imf Sdr Allocation Tracker

## Description
Tracks IMF Special Drawing Rights (SDR) holdings vs allocations for a country, converts to USD, and assesses quota adequacy.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `country_data` | `object` | Yes | Country SDR and economic data |
| `sdr_usd_rate` | `number` | Yes | Current SDR to USD exchange rate (e.g. 1.33) |
| `total_imf_sdrs` | `number` | No | Total IMF SDR allocation pool in SDR units (default: 660 billion) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "imf_sdr_allocation_tracker",
  "arguments": {
    "country_data": {},
    "sdr_usd_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "imf_sdr_allocation_tracker"`.
