# Project Map

## apps/users/models.py

Contains:
- User
- AccountDeletionRequest

## apps/users/services.py

Contains:
- Firebase token verification
- Firebase user creation
- JWT issuance
- username generation

## apps/users/views.py

Contains API endpoints:
- Firebase authentication
- current user profile
- account deletion
- deletion cancellation

## apps/users/serializers.py

User profile serialization and validation.

## apps/users/management/commands/deleteusers.py

Deletes accounts whose deletion grace period has expired.

## apps/users/urls.py

User/auth API routing.

## config/settings.py

Django, DRF, JWT, database and environment configuration.

## config/urls.py

Global routing:
- Admin
- Swagger/OpenAPI
- user API

## Docker

Dockerfile:
- base
- dev
- prod

docker-compose.yml:
shared services

docker-compose.dev.yml:
development overrides

docker-compose.prod.yml:
production overrides