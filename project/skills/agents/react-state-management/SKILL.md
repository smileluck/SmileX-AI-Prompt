---
name: react-state-management
description: React 状态管理综合指南 - 从本地组件状态到全局存储和服务器状态同步
version: 1.0.0
author: wshobson
tags:
  - react
  - state-management
  - redux
  - zustand
  - jotai
  - react-query
---

# React State Management

Comprehensive guide to modern React state management patterns, from local component state to global stores and server state synchronization.

## When to Use This Skill

- Setting up global state management in a React app
- Choosing between Redux Toolkit, Zustand, or Jotai
- Managing server state with React Query or SWR
- Implementing optimistic updates
- Debugging state-related issues
- Migrating from legacy Redux to modern patterns

## Core Concepts

### 1. State Categories

| Type | Description | Solutions |
|------|-------------|-----------|
| Local State | Component-specific, UI state | useState, useReducer |
| Global State | Shared across components | Redux Toolkit, Zustand, Jotai |
| Server State | Remote data, caching | React Query, SWR, RTK Query |
| URL State | Route parameters, search | React Router, nuqs |
| Form State | Input values, validation | React Hook Form, Formik |

### 2. Selection Criteria

- **Small app, simple state** → Zustand or Jotai
- **Large app, complex state** → Redux Toolkit
- **Heavy server interaction** → React Query + light client state
- **Atomic/granular updates** → Jotai

## Quick Start

### Zustand (Simplest)

```typescript
// store/useStore.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface AppState {
  user: User | null
  theme: 'light' | 'dark'
  setUser: (user: User | null) => void
  toggleTheme: () => void
}

export const useStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        theme: 'light',
        setUser: (user) => set({ user }),
        toggleTheme: () => set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light'
        })),
      }),
      { name: 'app-storage' }
    )
  )
)

// Usage in component
function Header() {
  const { user, theme, toggleTheme } = useStore()
  return (
    <header className={theme}>
      {user?.name}
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  )
}
```

## Patterns

### Pattern 1: Redux Toolkit with TypeScript

```typescript
// store/index.ts
import { configureStore } from "@reduxjs/toolkit";
import { TypedUseSelectorHook, useDispatch, useSelector } from "react-redux";
import userReducer from "./slices/userSlice";
import cartReducer from "./slices/cartSlice";

export const store = configureStore({
  reducer: {
    user: userReducer,
    cart: cartReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ["persist/PERSIST"],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed hooks
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

```typescript
// store/slices/userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";

interface User {
  id: string;
  email: string;
  name: string;
}

interface UserState {
  current: User | null;
  status: "idle" | "loading" | "succeeded" | "failed";
  error: string | null;
}

const initialState: UserState = {
  current: null,
  status: "idle",
  error: null,
};

export const fetchUser = createAsyncThunk(
  "user/fetchUser",
  async (userId: string, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error("Failed to fetch user");
      return await response.json();
    } catch (error) {
      return rejectWithValue((error as Error).message);
    }
  },
);

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.current = action.payload;
      state.status = "succeeded";
    },
    clearUser: (state) => {
      state.current = null;
      state.status = "idle";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.current = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload as string;
      });
  },
});

export const { setUser, clearUser } = userSlice.actions;
export default userSlice.reducer;
```

### Pattern 2: Zustand with Slices (Scalable)

```typescript
// store/slices/createUserSlice.ts
import { StateCreator } from "zustand";

