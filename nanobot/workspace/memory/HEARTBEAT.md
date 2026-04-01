# Heartbeat Tasks

Tasks processed periodically by nanobot.

## Active Tasks

- [ ] **LMS Health Check** (every 2 minutes)
  - Check `logs_error_count` for LMS/Learning Management Service (last 2 min)
  - If errors exist: search logs, extract trace_id, fetch trace details
  - Post summary to webchat channel (chat_id: 13c636b1-65fc-4cf1-91ea-f4d8ab008904)
  - If no errors: report "System looks healthy"
