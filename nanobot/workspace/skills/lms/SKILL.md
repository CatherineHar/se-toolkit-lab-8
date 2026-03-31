---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use LMS MCP tools to answer questions about the Learning Management System. Always prefer live data from the LMS backend over cached or hardcoded information.

## Available Tools

| Tool | When to Use |
|------|-------------|
| `lms_health` | Check if the LMS backend is healthy and get total item count |
| `lms_labs` | List all available labs — use first when user asks about labs |
| `lms_learners` | List all registered learners in the system |
| `lms_pass_rates` | Get pass rates for a specific lab (requires `lab` parameter) |
| `lms_timeline` | Get submission timeline for a specific lab (requires `lab` parameter) |
| `lms_groups` | Get group performance for a specific lab (requires `lab` parameter) |
| `lms_top_learners` | Get top learners for a specific lab (requires `lab` parameter, optional `limit`) |
| `lms_completion_rate` | Get completion rate (passed/total) for a specific lab (requires `lab` parameter) |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline when data appears stale or empty |

## Strategy

### Answering Lab Questions

1. **Start with `lms_labs`** when the user asks about available labs or which labs exist
2. **For comparisons** (e.g., "lowest pass rate", "best performing lab"):
   - First call `lms_labs` to get all lab IDs
   - Then call the relevant metric tool (`lms_completion_rate`, `lms_pass_rates`) for each lab
   - Compare results and report the answer
3. **For specific lab queries** (e.g., "how is lab-03 doing?"):
   - Call multiple tools in parallel: `lms_pass_rates`, `lms_timeline`, `lms_groups`, `lms_top_learners`
   - Synthesize a comprehensive answer

### Handling Empty or Stale Data

- If `lms_labs` returns empty or zero items, call `lms_sync_pipeline` to refresh data
- The sync may timeout but still complete in the background — verify by calling `lms_labs` again
- If all metrics show zero (0.0 completion rate, 0 submissions), inform the user that no data is recorded yet

### Response Formatting

- **Lab names**: Use the exact lab ID from the API (e.g., `lab-01`, `lab-02`)
- **Percentages**: Format as percentages (e.g., "75%" not "0.75")
- **Dates**: Preserve the date format returned by the API
- **Rankings**: Present as numbered lists with clear labels

### Authentication

- The MCP server handles authentication using `NANOBOT_LMS_API_KEY` from the environment
- Do not ask the user for API credentials
- If authentication fails, report the error and suggest checking the MCP server configuration

## Examples

**"What labs are available?"** → Call `lms_labs`, list results

**"Which lab has the lowest pass rate?"** → Call `lms_labs`, then `lms_completion_rate` for each lab, compare and report

**"How are students doing in lab-04?"** → Call `lms_pass_rates`, `lms_timeline`, `lms_top_learners` for `lab-04`

**"Is the LMS working?"** → Call `lms_health`, report status and item count
