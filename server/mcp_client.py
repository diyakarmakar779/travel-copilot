import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

async def run_query():
    server = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            
            await session.initialize()

            result = await session.call_tool(
                "itinerary",
                {"destination": "Coorg", "days": 2}
            )

            return result


if __name__ == "__main__":
    result = asyncio.run(run_query())
    print(result)