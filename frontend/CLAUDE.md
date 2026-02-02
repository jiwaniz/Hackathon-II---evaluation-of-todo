# Frontend Guidelines

## Stack

- Next.js 16+ (App Router)
- TypeScript (strict mode)
- Tailwind CSS
- Better Auth (authentication)

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing page
│   ├── globals.css         # Global styles
│   ├── (auth)/             # Auth group (login, register)
│   └── (dashboard)/        # Protected dashboard pages
├── components/             # React components
│   ├── auth/               # Auth components
│   ├── layout/             # Layout components
│   ├── tasks/              # Task components
│   ├── filters/            # Filter components
│   └── ui/                 # Reusable UI components
├── lib/                    # Utilities
│   ├── api.ts              # API client
│   ├── auth.ts             # Better Auth config
│   └── utils.ts            # Helper functions
├── types/                  # TypeScript types
└── hooks/                  # Custom React hooks
```

## Patterns

### Components
- Use server components by default
- Client components only when interactivity needed (`'use client'`)
- Colocate components with their pages when page-specific

### API Calls
All backend calls should use the API client:

```typescript
import { api } from '@/lib/api';

// Example usage
const tasks = await api.getTasks();
const task = await api.createTask({ title: 'New task' });
```

### Authentication
```typescript
import { useSession } from '@/lib/auth';

// In client components
const { user, isLoading } = useSession();

// Protect routes with AuthGuard
<AuthGuard>
  <ProtectedContent />
</AuthGuard>
```

### State Management
- Use React hooks for local state
- Use URL params for filter/search state (shareable)
- Use React Query for server state caching

## Styling

- Use Tailwind CSS classes exclusively
- No inline styles or CSS modules
- Follow existing component patterns
- Mobile-first responsive design

### Color Conventions
- Primary actions: `bg-blue-600`
- Success: `bg-green-600`
- Danger/Delete: `bg-red-600`
- Priority High: `bg-red-100 text-red-800`
- Priority Medium: `bg-yellow-100 text-yellow-800`
- Priority Low: `bg-green-100 text-green-800`

## Environment Variables

```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<shared-secret>
BETTER_AUTH_URL=http://localhost:3000
```

## Commands

```bash
npm run dev      # Development server (port 3000)
npm run build    # Production build
npm run lint     # ESLint check
npm run test     # Run tests
```

## Spec References

- UI Components: @specs/ui/components.md
- Page Layouts: @specs/ui/pages.md
- API Integration: @specs/api/rest-endpoints.md
- Auth Flow: @specs/features/authentication.md
