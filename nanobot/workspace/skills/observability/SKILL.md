---
name: observability
description: Use observability MCP tools to investigate errors and traces
always: true
---

# Observability Skill

Use the observability MCP tools (`logs_*` and `traces_*`) to investigate system health, errors, and request traces. Always prefer live observability data over speculation.

## Available Tools

| Tool | When to Use |
|------|-------------|
| `logs_error_count` | First step when user asks about errors — quick count without details |
| `logs_search` | Search for specific log entries by keyword, service, severity, or time range |
| `traces_list` | List recent traces for a service to find relevant trace IDs |
| `traces_get` | Fetch full trace details when you have a trace ID from logs |
| `lms_health` | Quick health check of the LMS backend |

## Investigation Strategy

### When asked about errors (e.g., "Any errors in the last hour?")

1. **Start with `logs_error_count`** — Get a quick count of errors by service
   - If zero errors: Report "No errors found in the time window"
   - If errors exist: Proceed to step 2

2. **Use `logs_search`** — Find relevant error logs
   - Query pattern: `service.name:"<service>" severity:ERROR _time:<window>`
   - Look for `trace_id` fields in error logs

3. **If trace_id found, use `traces_get`** — Fetch full trace context
   - This shows the complete request path and where it failed

4. **Summarize findings** — Don't dump raw JSON
   - State the error count
   - Describe the error type and affected service
   - If trace analyzed, explain the failure point

### When asked "What went wrong?" or "Why is the system failing?"

**Multi-step investigation flow:**

1. **Check error count first**: `logs_error_count(service="Learning Management Service", minutes=10)`
   - This tells you if there are recent errors and how many

2. **Search for error details**: `logs_search(query='_time:10m service.name:"Learning Management Service" severity:ERROR', limit=5)`
   - Look for error messages and extract `trace_id` from the results

3. **Fetch the failing trace**: `traces_get(trace_id="<extracted_id>")`
   - Examine the span hierarchy to find where the failure occurred
   - Look for spans with error tags or unusually long durations

4. **Correlate with LMS health**: Call `lms_health()` to check current backend status

5. **Provide a diagnosis summary**:
   - "The system is experiencing database connection failures"
   - "X errors detected in the last Y minutes"
   - "The failure occurs at the [span name] step"
   - "Root cause: [specific error from trace]"

### When asked about a specific service health

1. Check `logs_error_count` for that service
2. If errors exist, use `logs_search` with service filter
3. Extract trace IDs and use `traces_get` for context

### Proactive Health Monitoring

For scheduled health checks (via HEARTBEAT.md):
1. Call `lms_health()` to check backend status
2. Call `logs_error_count(minutes=5)` for recent errors
3. Report any issues found to the chat channel
