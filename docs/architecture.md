# Architecture

## Authentication flow

Client
→ Firebase Authentication
→ Firebase ID Token
→ POST /api/auth/firebase/
→ Django verifies Firebase token
→ User is created/found
→ SimpleJWT access + refresh tokens are issued

Firebase proves identity.

SimpleJWT is used for authentication inside the Django API.

Do not replace this flow without an explicit architectural reason.

## Layers

### Views

Responsible for:
- HTTP requests
- permissions
- calling application logic
- HTTP responses

Views should not contain substantial business logic.

### Serializers

Responsible for:
- validation
- serialization
- deserialization

### Services

`apps/users/services.py`

Responsible for operations such as:
- Firebase verification
- user creation
- token issuance

### Models

Contain persistent state and behavior closely related to that state.

Example:

AccountDeletionRequest.schedule()
AccountDeletionRequest.cancel()

## Account deletion

User requests deletion
→ Firebase identity is reverified
→ AccountDeletionRequest is created
→ user.is_active = False
→ grace period
→ `python manage.py deleteusers`
→ expired accounts are deleted

Cancellation:
Firebase reauthentication
→ locate user by firebase_uid
→ deletion_request.cancel()
→ user.is_active = True