export interface UserSlice {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

export const createUserSlice: StateCreator<
  UserSlice & CartSlice,
  [],
  [],
  UserSlice
> = (set, get) => ({
  user: null,
  isAuthenticated: false,
  login: async (credentials) => {
    const user = await authApi.login(credentials);
    set({ user, isAuthenticated: true });
  },
  logout: () => {
    set({ user: null, isAuthenticated: false });
  },
});

// store/index.ts
import { create } from "zustand";
import { createUserSlice, UserSlice } from "./slices/createUserSlice";
import { createCartSlice, CartSlice } from "./slices/createCartSlice";

export const useStore = create<UserSlice & CartSlice>()((...a) => ({
  ...createUserSlice(...a),
  ...createCartSlice(...a),
}));
```

### Pattern 3: Jotai (Atomic)

```typescript
// atoms/index.ts
import { atom, useAtom } from "jotai";

// Primitive atoms
export const userAtom = atom<User | null>(null);
export const themeAtom = atom<"light" | "dark">("light");

// Derived atoms (read-only)
export const isAuthenticatedAtom = atom((get) => !!get(userAtom));

// Read-write atoms
export const toggleThemeAtom = atom(
  (get) => get(themeAtom),
  (get, set) => set(themeAtom, get(themeAtom) === "light" ? "dark" : "light")
);

// Async atoms
export const userStatsAtom = atom(async (get) => {
  const user = get(userAtom);
  if (!user) return null;
  return fetchUserStats(user.id);
});

// Usage
function Header() {
  const [user] = useAtom(userAtom);
  const [theme, toggleTheme] = useAtom(toggleThemeAtom);
  return (
    <header className={theme}>
      {user?.name}
      <button onClick={toggleTheme}>Toggle</button>
    </header>
  );
}
```

### Pattern 4: React Query (Server State)

```typescript
// queries/useUsers.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

export function useUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: () => fetch("/api/users").then((r) => r.json()),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useUser(id: string) {
  return useQuery({
    queryKey: ["users", id],
    queryFn: () => fetch(`/api/users/${id}`).then((r) => r.json()),
    enabled: !!id,
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (user: User) =>
      fetch(`/api/users/${user.id}`, {
        method: "PUT",
        body: JSON.stringify(user),
      }).then((r) => r.json()),
    onMutate: async (newUser) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["users", newUser.id] });

      // Snapshot previous value
      const previousUser = queryClient.getQueryData(["users", newUser.id]);

      // Optimistically update
      queryClient.setQueryData(["users", newUser.id], newUser);

      return { previousUser };
    },
    onError: (err, newUser, context) => {
      // Rollback on error
      queryClient.setQueryData(["users", newUser.id], context?.previousUser);
    },
    onSettled: (newUser) => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ["users", newUser.id] });
    },
  });
}
```

### Pattern 5: Optimistic Updates

```typescript
function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [pendingTodo, setPendingTodo] = useState<Todo | null>(null);

  const addTodo = async (text: string) => {
    const tempId = Date.now();
    const optimisticTodo: Todo = { id: tempId, text, completed: false };

    // Optimistic update
    setTodos((prev) => [...prev, optimisticTodo]);
    setPendingTodo(optimisticTodo);

    try {
      const realTodo = await api.createTodo(text);
      // Replace temp with real
      setTodos((prev) =>
        prev.map((t) => (t.id === tempId ? realTodo : t))
      );
    } catch (error) {
      // Rollback on error
      setTodos((prev) => prev.filter((t) => t.id !== tempId));
    } finally {
      setPendingTodo(null);
    }
  };

  return (
    <ul>
      {todos.map((todo) => (
        <li
          key={todo.id}
          style={{ opacity: todo.id === pendingTodo?.id ? 0.5 : 1 }}
        >
          {todo.text}
        </li>
      ))}
    </ul>
  );
}
```

## Best Practices

1. **Choose the right tool**: Match state management to app complexity
2. **Separate concerns**: Keep server state separate from client state
3. **Normalize data**: Use normalized shapes for relational data
4. **Avoid prop drilling**: Use context or state management for deep trees
5. **Type everything**: TypeScript integration for all state solutions
6. **Test state logic**: Unit test reducers, selectors, and hooks
7. **Monitor performance**: Use React DevTools and Redux DevTools
8. **Handle loading states**: Always show loading indicators
9. **Error boundaries**: Handle state errors gracefully
10. **Persist wisely**: Only persist necessary state

## Decision Matrix

| Scenario | Recommended Solution |
|----------|---------------------|
| Simple app (< 10 components) | useState + Context |
| Medium app, shared state | Zustand |
| Large enterprise app | Redux Toolkit |
| Heavy API usage | React Query + Zustand |
| Real-time updates | React Query + WebSocket |
| Complex derived state | Jotai or Redux selectors |
| Form-heavy app | React Hook Form + Zustand |

## Resources

- **Redux Toolkit**: https://redux-toolkit.js.org/
- **Zustand**: https://github.com/pmndrs/zustand
- **Jotai**: https://jotai.org/
- **React Query**: https://tanstack.com/query/latest
- **SWR**: https://swr.vercel.app/
