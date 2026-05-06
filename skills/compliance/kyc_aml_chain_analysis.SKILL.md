---
skill: kyc_aml_chain_analysis
category: compliance
description: Performs on-chain KYC/AML screening by cross-referencing wallet addresses against OFAC-style sanctioned address lists and heuristic risk indicators including mixer usage patterns, rapid fund movement (under 24h), and known bad actor address clusters. Supports TON, Solana, and Ethereum chains.
tier: premium
inputs: wallet_addresses, chain
---

# Kyc Aml Chain Analysis

## Description
Performs on-chain KYC/AML screening by cross-referencing wallet addresses against OFAC-style sanctioned address lists and heuristic risk indicators including mixer usage patterns, rapid fund movement (under 24h), and known bad actor address clusters. Supports TON, Solana, and Ethereum chains. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `wallet_addresses` | `array[string]` | Yes | List of wallet addresses to screen against OFAC-style sanctioned address lists and risk indicators |
| `chain` | `string` | No | Blockchain to query: "ethereum" (default), "solana", or "ton" |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "kyc_aml_chain_analysis",
  "arguments": {
    "wallet_addresses": ["0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe"],
    "chain": "ethereum"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "kyc_aml_chain_analysis"`.
