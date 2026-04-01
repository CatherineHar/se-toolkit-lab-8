# Heartbeat Tasks

This file is checked every 30 minutes by your nanobot agent.
Add tasks below that you want the agent to work on periodically.

If this file has no tasks (only headers and comments), the agent will skip the heartbeat.

## Active Tasks

<!-- Add your periodic tasks below this line -->

### System Health Check

Every 30 minutes, check the LMS backend health and report any issues:

1. Call `lms_health` to check if the backend is healthy
2. Call `logs_error_count(service="Learning Management Service", minutes=30)` to check for recent errors
3. If errors are found:
   - Use `logs_search` to get error details
   - Extract any trace IDs and use `traces_get` for context
   - Report findings to the chat channel with a summary

Report format:
- If healthy: "✅ System health check passed. LMS backend is healthy with X items. No errors in the last 30 minutes."
- If errors found: "⚠️ System health check found X errors. [Summary of issues]"

## Completed

<!-- Move completed tasks here or delete them -->

