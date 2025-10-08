# 1. Start with the slim Python base image
FROM python:3.12

# 2. Install uv directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# 3. Set the working directory
WORKDIR /app

# 4. (OPTIMIZATION) Copy dependency files first to leverage layer caching.
COPY pyproject.toml uv.lock ./


RUN uv venv && . .venv/bin/activate && uv sync --no-cache


COPY . .


CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

    


