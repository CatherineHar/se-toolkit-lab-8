# Dockerfile for nanobot gateway

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Install nanobot-ai from URL
RUN uv venv && uv pip install "nanobot-ai @ https://github.com/HKUDS/nanobot/archive/e7d371ec1e6531b28898ec2c869ef338e8dd46ec.zip"

# ---
# Stage 2: runtime image
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Accept build args for user
ARG APP_UID=1000
ARG APP_GID=1000

# Create user with specified UID/GID
RUN groupadd --system --gid "${APP_GID}" appgroup \
    && useradd --system --gid "${APP_GID}" --uid "${APP_UID}" --create-home appuser

# Copy the venv from builder
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

USER appuser

CMD ["python", "/app/nanobot/entrypoint.py"]
