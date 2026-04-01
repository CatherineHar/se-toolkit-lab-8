"""Observability tools for VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import httpx
from pydantic import BaseModel, Field


class LogsSearchQuery(BaseModel):
    query: str = Field(description="LogsQL query string (e.g., 'service.name:\"LMS\" severity:ERROR')")
    limit: int = Field(default=20, ge=1, le=100, description="Max results to return")


class LogsErrorCountQuery(BaseModel):
    service: str = Field(default="", description="Service name filter (empty = all services)")
    minutes: int = Field(default=60, ge=1, le=1440, description="Time window in minutes")


class TracesListQuery(BaseModel):
    service: str = Field(description="Service name to filter traces")
    limit: int = Field(default=10, ge=1, le=50, description="Max traces to return")


class TracesGetQuery(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


class ObservabilityClient:
    """Client for VictoriaLogs and VictoriaTraces APIs."""

    def __init__(self, logs_url: str = "", traces_url: str = ""):
        self.logs_url = logs_url.rstrip("/") or "http://victorialogs:9428"
        self.traces_url = traces_url.rstrip("/") or "http://victoriatraces:10428"

    async def logs_search(self, query: str, limit: int = 20) -> list[dict]:
        """Search logs using VictoriaLogs query API."""
        url = f"{self.logs_url}/select/logsql/query"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"query": query, "limit": limit})
            response.raise_for_status()
            return response.json()

    async def logs_error_count(self, service: str = "", minutes: int = 60) -> dict:
        """Count errors per service over a time window."""
        time_filter = f"_time:{minutes}m"
        if service:
            query = f'{time_filter} service.name:"{service}" severity:ERROR'
        else:
            query = f"{time_filter} severity:ERROR"
        
        url = f"{self.logs_url}/select/logsql/hits"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"query": query, "step": f"{minutes}m"})
            response.raise_for_status()
            data = response.json()
            
        # Parse hits to get error count
        total_errors = 0
        if data.get("hits"):
            for hit in data["hits"]:
                values = hit.get("values", [])
                total_errors += sum(values) if isinstance(values, list) else 0
                
        return {
            "service": service or "all",
            "time_window_minutes": minutes,
            "total_errors": total_errors,
        }

    async def traces_list(self, service: str, limit: int = 10) -> list[dict]:
        """List recent traces for a service."""
        url = f"{self.traces_url}/select/jaeger/api/traces"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"service": service, "limit": limit})
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])

    async def traces_get(self, trace_id: str) -> dict:
        """Fetch a specific trace by ID."""
        url = f"{self.traces_url}/select/jaeger/api/traces/{trace_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            traces = data.get("data", [])
            return traces[0] if traces else {}
