# Testing

Every behavior change should include tests.

Run:

python manage.py test apps.users

Current test suite covers:
- Firebase authentication
- user creation
- JWT authentication
- profile retrieval
- profile update
- account deletion
- deletion cancellation
- deleteusers management command

External Firebase calls must be mocked.

Tests must never depend on the real Firebase API.

Before considering a task complete:

1. Tests pass.
2. Django system check passes.
3. Ruff passes.