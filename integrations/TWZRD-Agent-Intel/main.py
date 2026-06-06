"""
CrewAI + TWZRD Agent Intel MCP Integration

This example shows how CrewAI agents can use the TWZRD Agent Intel MCP server
to perform Solana agent trust-scoring before authorizing x402 payments.

The TWZRD Agent Intel MCP server exposes:
- score_agent(wallet): trust score for a Solana wallet (free)
- preflight_check(wallet): full preflight before payment (free)
- get_trust_receipt(wallet): signed trust receipt via HTTP 402 (paid)

Usage:
    pip install -r requirements.txt
    python main.py
"""

import asyncio

from crewai import Agent, Crew, Process, Task
from crewai_tools import MCPServerAdapter


async def main():
    # Connect to TWZRD Agent Intel MCP server (zero-install, streamable-HTTP)
    mcp_server_params = {
        "url": "https://intel.twzrd.xyz/mcp",
    }

    with MCPServerAdapter(mcp_server_params) as tools:
        # CrewAI agent with access to TWZRD trust-scoring tools
        trust_analyst = Agent(
            role="Solana Agent Trust Analyst",
            goal=(
                "Score Solana agent wallets for trustworthiness before authorizing "
                "x402 payments. Flag any wallet with a trust score below 0.5."
            ),
            backstory=(
                "You are an autonomous trust analyst specializing in Solana agent "
                "ecosystems. You use on-chain data to assess whether an agent "
                "has a reliable payment history and should be trusted with paid APIs."
            ),
            tools=tools,
            verbose=True,
        )

        # Example: score a known active agent wallet
        task = Task(
            description=(
                "Use the score_agent tool to check the trust score for wallet "
                "D1QkbFJKiPsymJ65RKHhF6DFB8sPMfpBaFBzuHKfJGWi. "
                "Then run preflight_check on the same wallet. "
                "Report: trust score, payment history summary, and a recommendation "
                "on whether to accept x402 payments from this agent."
            ),
            expected_output=(
                "A trust report with: score (0-1), number of prior x402 payments, "
                "and a APPROVE or REJECT recommendation with reasoning."
            ),
            agent=trust_analyst,
        )

        crew = Crew(
            agents=[trust_analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        print("\n=== Trust Analysis Result ===")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
