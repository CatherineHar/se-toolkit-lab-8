## Task 1A — Bare agent

### Checkpoint Question 1: "What is the agentic loop?"

**Agent Response:**

The **agentic loop** is the fundamental cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these stages:

1. **Perceive** — Gather information from the environment (user input, tool outputs, file contents, API responses, etc.)
2. **Reason** — Analyze the information, plan next steps, and decide what action to take
3. **Act** — Execute the chosen action (call a tool, write a file, run a command, send a message, etc.)
4. **Observe** — Receive feedback from the action (success, error, output data)
5. **Repeat** — Loop back to step 1 with the new information until the task is complete

This loop enables agents to:
- Break complex tasks into smaller steps
- Adapt based on intermediate results
- Recover from errors by trying alternative approaches
- Work autonomously without constant human guidance

In my case, each time I respond to you, I'm running through this loop: I perceive your question, reason about what tools or knowledge I need, act by calling tools or generating text, observe the results, and continue until I can provide a complete answer.

The quality of an agent depends on how well it executes each stage—especially the reasoning step, which determines whether it chooses effective actions and knows when to stop.

---

### Checkpoint Question 2: "What labs are available in our LMS?"

**Agent Response:**

Based on my exploration, here are the available labs in this LMS:

**Required Labs (4 tasks)**

1. Task 1 — Set Up the Agent: Install nanobot, configure Qwen API, add MCP tools, write skill prompt
2. Task 2 — Deploy and Connect a Web Client: Dockerize nanobot, add WebSocket channel + Flutter chat UI
3. Task 3 — Give the Agent New Eyes: Explore observability data, write log/trace MCP tools
4. Task 4 — Diagnose a Failure and Make the Agent Proactive: Investigate a failure, schedule in-chat health checks, fix a planted bug

**Optional Labs (1 task)**

1. Task 1 — Add a Telegram Bot Client: Same agent, different interface

This is Lab 8 titled "The Agent is the Interface" — where you build an AI agent (nanobot) as a natural-language interface to the LMS system. The agent can answer questions like "which lab has the lowest pass rate?" or "any errors in the last hour?" by calling MCP tools to query the backend and observability data.

*Note: The bare agent did not return real backend data. It inspected local repo files (lab/tasks/required, lab/tasks/optional, README.md) and answered from documentation instead of querying a live LMS backend.*

---

## Task 1B — Agent with LMS tools

### Configuration

- Installed MCP server: `uv add mcp-lms --editable ../mcp/mcp-lms`
- Added MCP server config to `config.json`:
  ```json
  {
    "mcpServers": {
      "lms": {
        "command": "python",
        "args": ["-m", "mcp_lms"],
        "env": {
          "NANOBOT_LMS_BACKEND_URL": "http://localhost:42002",
          "NANOBOT_LMS_API_KEY": "my-secret-api-key"
        }
      }
    }
  }
  ```

### Checkpoint Question 1: "What labs are available?"

**Agent Response:**

Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Is there a specific lab you'd like to know more about?

*The agent called `mcp_lms_lms_labs` and returned real lab names from the backend.*

---

### Checkpoint Question 2: "Is the LMS backend healthy?"

**Agent Response:**

Yes, the LMS backend is healthy. It currently has 56 items in the system.

*The agent called `mcp_lms_lms_health` and reported the actual item count from the LMS backend.*

---

## Task 1C — Skill prompt

### Skill File

Created `nanobot/workspace/skills/lms/SKILL.md` with:
- Frontmatter: `name: lms`, `description: Use LMS MCP tools for live course data`, `always: true`
- Tool reference table with 9 LMS tools and when to use each
- Strategy section for answering lab questions, handling empty data, and response formatting
- Authentication guidance
- Example queries

### Checkpoint Question: "Show me the scores" (without specifying a lab)

**Agent Response:**

Here's a summary of the scores across all labs:

**Lab Completion Rates**

| Lab    | Title                          | Completion Rate | Passed / Total |
|--------|--------------------------------|-----------------|----------------|
| lab-01 | Products, Architecture & Roles | 100%            | 258/258        |
| lab-02 | Run, Fix, and Deploy a Backend Service | 89.1%   | 131/147        |
| lab-03 | Backend API: Explore, Debug, Implement, Deploy | 89.1% | 156/175 |
| lab-04 | Testing, Front-end, and AI Agents | 97.2%        | 239/246        |
| lab-05 | Data Pipeline and Analytics Dashboard | 98.8%    | 247/250        |
| lab-06 | Build Your Own Agent           | 98.4%           | 242/246        |
| lab-07 | Build a Client with AI Coding Agent | 99.6%      | 238/239        |
| lab-08 | lab-08                         | 0%              | 0/0 (no submissions) |

**Average Scores by Lab (Key Tasks)**

- **lab-01**: Lab setup (84.2%), Task 0 Git workflow (64.5%), Task 1 Product description (55.1%)
- **lab-02**: Task 1 Run web server (67.9%), Task 2 Fix bug (66.7%), Task 4 Deploy to VM (56.2%)
- **lab-03**: Task 1 Explore API (63.5%), Task 2 Debug interactions (66.4%), Task 4 Deploy to VM (43.9%)
- **lab-04**: Task 1 Observe components (61.0%), Task 2 Back-end testing (59.8%), Task 3 Add Front-end (56.3%)
- **lab-05**: Task 1 Data Pipeline (73.5%), Task 2 Analytics Endpoints (64.4%), Task 3 Dashboard (73.0%)
- **lab-06**: Task 1 Call LLM (61.2%), Task 2 Documentation Agent (73.9%), Task 3 System Agent (42.9%)
- **lab-07**: Task 1 Plan/Scaffold (76.7%), Task 2 Backend Integration (66.8%), Task 3 NL Routing (58.8%), Task 4 Containerize (66.6%)
- **lab-08**: No data yet

Would you like more detailed information about any specific lab, such as top learners, group performance, or submission timeline?

*The skill prompt teaches the agent to handle ambiguous queries by listing all available options with their scores. At this stage, plain text output is used; Task 2 will add structured UI for web clients.*

---

### Additional Test: "Which lab has the lowest pass rate?"

**Agent Response:**

Based on the completion rates:

| Lab    | Completion Rate | Passed | Total |
|--------|-----------------|--------|-------|
| lab-01 | 100.0%          | 258    | 258   |
| lab-02 | 89.1%           | 131    | 147   |
| lab-03 | 89.1%           | 156    | 175   |
| lab-04 | 97.2%           | 239    | 246   |
| lab-05 | 98.8%           | 247    | 250   |
| lab-06 | 98.4%           | 242    | 246   |
| lab-07 | 99.6%           | 238    | 239   |
| lab-08 | 0.0%            | 0      | 0     |

lab-02 and lab-03 are tied for the lowest pass rate at 89.1%.

Note: lab-08 shows 0.0% but has no submissions yet (0 total), so it's not a meaningful comparison.

*The skill prompt improved the agent's response by adding a formatted markdown table and contextual notes about lab-08 having no submissions.*
