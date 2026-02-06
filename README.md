---
title: Todo AI Chatbot
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 7860
---

# Todo AI Chatbot - Phase 3

Full-stack todo application with AI-powered chatbot assistant built with Next.js, FastAPI, and Supabase.

## Features

- **Task Management**: Create, update, delete, and organize tasks with priorities and tags
- **AI Chatbot**: Natural language task management using Google Gemini and Groq
- **Authentication**: Secure user authentication with Supabase (mandatory email verification)
- **Smart Filtering**: Filter by priority, status, tags, and search
- **Responsive UI**: Modern, mobile-friendly interface with Tailwind CSS

## Tech Stack

### Frontend
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Supabase Auth

### Backend
- Python 3.13+ with FastAPI
- SQLModel ORM
- Neon PostgreSQL
- Google Gemini API
- Groq API

### Deployment
- Hugging Face Spaces (Docker)
- Serverless PostgreSQL (Neon)

## Environment Variables

Required secrets (configure in Space settings):

```bash
# Database
DATABASE_URL=postgresql://...

# Authentication
BETTER_AUTH_SECRET=your-secret
BETTER_AUTH_URL=https://your-space.hf.space
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_JWT_SECRET=your-jwt-secret
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# AI Providers
GOOGLE_API_KEY=your-google-key
GROQ_API_KEY=your-groq-key

# CORS & API
CORS_ORIGINS=https://your-space.hf.space
NEXT_PUBLIC_API_URL=https://your-space.hf.space

# Environment
ENVIRONMENT=production
```

## Local Development

### Prerequisites
- Python 3.13+
- Node.js 20+
- UV package manager
- PostgreSQL (or Neon account)

### Setup

1. Clone the repository
2. Install dependencies:

```bash
# Backend
cd backend
uv sync

# Frontend
cd frontend
npm install
```

3. Configure environment variables (copy from templates)

4. Run development servers:

```bash
# Backend (port 8000)
cd backend
uv run uvicorn main:app --reload

# Frontend (port 3000)
cd frontend
npm run dev
```

## Project Structure

```
/
├── frontend/          # Next.js application
├── backend/           # FastAPI server
├── specs/             # Feature specifications
├── Dockerfile         # Multi-stage build
└── README.md          # This file
```

## License

MIT

## Author

Built for PGD Data Sciences with AI - Agentic AI Hackathon
