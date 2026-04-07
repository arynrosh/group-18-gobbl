# Gobbl frontend

Playful, DoorDash-inspired React client for the existing **Gobbl FastAPI** backend. This app **does not** change server code; it follows the live routes and JSON field names in `app/routers` and `app/schemas`.

## Prerequisites

- Node.js **18+** (tested with Vite 5 on Node 20.16)
- Backend running (default `http://127.0.0.1:8000`)

## Setup

```bash
cd frontend
npm install
```

Copy environment example:

```bash
cp .env.example .env
```

- **Local dev (recommended):** keep `VITE_API_BASE_URL` empty. Requests go to `/api`, and Vite proxies to the backend (see `vite.config.ts`), avoiding browser CORS issues.
- **Direct API URL:** set `VITE_API_BASE_URL=http://127.0.0.1:8000` (or your deployed API). Your FastAPI app must allow CORS from the frontend origin in that case.

## Run

```bash
npm run dev
```

Open the printed URL (usually `http://localhost:5173`).

```bash
npm run build    # production bundle
npm run preview  # serve dist locally
```

## Auth

- **Login:** `POST /auth/login` with `application/x-www-form-urlencoded` body (`username`, `password`) — OAuth2 password flow, not JSON.
- **Profile:** `GET /auth/me` on startup when a JWT exists.
- **Token:** stored in `localStorage` (`gobbl_token`) and sent as `Authorization: Bearer …` on every Axios request.

## Roles & routing

Routes are guarded to match backend `require_roles` expectations:

| Role               | Example areas                                                                      |
| ------------------ | ---------------------------------------------------------------------------------- |
| `customer`         | Cart, checkout, payments, promos (`/discounts/my-codes`), notifications, reviews   |
| `restaurant_owner` | Owner sidebar: menu CRUD, drivers, restaurant notifications, order tools           |
| `driver`           | Update `driver_distance` / `status` for a chosen `driver_id`                       |
| `admin`            | Discounts, broadcast notifications, order-notification triggers, analytics         |

## Backend quirks (frontend workarounds)

1. **Restaurant ↔ owner:** the API does not expose “my restaurant” on the JWT. Owners pick a `restaurant_id` from the browse list; the choice is saved in `localStorage` (`gobbl_owner_restaurant_id`) for convenience.
2. **Driver identity:** drivers are keyed by numeric `driver_id` in `drivers.json`, not by username. The driver dashboard stores `driver_id` in `localStorage` (`gobbl_driver_id`).
3. **Recommendations:** `GET /recommendations/{customer_id}` returns **404** when there is no history. The UI treats that as an empty state (not a hard error).
4. **Customer notifications:** `GET /notifications/customer/{customer_id}` uses the JWT `sub` (username) as `customer_id`, matching how orders store `customer_id` in the sample data.
5. **Saved payment methods:** `POST /payments/process` always expects full card fields; saved methods are shown as **hints** only (prefill name/expiry), because the backend has no “pay with method id” shortcut.
6. **Cost calculation:** `POST /cost/calculate/{order_id}` builds an `Order` model server-side. If validation fails (e.g. schema vs. persisted JSON edge cases), the cart shows a clear “cost unavailable” message.

## Project layout

- `src/api` — Axios instance + interceptors  
- `src/features/*` — API wrappers grouped by domain  
- `src/pages` — route-level screens  
- `src/layouts` — shell / dashboard sidebars  
- `src/store` — Zustand (`auth`, `cart`)  
- `src/types` — TypeScript shapes aligned with backend responses  

## Tech stack

React 19, Vite 5, TypeScript, React Router 7, Axios, Zustand, Tailwind CSS 3, Sonner toasts, Framer Motion, Recharts (admin).
