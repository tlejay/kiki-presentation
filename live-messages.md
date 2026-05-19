# Live Audience Messages (optional add-on)

Lights up two surfaces during a live presentation:

1. **Cover-slide QR badge** — sits inside slide 1 (the cover). Audience scans it to open the comment-submission page.
2. **Bottom-left ticker** — pinned to the viewport bottom-left on every non-cover slide. Idle state shows the QR badge again ("scan to send a message"); when a message arrives via Supabase Realtime, the badge flips to a stack of live messages that fade out after ~12 seconds.

Build this only when Tle asks for it (keywords: "live messages", "comment ticker", "audience interaction", "ส่งข้อความขึ้นจอ"). Otherwise skip — the core deck does not depend on it.

**Reference implementation**: `bni-5min/comment-ticker.tsx`, `bni-5min/comment-qr.ts`, `bni-5min/comment/`.

---

## Architecture

```
audience phone                       speaker laptop
─────────────                        ──────────────
/<slug>/comment      submits  ───►   Supabase Postgres
  (form page)                         table: <slug>_comments
                                          │
                                          │ realtime INSERT
                                          ▼
                                     <CommentTicker>  (bottom-left of every slide)
```

- **Database**: Supabase Postgres table with realtime publication enabled. Schema: `id uuid pk default gen_random_uuid()`, `name text`, `message text`, `created_at timestamptz default now()`. Row-level security: insert allowed for the anon role (this is intentionally a public submission form), select allowed for anon (the deck reads via realtime).
- **Realtime channel**: subscribe to `postgres_changes` events on the comments table. Each `INSERT` payload becomes a live message in the ticker.
- **Submission page**: a small `'use client'` form at `/<slug>/comment` that POSTs (server action or route handler) and inserts into the table. Rate-limit on the server side (e.g. one message per IP per 30s) to keep noise down during a live talk.
- **QR**: pre-rendered server-side via the `qrcode` package and passed to the deck as an SVG string prop. Two locations consume it: cover slide (large), bottom-left ticker (small, idle state).

## Files to create

When Tle wants live messages, add four files alongside the deck:

```
src/app/presentation/<slug>/
├── comment-qr.ts          # LIVE_MESSAGES_ENABLED flag + COMMENT_URL + getCommentQrSvg()
├── comment-ticker.tsx     # 'use client' — Supabase realtime + ticker UI
├── comment/
│   ├── page.tsx           # public submission form
│   └── comment-form.tsx   # 'use client' — form input + POST handler
└── (existing deck files: layout.tsx, page.tsx, [slug]/page.tsx, slide-slugs.ts, <slug>-deck.tsx)
```

## `comment-qr.ts` (server-side helper)

```ts
import QRCode from "qrcode";

// Toggle the entire feature. When false the QR / ticker render as no-ops, so
// you can ship the deck without lighting up the realtime backend.
export const LIVE_MESSAGES_ENABLED = false;

export const COMMENT_URL = "https://madebytle.com/presentation/<slug>/comment";

export async function getCommentQrSvg(): Promise<string> {
  return QRCode.toString(COMMENT_URL, {
    type: "svg",
    errorCorrectionLevel: "M",
    margin: 1,
    color: { dark: "#111827", light: "#FFFFFF00" }, // dark glyphs on transparent bg
  });
}
```

## Deck wiring

The deck takes two optional props and threads them through to the cover slide and the ticker:

```tsx
export default function Deck({
  initialSlide = 0,
  commentQrSvg,
  commentUrl,
}: {
  initialSlide?: number;
  commentQrSvg?: string;
  commentUrl?: string;
} = {}) {
  // ...existing deck state...
  return (
    <div className="fixed inset-0 bg-white overflow-hidden">
      {commentQrSvg && (
        <CommentTicker
          qrSvg={commentQrSvg}
          commentUrl={commentUrl}
          hidden={active === 0}  // cover slide already shows the QR; hide ticker there
        />
      )}
      {/* ...stage / canvas / slides... */}
      {/* On the cover slide, render a `<QrBadge svg={commentQrSvg} />` inline next to the title.
          See bni-5min-deck.tsx for the exact JSX pattern. */}
    </div>
  );
}
```

The deck's `page.tsx` and `[slug]/page.tsx` (server components) call `getCommentQrSvg()` and pass the SVG + URL down:

```tsx
// page.tsx
import Deck from "./<slug>-deck";
import { COMMENT_URL, LIVE_MESSAGES_ENABLED, getCommentQrSvg } from "./comment-qr";

export default async function Page() {
  const commentQrSvg = LIVE_MESSAGES_ENABLED ? await getCommentQrSvg() : undefined;
  return (
    <Deck
      commentQrSvg={commentQrSvg}
      commentUrl={LIVE_MESSAGES_ENABLED ? COMMENT_URL : undefined}
    />
  );
}
```

## `<CommentTicker>` (client)

Pinned to viewport bottom-left (NOT inside the canvas — it stays upright in landscape mode), `aria-live="polite"` so screen readers announce new messages. UI states:

- **Idle** (no recent messages): renders the small QR badge with the prompt "ส่งข้อความขึ้นจอ".
- **Active** (one or more messages): renders up to `MAX_VISIBLE = 3` messages stacked, newest at the bottom. Each fades out after `VISIBLE_DURATION_MS = 12_000` (with a 600ms fade-out at the end).
- The two faces are siblings absolutely overlaid at the same anchor; the ticker uses a small CSS `rotateX` flip to transition between idle/active so it reads as a single object turning over.

Reference: `bni-5min/comment-ticker.tsx` is the canonical implementation. Keep its: visible/fade timing constants, `aria-live="polite"`, `pointer-events-none`, the cleanup of timeouts on unmount, and the `subscription.removeChannel` on cleanup.

## `/<slug>/comment` submission page

A public `'use client'` form with: name (max 30 chars, optional), message (max 200 chars, required), submit button. On submit, call a server action / route handler that:

1. Validates inputs server-side.
2. Optionally rate-limits per IP (recommended — a hostile audience member can otherwise spam the wall mid-talk).
3. Inserts into the `<slug>_comments` table.
4. Returns a confirmation; the form clears for the next submission.

No login. The page is intentionally low-friction.

## Env vars

```
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=...
```

The publishable (anon) key is used both server-side (for the form insert) and client-side (for the realtime subscription). Lock the table down to "insert + select for anon role on `<slug>_comments` only" via row-level security.

## Don't

- Don't render the ticker on the cover slide — the cover already shows a large QR badge. `hidden={active === 0}` keeps it from doubling up.
- Don't render the ticker inside the rotated canvas — it must live in the deck root so it stays upright when landscape mode is toggled.
- Don't ship with `LIVE_MESSAGES_ENABLED = true` until the Supabase table + RLS + rate limiter are in place. The flag is the off-switch.
