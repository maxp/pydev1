FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# TODO: copy only really needed files app/* *.toml *.lock
COPY . /app
WORKDIR /app

# NOTE: use byte code compilation?
ENV UV_COMPILE_BYTECODE=1
RUN uv sync --frozen --no-cache


CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0"]
# "--app-dir", "/app", 

# fastapi run app/main.py --port 8000 --host 0.0.0.0
