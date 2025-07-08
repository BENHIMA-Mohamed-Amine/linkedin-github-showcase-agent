from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from tools.tools import register_tools

# Initialize FastMCP server with correct name
mcp = FastMCP("github-linkedin-showcase")


def main():
    print("Hello from github-linkedin-project!")
    # Register tools from tools.py
    register_tools(mcp)
    # Start the MCP server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
