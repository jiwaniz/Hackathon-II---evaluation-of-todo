# UI Pages

## Overview

Page layouts using Next.js 16+ App Router with TypeScript. Uses file-based routing under `/app` directory.

## Route Structure

```
app/
├── layout.tsx              # Root layout
├── page.tsx                # Landing page (/)
├── globals.css             # Global styles
├── (auth)/                 # Auth group (no layout)
│   ├── login/
│   │   └── page.tsx        # Login page (/login)
│   └── register/
│       └── page.tsx        # Register page (/register)
├── (dashboard)/            # Dashboard group (protected)
│   ├── layout.tsx          # Dashboard layout with sidebar
│   └── tasks/
│       └── page.tsx        # Task dashboard (/tasks)
└── api/                    # API routes (if needed for BFF)
```

## Page Specifications

### Landing Page (/)

**Route**: `/`
**File**: `app/page.tsx`
**Type**: Server Component
**Auth**: Public

**Purpose**: Marketing/welcome page for unauthenticated users.

**Layout**:
```
┌─────────────────────────────────────────────┐
│  Header (Logo, Login, Register)             │
├─────────────────────────────────────────────┤
│                                             │
│         Hero Section                        │
│    "Organize Your Tasks Effortlessly"       │
│    [Get Started] [Learn More]               │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│         Features Section                    │
│    ┌───────┐ ┌───────┐ ┌───────┐          │
│    │ Multi │ │ Tags  │ │ Sync  │          │
│    │ User  │ │ Prior │ │ All   │          │
│    └───────┘ └───────┘ └───────┘          │
│                                             │
├─────────────────────────────────────────────┤
│  Footer                                     │
└─────────────────────────────────────────────┘
```

**Behavior**:
- If user is authenticated, redirect to `/tasks`
- CTA buttons lead to `/register`

---

### Login Page (/login)

**Route**: `/login`
**File**: `app/(auth)/login/page.tsx`
**Type**: Client Component
**Auth**: Public (redirect if authenticated)

**Purpose**: User authentication.

**Layout**:
```
┌─────────────────────────────────────────────┐
│  Header (Logo)                              │
├─────────────────────────────────────────────┤
│                                             │
│         ┌─────────────────────┐             │
│         │   Login Form        │             │
│         │                     │             │
│         │   Email: [______]   │             │
│         │   Pass:  [______]   │             │
│         │                     │             │
│         │   [Login Button]    │             │
│         │                     │             │
│         │   No account?       │             │
│         │   Register →        │             │
│         └─────────────────────┘             │
│                                             │
└─────────────────────────────────────────────┘
```

**Behavior**:
- Validate form inputs
- Call `/api/auth/login`
- Store JWT token
- Redirect to `/tasks` on success
- Show error on failure

---

### Register Page (/register)

**Route**: `/register`
**File**: `app/(auth)/register/page.tsx`
**Type**: Client Component
**Auth**: Public (redirect if authenticated)

**Purpose**: New user registration.

**Layout**:
```
┌─────────────────────────────────────────────┐
│  Header (Logo)                              │
├─────────────────────────────────────────────┤
│                                             │
│         ┌─────────────────────┐             │
│         │   Register Form     │             │
│         │                     │             │
│         │   Email: [______]   │             │
│         │   Pass:  [______]   │             │
│         │   Confirm: [____]   │             │
│         │                     │             │
│         │   [Register Button] │             │
│         │                     │             │
│         │   Have account?     │             │
│         │   Login →           │             │
│         └─────────────────────┘             │
│                                             │
└─────────────────────────────────────────────┘
```

**Behavior**:
- Validate form inputs
- Check password match
- Call `/api/auth/register`
- Auto-login after registration
- Redirect to `/tasks` on success

---

### Task Dashboard (/tasks)

**Route**: `/tasks`
**File**: `app/(dashboard)/tasks/page.tsx`
**Type**: Client Component
**Auth**: Protected (requires authentication)

**Purpose**: Main task management interface.

**Layout**:
```
┌─────────────────────────────────────────────┐
│  Header (Logo, User Menu)                   │
├─────────────────────────────────────────────┤
│        │                                    │
│ Sidebar│   Task Dashboard                   │
│        │                                    │
│ Filters│   ┌─────────────────────────────┐  │
│        │   │ Search: [_______________]   │  │
│ Status │   │ Filters: [All▼] [Priority▼] │  │
│ □ All  │   └─────────────────────────────┘  │
│ □ Todo │                                    │
│ □ Done │   ┌─────────────────────────────┐  │
│        │   │ ☐ Buy groceries      [High] │  │
│ Priority│  │   Milk, eggs...    Edit Del │  │
│ □ High │   ├─────────────────────────────┤  │
│ □ Med  │   │ ✓ Call mom         [Medium] │  │
│ □ Low  │   │   Weekly check-in  Edit Del │  │
│        │   ├─────────────────────────────┤  │
│ Tags   │   │ ☐ Review PR        [High]   │  │
│ [work] │   │   #work           Edit Del  │  │
│ [home] │   └─────────────────────────────┘  │
│        │                                    │
│        │                          [+ Add]   │
└────────┴────────────────────────────────────┘
```

**Features**:
- Fetch tasks on mount
- Filter tasks by status, priority, tags
- Search tasks by keyword
- Sort tasks by various criteria
- Toggle task completion
- Open modal for add/edit
- Confirm before delete
- Infinite scroll or pagination

**State Management**:
```typescript
{
  tasks: Task[];
  isLoading: boolean;
  filters: {
    status: 'all' | 'pending' | 'completed';
    priority: string | null;
    tags: string[];
    search: string;
  };
  sort: string;
  pagination: {
    page: number;
    hasMore: boolean;
  };
  modal: {
    isOpen: boolean;
    editingTask: Task | null;
  };
}
```

---

## Dashboard Layout

**File**: `app/(dashboard)/layout.tsx`
**Type**: Client Component

**Purpose**: Shared layout for authenticated pages.

**Features**:
- Auth guard (redirect if not authenticated)
- Header with user menu
- Responsive sidebar
- Main content area
- Toast notifications

**Layout**:
```tsx
export default function DashboardLayout({ children }) {
  return (
    <AuthGuard>
      <div className="min-h-screen flex flex-col">
        <Header />
        <div className="flex flex-1">
          <Sidebar />
          <main className="flex-1 p-6">
            {children}
          </main>
        </div>
        <ToastContainer />
      </div>
    </AuthGuard>
  );
}
```

---

## Responsive Design

### Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | < 640px | Sidebar hidden, hamburger menu |
| Tablet | 640-1024px | Sidebar overlay |
| Desktop | > 1024px | Sidebar visible |

### Mobile Considerations
- Touch-friendly tap targets (min 44px)
- Bottom navigation on mobile
- Swipe gestures for task actions
- Full-screen modals on mobile
- Simplified filters (drawer instead of sidebar)

---

## Error Pages

### 404 Not Found
- Friendly message
- Link to home/dashboard

### 500 Server Error
- Apologetic message
- Retry button
- Link to home

### Unauthorized (401)
- Redirect to login
- Preserve intended URL for redirect after login
