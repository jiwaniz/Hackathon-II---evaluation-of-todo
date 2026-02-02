# REST API Endpoints

## Base URLs

| Environment | URL |
|-------------|-----|
| Development | http://localhost:8000 |
| Production | https://api.{your-domain}.com |

## Authentication

All endpoints except `/api/auth/*` require JWT authentication.

```
Authorization: Bearer <jwt_token>
```

### JWT Verification (FastAPI Middleware)

The FastAPI backend MUST verify JWT tokens independently using the shared `BETTER_AUTH_SECRET`:

1. Extract token from `Authorization: Bearer <token>` header
2. Verify signature using `BETTER_AUTH_SECRET` environment variable
3. Decode payload to extract `user_id` (stored in `sub` claim)
4. Validate `{user_id}` in URL path matches JWT `sub` claim
5. Return 401 for invalid/expired tokens
6. Return 403 if URL `{user_id}` doesn't match JWT `sub`

**Required Environment Variable:**
```
BETTER_AUTH_SECRET=<shared-secret-with-frontend>
```

This enables stateless authentication - the backend verifies tokens without calling the frontend.

## Response Format

### Success Response
```json
{
  "data": { ... },
  "message": "Success message"
}
```

### Error Response
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## Authentication Endpoints

### POST /api/auth/register

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created):**
```json
{
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "created_at": "2026-01-18T00:00:00Z"
    },
    "token": "jwt_token_here"
  },
  "message": "Account created successfully"
}
```

**Errors:**
- 400 Bad Request: Invalid email format or weak password
- 409 Conflict: Email already registered

---

### POST /api/auth/login

Authenticate and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com"
    },
    "token": "jwt_token_here",
    "expires_at": "2026-01-25T00:00:00Z"
  },
  "message": "Login successful"
}
```

**Errors:**
- 401 Unauthorized: Invalid credentials

---

### POST /api/auth/logout

Invalidate current session.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

---

### GET /api/auth/session

Get current session info.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com"
    },
    "expires_at": "2026-01-25T00:00:00Z"
  }
}
```

**Errors:**
- 401 Unauthorized: Invalid or expired token

---

## Task Endpoints

All task endpoints require authentication and use the `{user_id}` path pattern for explicit user scoping.

**Important Security Rule**: The `{user_id}` in the URL MUST match the user ID extracted from the JWT token. Any mismatch MUST return 403 Forbidden.

### GET /api/{user_id}/tasks

List all tasks for the specified user.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| status | string | "all" | Filter: "all", "pending", "completed" |
| priority | string | null | Filter: "high", "medium", "low" |
| tag | string | null | Filter by tag name |
| search | string | null | Search in title and description |
| sort | string | "created_desc" | Sort: "created_desc", "created_asc", "priority", "title" |
| page | int | 1 | Page number |
| limit | int | 20 | Items per page (max 100) |

**Response (200 OK):**
```json
{
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "priority": "high",
        "tags": ["shopping", "home"],
        "created_at": "2026-01-18T10:00:00Z",
        "updated_at": "2026-01-18T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "pages": 3
    }
  }
}
```

---

### POST /api/{user_id}/tasks

Create a new task for the specified user.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "tags": ["shopping", "home"]
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "priority": "high",
    "tags": ["shopping", "home"],
    "created_at": "2026-01-18T10:00:00Z",
    "updated_at": "2026-01-18T10:00:00Z"
  },
  "message": "Task created successfully"
}
```

**Errors:**
- 400 Bad Request: Title missing or too long

---

### GET /api/{user_id}/tasks/{id}

Get a specific task by ID for the specified user.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "priority": "high",
    "tags": ["shopping", "home"],
    "created_at": "2026-01-18T10:00:00Z",
    "updated_at": "2026-01-18T10:00:00Z"
  }
}
```

**Errors:**
- 404 Not Found: Task does not exist
- 403 Forbidden: Task belongs to another user

---

### PUT /api/{user_id}/tasks/{id}

Update a task for the specified user.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "title": "Buy organic groceries",
  "description": "Organic milk, free-range eggs",
  "priority": "medium",
  "tags": ["shopping", "health"]
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": 1,
    "title": "Buy organic groceries",
    "description": "Organic milk, free-range eggs",
    "completed": false,
    "priority": "medium",
    "tags": ["shopping", "health"],
    "created_at": "2026-01-18T10:00:00Z",
    "updated_at": "2026-01-18T11:00:00Z"
  },
  "message": "Task updated successfully"
}
```

**Errors:**
- 400 Bad Request: Invalid data
- 403 Forbidden: Task belongs to another user
- 404 Not Found: Task does not exist

---

### DELETE /api/{user_id}/tasks/{id}

Delete a task for the specified user.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

**Errors:**
- 403 Forbidden: Task belongs to another user
- 404 Not Found: Task does not exist

---

### PATCH /api/{user_id}/tasks/{id}/toggle

Toggle task completion status for the specified user.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "data": {
    "id": 1,
    "completed": true,
    "updated_at": "2026-01-18T12:00:00Z"
  },
  "message": "Task marked as completed"
}
```

**Errors:**
- 403 Forbidden: Task belongs to another user
- 404 Not Found: Task does not exist

---

## Tag Endpoints

### GET /api/{user_id}/tags

List all tags used by the specified user.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "data": {
    "tags": [
      { "name": "work", "count": 15 },
      { "name": "home", "count": 8 },
      { "name": "urgent", "count": 3 }
    ]
  }
}
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid request data |
| UNAUTHORIZED | 401 | Missing or invalid authentication |
| FORBIDDEN | 403 | Access denied to resource |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Resource already exists |
| INTERNAL_ERROR | 500 | Server error |
