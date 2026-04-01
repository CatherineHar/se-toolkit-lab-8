"""MCP server for observability tools."""

from __future__ import annotations

import os
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass

from mcp.types import Tool
from pydantic import BaseModel

from mcp_obs.observability import (
    LogsSearchQuery,
    LogsErrorCountQuery,
    TracesListQuery,
    TracesGetQuery,
    ObservabilityClient,
)


class NoArgs(BaseModel):
    """Empty input model for tools that only need server-side configuration."""


ToolPayload = BaseModel | Sequence[BaseModel]
ToolHandler = Callable[[ObservabilityClient, BaseModel], Awaitable[ToolPayload]]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    query = args.query if hasattr(args, "query") else ""
    limit = args.limit if hasattr(args, "limit") else 20
    return await client.logs_search(query, limit)


async def _logs_error_count(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    service = args.service if hasattr(args, "service") else ""
    minutes = args.minutes if hasattr(args, "minutes") else 60
    return await client.logs_error_count(service, minutes)


async def _traces_list(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    service = args.service if hasattr(args, "service") else ""
    limit = args.limit if hasattr(args, "limit") else 10
    return await client.traces_list(service, limit)


async def _traces_get(client: ObservabilityClient, args: BaseModel) -> ToolPayload:
    trace_id = args.trace_id if hasattr(args, "trace_id") else ""
    return await client.traces_get(trace_id)


TOOL_SPECS = (
    ToolSpec(
        "logs_search",
        "Search logs in VictoriaLogs using LogsQL query syntax. Use for finding specific log entries by keyword, service, severity, or time range.",
        LogsSearchQuery,
        _logs_search,
    ),
    ToolSpec(
        "logs_error_count",
        "Count errors per service over a time window. Use to quickly check if there are recent errors before diving into detailed log search.",
        LogsErrorCountQuery,
        _logs_error_count,
    ),
    ToolSpec(
        "traces_list",
        "List recent traces for a service from VictoriaTraces. Returns trace IDs and span summaries.",
        TracesListQuery,
        _traces_list,
    ),
    ToolSpec(
        "traces_get",
        "Fetch a specific trace by ID from VictoriaTraces. Use trace_id from logs to get full request context.",
        TracesGetQuery,
        _traces_get,
    ),
)

TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
