from mcp.server.fastmcp import FastMCP
from tools.itinerary import generate_itinerary
from tools.captions import generate_captions
from tools.reels import suggest_reels

# Initialize FastMCP
mcp = FastMCP("Travel Copilot")

# Tool 1: Itinerary
@mcp.tool()
def itinerary(destination: str, days: int):
    """Generate a travel itinerary"""
    return generate_itinerary(destination, days)

# Tool 2: Captions
@mcp.tool()
def captions(destination: str):
    """Generate Instagram captions"""
    return generate_captions(destination)

# Tool 3: Reels
@mcp.tool()
def reels(destination: str):
    """Generate reel ideas"""
    return suggest_reels(destination)

if __name__ == "__main__":
    # Start the MCP server (stdio only)
    mcp.run()