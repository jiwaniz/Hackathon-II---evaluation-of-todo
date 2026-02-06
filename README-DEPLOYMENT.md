# Hugging Face Spaces Deployment Guide

## Overview
Full-stack Todo application with AI chatbot (Phase 1-3) deployed on Hugging Face Spaces.

**Stack:**
- Frontend: Next.js 16+ (TypeScript, Tailwind CSS)
- Backend: FastAPI (Python 3.13+)
- Database: Neon PostgreSQL
- AI: Gemini/Groq with MCP tools

## Prerequisites
- Hugging Face account
- Neon PostgreSQL database
- Gemini/Groq API keys
- Auth secrets (BETTER_AUTH_SECRET, Supabase)

## Deployment Steps

### 1. Create a New Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in details:
   - **Name:** `todo-app-ai-chatbot` (or your choice)
   - **License:** MIT
   - **Space SDK:** Docker
   - **Visibility:** Public or Private
4. Click **"Create Space"**

### 2. Push Your Code to the Space

#### Option A: Via Git (Recommended)

```bash
# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/<your-username>/<space-name>

# Push to Hugging Face
git push hf main:main
```

#### Option B: Via Web UI

1. In your Space, go to **Files** tab
2. Click **"Add file"** → **"Upload files"**
3. Upload all project files (or use git)

### 3. Configure Environment Variables

In your Space settings, add these **Secrets**:

```bash
# Database
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your-secret-here
BETTER_AUTH_URL=https://your-space.hf.space

# Supabase (Phase 3)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# AI APIs
GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key

# CORS
CORS_ORIGINS=https://your-space.hf.space

# Next.js
NEXT_PUBLIC_API_URL=https://your-space.hf.space
```

### 4. Wait for Build

- Hugging Face will automatically build your Docker image
- Check the **Logs** tab for build progress
- Build typically takes 5-10 minutes

### 5. Access Your App

Once deployed, your app will be available at:
```
https://<your-username>-<space-name>.hf.space
```

## Troubleshooting

### Build Fails
- Check Logs tab for errors
- Verify Dockerfile syntax
- Ensure all dependencies are in pyproject.toml

### App Won't Start
- Check environment variables are set
- Verify DATABASE_URL is correct
- Check backend logs for connection errors

### Database Connection Issues
- Ensure Neon database allows connections from any IP
- Verify DATABASE_URL includes `?sslmode=require`
- Check database credentials

### Frontend Not Loading
- Verify NEXT_PUBLIC_API_URL points to your Space URL
- Check CORS_ORIGINS includes your Space URL
- Review browser console for errors

## Architecture

```
┌─────────────────────────────────────┐
│   Hugging Face Space (Docker)      │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │   Next.js    │  │   FastAPI   │ │
│  │  (Port 7860) │◄─┤  (Port 8000)│ │
│  └──────────────┘  └──────┬──────┘ │
│                           │         │
└───────────────────────────┼─────────┘
                            │
                    ┌───────▼────────┐
                    │  Neon Postgres │
                    │   (External)   │
                    └────────────────┘
```

## Monitoring

- **Space Logs:** Check application logs in the Logs tab
- **Usage:** Monitor CPU/RAM in Space settings
- **Database:** Monitor connections in Neon dashboard

## Updating

To update your deployment:

```bash
# Make changes locally
git add .
git commit -m "Update: description"

# Push to Hugging Face
git push hf main:main
```

Hugging Face will automatically rebuild and redeploy.

## Cost

- **Hugging Face Space:** Free tier available
- **Neon Database:** Free tier (0.5GB storage)
- **Gemini/Groq APIs:** Pay per use

## Support

For issues:
- Check Hugging Face Spaces documentation
- Review application logs
- Verify environment variables
