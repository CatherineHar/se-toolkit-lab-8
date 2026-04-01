#!/usr/bin/env python3
"""MCP Observability Server entry point."""

from __future__ import annotations

import asyncio
import os
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from mcp_obs.observability import ObservabilityClient
from mcp_obs.server import TOOL_SPECS, TOOLS_BY_NAME


def create_server() -> Server:
    """Create the MCP observability server."""
    server = Server("mcp-obs")
    client = ObservabilityClient(
        logs_url=os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"),
        traces_url=os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428"),
    )

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [spec.as_tool() for spec in TOOL_SPECS]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list:
        if name not in TOOLS_BY_NAME:
            raise ValueError(f"Unknown tool: {name}")

        spec = TOOLS_BY_NAME[name]
        model = spec.model(**arguments)
        result = await spec.handler(client, model)

        # Convert result to MCP response format
        import json
        return [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]

    return server


async def main() -> None:
    """Run the MCP server."""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
