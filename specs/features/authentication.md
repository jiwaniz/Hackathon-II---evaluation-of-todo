# Feature: User Authentication

## Overview

Secure user authentication using **Better Auth with JWT Plugin** for API authorization. Enables multi-user support with strict data isolation.

## Technology Requirements

- **Frontend**: Better Auth with `@better-auth/jwt` plugin explicitly enabled
- **Backend**: FastAPI with `python-jose` for JWT verification using shared `BETTER_AUTH_SECRET`
- **Shared Secret**: Both frontend and backend MUST use identical `BETTER_AUTH_SECRET` environment variable
- **Stateless Verification**: Backend verifies tokens independently without calling frontend

## User Stories

### Registration
- As a visitor, I can create a new account with email and password
- As a visitor, I receive immediate access after registration
- As a visitor, I see validation errors for invalid input

### Login
- As a registered user, I can log in with my email and password
- As a user, I receive a JWT token upon successful login
- As a user, I am redirected to my task dashboard after login
- As a user, I see an error for invalid credentials

### Logout
- As a logged-in user, I can log out from my account
- As a user, my session is invalidated on logout
- As a user, I am redirected to the landing page after logout

### Session Management
- As a user, my session persists across browser refreshes
- As a user, my session expires after 7 days
- As a user, I am prompted to re-login when session expires

## Acceptance Criteria

### Registration
- Email must be valid format
- Email must be unique (not already registered)
- Password must be at least 8 characters
- Password must include at least one number
- Password is stored using secure hashing (never plain text)
- User is automatically logged in after registration
- JWT token is issued immediately

### Login
- Email and password are required
- Credentials are validated against database
- Error message does not reveal which field is incorrect (security)
- JWT token is issued on successful authentication
- Token contains user ID and expiration time
- Token is signed with BETTER_AUTH_SECRET

### Logout
- Current session/token is invalidated
- User is redirected to landing page
- Protected routes become inaccessible

### JWT Token
- Valid for 7 days from issuance
- Contains: user_id, email, issued_at, expires_at
- Signed with shared BETTER_AUTH_SECRET
- Verified on every API request
- Refresh mechanism before expiration

## Security Requirements

### Password Security
- Minimum 8 characters
- At least one number
- Stored with bcrypt or Argon2 hashing
- Never transmitted in plain text
- Never logged or exposed in errors

### Token Security
- Transmitted only via HTTPS
- Stored in httpOnly cookies (frontend)
- Included in Authorization header for API calls
- Secret key shared between frontend and backend
- Secret key stored in environment variables

### API Protection
- All `/api/{user_id}/*` routes require valid JWT (except auth routes)
- The `{user_id}` in URL MUST match the `sub` claim in JWT token
- Invalid/expired token returns 401 Unauthorized
- Missing token returns 401 Unauthorized
- URL `{user_id}` mismatch with JWT `sub` returns 403 Forbidden
- Cross-user access attempts return 403 Forbidden

## Integration with Better Auth

### Frontend (Next.js)
```
- Install: better-auth, @better-auth/jwt
- Configure in lib/auth.ts
- Use session hooks in components
- Attach token to API requests
```

### Backend (FastAPI)
```
- Install: python-jose, passlib
- Create JWT verification middleware
- Extract user_id from token
- Apply to all protected routes
```

### Shared Configuration
```
Environment Variables:
- BETTER_AUTH_SECRET: Shared JWT signing key
- BETTER_AUTH_URL: Frontend auth URL
- DATABASE_URL: Neon connection string
```

## API Reference

See [REST Endpoints](../api/rest-endpoints.md) for auth routes:
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Authenticate
- `POST /api/auth/logout` - End session
- `GET /api/auth/session` - Get current session

## UI Reference

See [Pages](../ui/pages.md) for:
- Landing page with auth options
- Login page
- Registration page
- Protected dashboard layout
