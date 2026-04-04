---
name: react-dev
description: React TypeScript 开发技能 - 类型安全的 React 组件开发、React 19 新特性、事件处理、Hooks 类型、泛型组件
version: 1.0.0
author: softaworks
tags:
  - react
  - typescript
  - frontend
  - hooks
  - components
  - react19
---

# React TypeScript 开发

Type-safe React = compile-time guarantees = confident refactoring.

## When to Use This Skill

- Building typed React components
- Implementing generic components
- Typing event handlers, forms, refs
- Using React 19 features (Actions, Server Components, use())
- Router integration (TanStack Router, React Router)
- Custom hooks with proper typing

**NOT for**: non-React TypeScript, vanilla JS React

## React 19 Changes

React 19 breaking changes require migration. Key patterns:

### ref as prop - forwardRef deprecated

```typescript
// React 19 - ref as regular prop
type ButtonProps = {
  ref?: React.Ref<HTMLButtonElement>;
} & React.ComponentPropsWithoutRef<'button'>;

function Button({ ref, children, ...props }: ButtonProps) {
  return <button ref={ref} {...props}>{children}</button>;
}
```

### useActionState - replaces useFormState

```typescript
import { useActionState } from 'react';

type FormState = { errors?: string[]; success?: boolean };

function Form() {
  const [state, formAction, isPending] = useActionState(submitAction, {});
  return <form action={formAction}>...</form>;
}
```

### use() - unwraps promises/context

```typescript
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspends until resolved
  return <div>{user.name}</div>;
}
```

See `react-19-patterns.md` for useOptimistic, useTransition, migration checklist.

## Component Patterns

### Props - extend native elements

```typescript
type ButtonProps = {
  variant: 'primary' | 'secondary';
} & React.ComponentPropsWithoutRef<'button'>;

function Button({ variant, children, ...props }: ButtonProps) {
  return <button className={variant} {...props}>{children}</button>;
}
```

### Children typing

```typescript
type Props = {
  children: React.ReactNode;          // Anything renderable
  icon: React.ReactElement;           // Single element
  render: (data: T) => React.ReactNode;  // Render prop
};
```

### Discriminated unions for variant props

```typescript
type ButtonProps =
  | { variant: 'link'; href: string }
  | { variant: 'button'; onClick: () => void };

function Button(props: ButtonProps) {
  if (props.variant === 'link') {
    return <a href={props.href}>Link</a>;
  }
  return <button onClick={props.onClick}>Button</button>;
}
```

## Event Handlers

Use specific event types for accurate target typing:

```typescript
// Mouse
function handleClick(e: React.MouseEvent<HTMLButtonElement>) {
  e.currentTarget.disabled = true;
}

// Form
function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
  const formData = new FormData(e.currentTarget);
}

// Input
function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value);
}

// Keyboard
function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
  if (e.key === 'Enter') e.currentTarget.blur();
}
```

See `event-handlers.md` for focus, drag, clipboard, touch, wheel events.

## Hooks Typing

### useState - explicit for unions/null

```typescript
const [user, setUser] = useState<User | null>(null);
const [status, setStatus] = useState<'idle' | 'loading'>('idle');
```

### useRef - null for DOM, value for mutable

```typescript
const inputRef = useRef<HTMLInputElement>(null);  // DOM - use ?.
const countRef = useRef<number>(0);               // Mutable - direct access
```

### useReducer - discriminated unions for actions

```typescript
type Action =
  | { type: 'increment' }
  | { type: 'set'; payload: number };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'set': return { ...state, count: action.payload };
    default: return state;
  }
}
```

### Custom hooks - tuple returns with as const

```typescript
function useToggle(initial = false) {
  const [value, setValue] = useState(initial);
  const toggle = () => setValue(v => !v);
  return [value, toggle] as const;
}
```

### useContext - null guard pattern

```typescript
const UserContext = createContext<User | null>(null);

function useUser() {
  const user = useContext(UserContext);
  if (!user) throw new Error('useUser outside UserProvider');
  return user;
}
```

See `hooks.md` for useCallback, useMemo, useImperativeHandle, useSyncExternalStore.

## Generic Components

Generic components infer types from props - no manual annotations at call site.

### Pattern - keyof T for column keys, render props for custom rendering

```typescript
type Column<T> = {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], item: T) => React.ReactNode;
};

type TableProps<T> = {
  data: T[];
  columns: Column<T>[];
  keyExtractor: (item: T) => string | number;
};

function Table<T>({ data, columns, keyExtractor }: TableProps<T>) {
  return (
    <table>
      <thead>
        <tr>{columns.map(col => <th key={String(col.key)}>{col.header}</th>)}</tr>
      </thead>
      <tbody>
        {data.map(item => (
          <tr key={keyExtractor(item)}>
            {columns.map(col => (
              <td key={String(col.key)}>
                {col.render ? col.render(item[col.key], item) : String(item[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Constrained generics for required properties

```typescript
type HasId = { id: string | number };

function List<T extends HasId>({ items }: { items: T[] }) {
  return items.map(item => <div key={item.id}>{String(item.id)}</div>);
}
```

## Forms

### Controlled inputs with discriminated unions

```typescript
type FormState = {
  status: 'idle' | 'submitting' | 'success' | 'error';
  data: { name: string; email: string };
  error?: string;
};

function Form() {
  const [state, setState] = useState<FormState>({
    status: 'idle',
    data: { name: '', email: '' }
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setState(prev => ({
      ...prev,
      data: { ...prev.data, [e.target.name]: e.target.value }
    }));
  };

  return <form>...</form>;
}
```

### React 19 Actions with useActionState

```typescript
async function submitForm(formData: FormData): Promise<FormState> {
  const response = await fetch('/api/submit', {
    method: 'POST',
    body: formData
  });
  return response.json();
}

function Form() {
  const [state, formAction, isPending] = useActionState(submitForm, {
    status: 'idle',
    data: { name: '', email: '' }
  });

  return (
    <form action={formAction}>
      <input name="name" />
      <input name="email" />
      <button disabled={isPending}>
        {isPending ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

## Router Integration

### TanStack Router - type-safe routing

```typescript
import { createRootRoute, createRoute, createRouter } from '@tanstack/react-router';

const rootRoute = createRootRoute();

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: Index
});

const userRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/users/$userId',
  component: User,
  loader: ({ params }) => fetchUser(params.userId)
});

const router = createRouter({
  routeTree: rootRoute,
  defaultPreload: 'intent'
});

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}
```

### React Router v6+ with type safety

```typescript
import { createBrowserRouter, LoaderFunctionArgs } from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      {
        path: 'users/:userId',
        element: <User />,
        loader: async ({ params }: LoaderFunctionArgs) => {
          return fetchUser(params.userId!);
        }
      }
    ]
  }
]);
```

## Best Practices

1. **Type Props Explicitly**: Always define prop types, use `ComponentPropsWithoutRef` for extending native elements
2. **Use Discriminated Unions**: For variant props and state management
3. **Type Event Handlers**: Use specific event types for accurate target typing
4. **Generic Components**: Let TypeScript infer types from props
5. **Custom Hooks**: Return tuples with `as const` for proper typing
6. **Context Pattern**: Use null guard pattern for required context
7. **React 19 Migration**: Update ref patterns, use new hooks

## Resources

- **React TypeScript Cheatsheet**: https://react-typescript-cheatsheet.netlify.app/
- **React 19 Docs**: https://react.dev/blog/2024/04/25/react-19
- **TanStack Router**: https://tanstack.com/router/latest
