FROM python:3.12-slim AS base

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

# Можно не запускать проект отсюда, для гибкости можно вынести в докер композ файл
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# ---- prod ----
FROM base AS prod

RUN uv sync --frozen --no-dev

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]