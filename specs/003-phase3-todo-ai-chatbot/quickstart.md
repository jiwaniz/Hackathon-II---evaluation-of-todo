# Quickstart: Todo AI Chatbot

## Prerequisites

- Python 3.13+ with UV package manager
- Node.js 18+ with npm
- Neon PostgreSQL database (existing from Phase 2)
- Google AI Studio API key (free tier)
- Groq API key (free tier, for fallback)
- Supabase project (for auth)

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require
GOOGLE_API_KEY=<from Google AI Studio>
GROQ_API_KEY=<from Groq console>
SUPABASE_URL=<your Supabase project URL>
SUPABASE_JWT_SECRET=<from Supabase dashboard, Settings > API > JWT Secret>
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=<your Supabase project URL>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<from Supabase dashboard>
```

## Setup

### Backend
```bash
cd backend
uv add google-adk mcp groq
uv run alembic upgrade head  # Run migrations for new tables
uv run uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install @supabase/supabase-js
npm run dev
```

## Verify

1. Open http://localhost:3000 and log in via Supabase Auth
2. Navigate to the chat page
3. Type "Add a task to test the chatbot"
4. Verify task is created and confirmation response appears

## Key Architecture

- **Stateless**: Each POST to `/api/{user_id}/chat` is independent
- **MCP Tools**: Agent uses MCP protocol to invoke task operations
- **Fallback**: If Gemini fails, request retries with Groq automatically
