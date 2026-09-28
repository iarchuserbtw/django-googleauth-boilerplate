FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

ENV PATH="/app/.venv/bin:$PATH"


# ---- dev ----
FROM base AS dev

RUN uv sync --frozen

COPY . .


# ---- prod ----
FROM base AS prod

RUN uv sync --frozen --no-dev

COPY . .

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]