# Agent context: Snippy & auth playground

## Overview and context

This repo (**snippy**) is a small full-stack Rust app: Actix backend + Yew (WASM) frontend, with a Boids demo and deployment to GitHub Pages via Actions. The following context is for future work and for a separate **auth playground** project.

### Systems design and web architecture (high level)

- **Auth** requires a backend: storing users, verifying credentials, sessions/tokens. Static hosting (e.g. GitHub Pages) alone can’t do real auth.
- **Frontend** can be “dynamic” even when served as static files: an SPA loads from an API at runtime. “Static” refers to how files are delivered; behavior can still be dynamic.
- **Rendering** options: static (build-time), client-side (SPA), server-side (SSR), or hybrid. Choice depends on how the page should feel and where we’re willing to run a server.
- **Request path** (typical order): Client → DNS → (CDN) → (Load balancer) → (API Gateway) → (Web server e.g. Nginx) → App server → Business logic. Not every layer is required; Nginx and API Gateway are independent choices.
- **Nginx** (or similar web server) offloads: HTTP/TLS, static file I/O (e.g. sendfile), reverse proxy with buffering so slow clients don’t block app workers. App server then focuses on business logic.

### What we’re looking to do

- **Auth playground**: A separate project for experimenting with systems design, starting with a **simple auth system for users**.
- **Auth0** for login (identity); a **custom backend** to manage **business-specific permissions** in a way Auth0 doesn’t support.
- **Minimal** setup: static frontend + Auth0 + one backend service + one DB for permissions.

---

## Minimal auth playground plan

### Roles

- **Auth0** = identity (who the user is). Frontend sends users to Auth0; Auth0 returns a JWT.
- **Backend** = “user” data Auth0 doesn’t handle: business-specific permissions (roles, flags, per-resource access), keyed by Auth0 user id (or email).

### Frontend (minimal)

- **Single static app**: one HTML page + JS, or a tiny SPA.
- **Auth0 SPA SDK** (or login-with-redirect): user clicks “Log in” → redirect to Auth0 → Auth0 redirects back with tokens → JS stores the token and calls our API.
- **Host**: anywhere static (GitHub Pages, Vercel, Netlify). No server required for the frontend.

### Backend (minimal)

- **One small API** that:
  1. Accepts requests with the **Auth0 JWT** (e.g. `Authorization: Bearer <token>`).
  2. **Validates the JWT** with Auth0’s JWKS (so we trust “this is user X from Auth0”).
  3. Uses **Auth0 user id** (or email) as the key to **read/write permission data** (roles, permissions, etc.).
- **Storage**: Start with **SQLite** (one file) or a single **Postgres** (e.g. Supabase, Neon). One table e.g. `user_permissions (auth0_user_id, permission_type, ...)`.
- **Host**: One process on **Railway**, **Render**, or **Fly.io** (free/cheap tiers). Or serverless (Vercel/Netlify functions, Lambda) if preferred.

### Minimal path to “playground”

1. **Auth0**: Create a tenant, add a “Single Page Application” app, set allowed callback URLs for the frontend.
2. **Frontend**: One page with “Log in” (Auth0 redirect) and e.g. “Call my API” that sends the token to the backend.
3. **Backend**: One service (e.g. Node/Express, Python/FastAPI, Rust/Actix) with:
   - Middleware: validate JWT with Auth0 JWKS, attach `auth0_user_id` to the request.
   - Route: e.g. `GET /me/permissions` → return current user’s permissions from our DB.
   - Optional: admin route to set permissions (e.g. `POST /admin/users/:id/permissions`), protected by an admin check.
4. **DB**: SQLite or one Postgres DB; one table for permissions keyed by Auth0 user id.

**Summary**: Auth0 + static frontend + one backend service + one small DB. Backend exists only to own the permission model Auth0 doesn’t support; Auth0 owns login.
