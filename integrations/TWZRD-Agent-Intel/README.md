# CrewAI + TWZRD Agent Intel

## Introduction

This example shows how CrewAI agents can use the [TWZRD Agent Intel](https://intel.twzrd.xyz) MCP server to perform **Solana agent trust-scoring** before authorizing x402 micropayments.

TWZRD Agent Intel is a zero-install MCP server that scores Solana AI agent wallets based on on-chain behavior — payment history, first-seen date, repeat interactions, and more. It natively supports the [x402 payment protocol](https://x402.org) for paid trust receipts.

## Tools Available

| Tool | Description | Cost |
|------|-------------|------|
| `score_agent(wallet)` | On-chain trust score (0–1) | Free |
| `preflight_check(wallet)` | Full preflight before x402 payment | Free |
| `get_trust_receipt(wallet)` | Signed trust receipt | HTTP 402 (paid) |

## Running the Example

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the example**:
   ```bash
   python main.py
   ```

No API key or configuration needed — the MCP server is publicly accessible.

## MCP Configuration

Add to your MCP client config to use TWZRD Agent Intel in any MCP-compatible tool:

```json
{
  "mcpServers": {
    "twzrd-agent-intel": {
      "url": "https://intel.twzrd.xyz/mcp"
    }
  }
}
```

## What This Example Does

A CrewAI `Agent` with the role of "Solana Agent Trust Analyst" is given the TWZRD tools. It:

1. Calls `score_agent` to get a trust score for a target wallet
2. Runs `preflight_check` for full due diligence
3. Returns an APPROVE or REJECT recommendation with reasoning

## License

MIT
