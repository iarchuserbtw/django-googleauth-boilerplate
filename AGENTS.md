# Project Instructions

## Project

Django REST API boilerplate using:
- Django
- Django REST Framework
- Firebase Authentication
- SimpleJWT
- PostgreSQL
- Docker
- uv

# Agent Instructions

Before making significant changes, read:

- `docs/architecture.md`
- `docs/project-map.md`
- `docs/conventions.md`
- `docs/testing.md`

Follow the existing architecture and conventions.

## Rules

- Keep views thin.
- Business logic belongs in services or domain models.
- Use serializers for input/output validation.
- Use `get_user_model()` instead of importing User directly where appropriate.
- API endpoints are under `/api/`.
- Authentication uses Firebase for identity verification and SimpleJWT for API sessions.
- Never expose Firebase credentials or Django secrets.
- Do not introduce Celery, Redis, or other infrastructure without a concrete requirement.

## Before changing code

1. Understand the existing implementation.
2. Reuse existing patterns.
3. Avoid unnecessary abstractions.
4. Update tests for changed behavior.
5. Run tests.
6. Run Ruff.

See `docs/conventions.md`.

## Validation

Run:

python manage.py test apps.users
ruff check .