# Development Conventions

## API

Use REST-style URLs.

Examples:

GET /api/users/me/
PATCH /api/users/me/

POST /api/users/me/deletion/
POST /api/users/me/deletion/cancel/

Avoid action URLs such as:

/delete-user/
/update-user/
/cancel-delete/

## Authentication

Protected endpoints use:

IsAuthenticated

Public authentication endpoints explicitly use:

AllowAny

Firebase ID tokens must be verified through:

apps.users.services.verify_id_token

Do not call Firebase Admin directly from views.

## Database

Production/development Docker environment:
PostgreSQL

Local fallback:
SQLite

Never automatically fall back to SQLite after a PostgreSQL connection failure.

## Environment

Secrets must come from environment variables.

Never commit:
- SECRET_KEY
- Firebase credentials
- database passwords

## Dependencies

Do not add a dependency when the same task can reasonably be solved with existing dependencies or the Python/Django standard library.