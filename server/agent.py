import asyncio
import json
import re

from server.ai_client import call_llm
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

# MCP Server command parameters (stdio)
server_params = StdioServerParameters(
    command="python",
    args=["server/mcp_server.py"]
)

async def run_agent(query: str):
    """
    Runs the Travel Copilot agent:
    1. Calls the LLM to decide which tools to use
    2. Executes the tools via MCP
    3. Generates human-readable response
    """
    # Step 1: Ask LLM which tools to use
    llm_output = call_llm(query, mode="decision")
    print("\nLLM Decision:", llm_output)

    # Extract JSON from LLM output
    match = re.search(r"\[.*\]", llm_output, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM output")

    decisions = json.loads(match.group(0))

    # Step 2: Connect to MCP server via stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            results = []
            for decision in decisions:
                tool_name = decision["tool"]
                args = decision["args"]

                result = await session.call_tool(tool_name, args)
                results.append(result)

            # Step 3: Convert tool results to human-readable output
            final_prompt = f"""
            User asked: {query}

            Tool results:
            {results}

            Write a polished, engaging response like a travel influencer + guide.

            Rules:
            - No JSON
            - No mentioning tools
            - Make it aesthetic, slightly emotional, and structured
            - Add emojis where relevant
            """

            final_response = call_llm(final_prompt, mode="final")
            return final_response

# Optional: standalone test
if __name__ == "__main__":
    query = input("Ask Travel Copilot: ")
    result = asyncio.run(run_agent(query))
    print("\n--- FINAL RESPONSE ---")
    print(result)