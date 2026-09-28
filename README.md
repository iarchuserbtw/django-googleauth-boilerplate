# Django Firebase Auth Boilerplate

A Django REST API boilerplate with **Firebase Authentication**, **JWT**, **PostgreSQL**, Docker and API documentation.

> The project is currently under active development.

## Features & Roadmap

| Feature | Status | Date |
|---|:---:|:---:|
| Firebase Authentication | ✅ Done | — |
| User registration | ✅ Done | — |
| User login | ✅ Done | — |
| Get user profile | ✅ Done | — |
| Update user profile | ✅ Done | — |
| Docker image | ✅ Done | 25.09.26 |
| Docker Compose configuration | ✅ Done | 25.09.26 |
| Postman API documentation | ✅ Done | 26.09.26 |
| Account deletion flow | ✅ Done | 28.09.26 |
| Account deletion management command (`deleteusers`) | ✅ Done | 28.09.26 |
| User last activity tracking | 🟡 In Progress | — |
| Tests | ⚪ Not Started | — |
| Gunicorn / Uvicorn production setup | ✅ Done | 28.09.26 |
| CI/CD | ⚪ Not Started | — |
| Production secrets management | ⚪ Not Started | — |
| MFA setup documentation | ⚪ Not Started | — |
| Project architecture & AI coding guidelines | ⚪ Not Started | — |
| Docker `.dockerignore` investigation | 🟡 In Progress | — |

### Status

- ✅ **Done**
- 🟡 **In Progress**
- ⚪ **Not Started**

## Tech Stack

- Python
- Django
- Django REST Framework
- Firebase Authentication
- Simple JWT
- PostgreSQL
- Docker & Docker Compose
- uv
- drf-spectacular / OpenAPI
- Postman

## Getting Started

### Local Development

Install dependencies:

```bash
uv sync
```

Activate the virtual environment on Linux:

```bash
source .venv/bin/activate
```

Apply database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://localhost:8000
```

## Docker

Start the development environment:

```bash
docker compose \
  -f docker-compose.yml \
  -f docker-compose.dev.yml \
  up --build
```

Run Django commands inside the API container:

```bash
docker compose \
  -f docker-compose.yml \
  -f docker-compose.dev.yml \
  exec api python manage.py <command>
```

## Account Deletion

Users can request account deletion through the API.

Instead of deleting the account immediately, the request is stored and processed after the configured grace period.

Expired deletion requests can be processed with:

```bash
python manage.py deleteusers
```

The command finds expired, non-cancelled deletion requests and removes the corresponding accounts.

## API Documentation

Interactive API documentation is available through the project OpenAPI/Swagger configuration.

### Postman

[Open Postman API Documentation](https://documenter.getpostman.com/view/52943131/2sBYB4K6a8)

## Project Structure

```text
apps/
└── users/
    ├── management/
    │   └── commands/
    │       └── deleteusers.py
    ├── migrations/
    ├── admin.py
    ├── middleware.py
    ├── models.py
    ├── serializers.py
    ├── services.py
    ├── urls.py
    └── views.py

config/
├── settings.py
├── urls.py
└── wsgi.py

Dockerfile
docker-compose.yml
docker-compose.dev.yml
docker-compose.prod.yml
pyproject.toml
```

## Development

The project is intended to provide a reusable foundation for Django applications that require Firebase-based authentication and a Django REST API.

The current focus is on:

- reliability and automated tests;
- production-ready Docker configuration;
- CI/CD;
- account lifecycle management;
- clean API documentation.