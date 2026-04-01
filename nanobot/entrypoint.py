#!/usr/bin/env python3
"""Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config at runtime, then launches nanobot gateway.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    # Install workspace packages at runtime from mounted volumes
    mcp_dir = Path("/app/mcp")
    webchat_dir = Path("/app/nanobot-websocket-channel")

    # Install all packages together so dependencies resolve correctly
    print(f"Installing workspace packages...", file=sys.stderr)
    packages = [
        str(mcp_dir / "mcp-lms"),
        str(mcp_dir / "mcp-obs"),
        str(webchat_dir / "nanobot-channel-protocol"),
        str(webchat_dir / "nanobot-webchat"),
        str(webchat_dir / "mcp-webchat"),
    ]
    result = subprocess.run(["pip", "install", "--target=/app/.venv/lib/python3.14/site-packages"] + packages, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Workspace packages installed", file=sys.stderr)
    else:
        print(f"Note: Package installation had issues: {result.stderr[:300]}", file=sys.stderr)
    
    # Paths
    app_dir = Path("/app")
    nanobot_dir = app_dir / "nanobot"
    config_src = nanobot_dir / "config.json"
    config_resolved = Path("/tmp/config.resolved.json")
    workspace_dir = nanobot_dir / "workspace"

    # Read base config
    with open(config_src) as f:
        config = json.load(f)

    # Override from environment variables
    # LLM provider config
    if llm_api_key := os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base := os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = llm_api_base
    if llm_api_model := os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = llm_api_model

    # Gateway config
    if gateway_host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config["gateway"]["host"] = gateway_host
    if gateway_port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config["gateway"]["port"] = int(gateway_port)

    # Webchat channel config
    webchat_config = config["channels"].get("webchat", {})
    webchat_config["enabled"] = True
    if webchat_host := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"):
        webchat_config["host"] = webchat_host
    if webchat_port := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT"):
        webchat_config["port"] = int(webchat_port)
    if access_key := os.environ.get("NANOBOT_ACCESS_KEY"):
        webchat_config["accessKey"] = access_key
    config["channels"]["webchat"] = webchat_config

    # MCP servers config
    config["tools"]["mcpServers"] = {
        "lms": {
            "command": "python",
            "args": ["-m", "mcp_lms"],
            "env": {
                "NANOBOT_LMS_BACKEND_URL": os.environ.get("NANOBOT_LMS_BACKEND_URL", ""),
                "NANOBOT_LMS_API_KEY": os.environ.get("NANOBOT_LMS_API_KEY", ""),
            },
        },
        "obs": {
            "command": "python",
            "args": ["-m", "mcp_obs"],
            "env": {
                "NANOBOT_VICTORIALOGS_URL": os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"),
                "NANOBOT_VICTORIATRACES_URL": os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428"),
            },
        },
        "webchat": {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
        },
    }

    # Write resolved config
    with open(config_resolved, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {config_resolved}", file=sys.stderr)

    # Launch nanobot gateway - use PATH to find nanobot in venv
    os.environ["PATH"] = "/app/.venv/bin:" + os.environ.get("PATH", "")
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(config_resolved),
            "--workspace",
            str(workspace_dir),
        ],
    )


if __name__ == "__main__":
    main()
