# Base
FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_PREFERENCE=only-system \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

# Development
FROM base AS dev

RUN uv sync --frozen

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production
FROM base AS prod

RUN uv sync --frozen --no-dev --no-editable

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Если Django + Gunicorn, например:
# CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]