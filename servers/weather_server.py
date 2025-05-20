
# weather_server.py
from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather", port=000)

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return "It's always windy in Puerto Madryn"
if __name__ == "__main__":
    mcp.run(transport="streamable-http")