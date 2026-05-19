---
name: kiki-presentation
description: Build web-based presentation decks and deploy them under madebytle.com/presentation/<project-slug>. Use when the user asks to "make a presentation", "create slides", "build a deck", "ทำ presentation", "ทำสไลด์", "พรีเซน" — works from inside any project directory. Scans the current project for context, asks the user via AskUserQuestion about audience + theme + content, then writes a 15-slide React deck into the MakeByTle.com Next.js app and verifies it locally.
---

# kiki-presentation — Web Presentation Builder

Build a presentation as a Next.js page that lives at **`madebytle.com/presentation/<slug>`**. Works from inside any project — the current project provides *content*, the deck always deploys to MakeByTle.com.

## Concept in one line

> **Anywhere you're working, "make me a presentation" → a deployed web deck under `madebytle.com/presentation/<slug>`.**

The deck is a single React component using Tailwind + Heroicons + Noto Sans Thai, with horizontal scroll-snap slides and keyboard navigation. It opens on any device, including a TV/projector.

## Inputs (always confirm via AskUserQuestion)

| # | Input | Source |
|---|-------|--------|
| 1 | **Slug** | Suggest from current dir name; ask Tle to confirm/edit |
| 2 | **Audience** | "BNI / Pitch / Internal team / Client / Conference" — drives slide selection |
| 3 | **Theme** | Always ask, even if defaulting (see [themes.md](./themes.md)) |
| 4 | **Title + tagline** | Read from `CLAUDE.md` / `README.md`; confirm |
| 5 | **Services / sections** | Project-dependent |
| 6 | **Looking for** | Skip for non-BNI decks |
| 7 | **Trigger words** | Skip for non-BNI decks |
| 8 | **Contact** | Default to Tle's standard (email/phone/web); confirm |

## Output (file paths)

The deck **always** lives in the MakeByTle.com Next.js repo. Every slide gets its own deep-linkable URL — required for sharing, commenting, and "jump to slide" use cases:

```
/Users/tlej/Works (Local)/Vibe Docs/00 Made by Tle/madebytle/src/app/presentation/<slug>/
├── layout.tsx        # metadata (title, description, OG)
├── page.tsx          # renders <Deck /> at /<slug> (defaults to slide 1)
├── slide-slugs.ts    # SLIDE_SLUGS, SLIDE_TITLES, BASE_PATH (shared by deck + dynamic route)
├── [slug]/page.tsx   # renders <Deck initialSlide={index} /> at /<slug>/<slide-slug>
└── <slug>-deck.tsx   # the React component (the actual slides)
```

URLs:
- `https://madebytle.com/presentation/<slug>` — root, lands on slide 1
- `https://madebytle.com/presentation/<slug>/<slide-slug>` — deep link to a specific slide

Dev: `http://localhost:3000/presentation/<slug>` and `…/<slug>/<slide-slug>`.

## Workflow

### Step 1 — Scan the current project (no questions yet)

Before asking Tle anything, gather context:

```bash
# What project am I in?
pwd
ls
cat CLAUDE.md 2>/dev/null
cat README.md 2>/dev/null
cat package.json 2>/dev/null | head -30
```

Use this to **suggest** sensible defaults for slug, title, and tagline. Don't ask Tle for facts that are visible in the repo.

### Step 2 — Pick audience type

Use `AskUserQuestion` to ask **what kind of presentation**, since this drives which slide templates to use:

- **BNI 5-min** → use the full 15-slide BNI structure (Cover → About → Why → Services → LCD → ServiceDetail → Strengths → Customers → Case → Looking-For → Triggers → Script → Misconceptions → Closing). See [`bni-structure.md`](./bni-structure.md).
- **Pitch deck** → Cover, Problem, Solution, Market, Product Demo, Traction, Business Model, Team, Ask, Closing.
- **Project handover / Internal demo** → Cover, Context, What We Built, Demo, Tech Stack, Results, Next Steps, Closing.
- **Conference talk** → Cover, Hook, 3-5 Sections, Closing/CTA.
- **Custom** → ask Tle for a slide outline.

### Step 3 — Always ask theme

This is required every time. See [`themes.md`](./themes.md) for the preset gallery. The four standing presets:

1. **MakeByTle (default)** — white bg, amber accent, Noto Sans Thai
2. **Premium Dark** — navy/black bg, gold accent, Noto Sans Thai
3. **Gradient AI** — gradient bg (purple/blue/cyan), white text, Noto Sans Thai
4. **Custom** — user picks primary color + light/dark mode

### Step 4 — Gather remaining content

Use `AskUserQuestion` for content the project doesn't provide. Batch related questions; cap at 4 questions per turn.

### Step 4.5 — Wire deep-linkable per-slide URLs (mandatory)

Every deck must give every slide its own URL. People share decks by linking to a specific slide; comments reference slides by URL. Hash fragments (`#cover`) are not enough — Tle wants real path segments.

Create three files:

**`slide-slugs.ts`** — shared module (NOT `"use client"`) so the dynamic route (server component) can import the constant. Importing constants from a `"use client"` file into a server component fails the build.

```ts
// Order MUST match the SlideShell components in the deck.
export const SLIDE_SLUGS = [
  "cover", "about", "why-choose-us", /* ... */, "closing",
] as const;
export type SlideSlug = (typeof SLIDE_SLUGS)[number];
export const BASE_PATH = "/presentation/<slug>";
export const SLIDE_TITLES: Record<SlideSlug, string> = {
  cover: "Cover",
  about: "About — …",
  // ... one human-friendly title per slug for <title> metadata
};
```

**`[slug]/page.tsx`** — server component that maps slug → index → passes to deck:

```tsx
import { notFound } from "next/navigation";
import Bni5MinDeck from "../<slug>-deck";
import { SLIDE_SLUGS, SLIDE_TITLES, type SlideSlug } from "../slide-slugs";

export function generateStaticParams() {
  return SLIDE_SLUGS.map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const title = SLIDE_TITLES[slug as SlideSlug];
  if (!title) return {};
  return { title: `${title} — <Brand> · <Deck>` };
}

export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const index = SLIDE_SLUGS.indexOf(slug as SlideSlug);
  if (index === -1) notFound();
  return <Bni5MinDeck initialSlide={index} />;
}
```

**Deck component** — accepts `initialSlide` prop, jumps there on mount, syncs URL on scroll:

```tsx
import { useLayoutEffect, useEffect, useRef, useState } from "react";
import { SLIDE_SLUGS, BASE_PATH } from "./slide-slugs";

export default function Deck({ initialSlide = 0 }: { initialSlide?: number } = {}) {
  const [active, setActive] = useState(initialSlide);
  const containerRef = useRef<HTMLDivElement>(null);
  const hasMountedRef = useRef(false);

  // Set scrollLeft synchronously BEFORE paint so scroll-snap-mandatory doesn't
  // snap-back to 0. Use scrollLeft assignment, not scrollTo (smoother).
  useLayoutEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    if (initialSlide > 0) el.scrollLeft = initialSlide * BASE_W;
    requestAnimationFrame(() => { hasMountedRef.current = true; });
  }, [initialSlide]);

  // Mirror active slide into URL via history.replaceState — no Next.js router,
  // no remount. The hasMountedRef guard ignores the synthetic scroll event from
  // the mount-time scrollLeft assignment.
  useEffect(() => {
    if (typeof window === "undefined" || !hasMountedRef.current) return;
    const slug = SLIDE_SLUGS[active];
    if (!slug) return;
    const target = `${BASE_PATH}/${slug}`;
    if (window.location.pathname !== target) {
      window.history.replaceState(null, "", target);
    }
  }, [active]);

  // ...rest of deck (scroll tracker that calls setActive, scrollToSlide, etc.)
}
```

**Why this pattern works:**
- `useLayoutEffect` + `scrollLeft` assignment runs before browser paint → no flash, no race with snap-mandatory.
- `history.replaceState` (not Next.js `router.replace`) updates the URL bar without triggering navigation, RSC fetches, or remount — purely cosmetic URL sync.
- `hasMountedRef` guard prevents the mount-time scroll event from clobbering the deep-link URL with `/cover`.
- Root URL `/<slug>` (no slide-slug) lands on slide 1 and starts URL-syncing once the user scrolls.

### Step 5 — Build the deck

Use the slide templates in [`slide-templates.md`](./slide-templates.md) — that file is the full gallery (primitives + every slide pattern) **and** holds the canonical canvas root / controls pill / keyboard nav blocks. **Read it when you build**; it is the source of truth.

The viewport, controller, and font handling are now **locked patterns** — paste them in verbatim from [`slide-templates.md`](./slide-templates.md) (`## Canvas mode` section). Do not invent your own scaffolding.

Skeleton (top-level structure of `<slug>-deck.tsx`) — this is the *outer shape*; the inner state/markup blocks come straight from `slide-templates.md → Canvas mode`:

```tsx
"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import {
  ArrowLeftIcon, ArrowRightIcon, ArrowsPointingOutIcon,
  // ...other Heroicons as needed
} from "@heroicons/react/24/outline";
import { SLIDE_SLUGS, BASE_PATH } from "./slide-slugs";

// --- Data (extracted from inputs, kept at top of file for easy editing) ---
const services = [/* ... */];
const customers = [/* ... */];

// --- Canvas constants (locked — never change) ---
const BASE_W = 1920;
const BASE_H = 1080;

// --- Primitives (paste from slide-templates.md → Primitives) ---
function SlideShell({ children, number, total, label, bgImage, bgAlt, align = "top" }) { /* ... */ }
function Kicker({ children, spacing = "mb-4" }) { /* ... */ }
function SlideNumber({ current, total }) { /* ... */ }

// --- Deck ---
export default function <PascalSlug>Deck({
  initialSlide = 0,
}: { initialSlide?: number } = {}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const stageBoxRef = useRef<HTMLDivElement>(null);
  const [active, setActive] = useState(initialSlide);
  const [landscapeMode, setLandscapeMode] = useState(false);
  const [stageScale, setStageScale] = useState(1);
  const [stageW, setStageW] = useState(BASE_W);
  const [stageH, setStageH] = useState(BASE_H);
  const totalSlides = N;

  // 1. Stage scaling + rotation effect          → slide-templates.md (Canvas root)
  // 2. scrollToSlide(index)                      → slide-templates.md (Scrolling math)
  // 3. onScroll → setActive                      → slide-templates.md (Scrolling math)
  // 4. useLayoutEffect → initialSlide jump       → SKILL.md step 4.5
  // 5. useEffect → history.replaceState URL sync → SKILL.md step 4.5
  // 6. Keyboard nav (← → Space Home End PageUp/Down) → slide-templates.md (Keyboard nav)

  return (
    <div className="fixed inset-0 bg-white overflow-hidden">
      {/* Stage area — viewport minus 96px bottom strip for the controls pill */}
      <div ref={stageBoxRef} className="absolute top-0 left-0 right-0 bottom-24 flex items-start justify-center">
        {/* Frame — pure clipper, no chrome */}
        <div className="relative overflow-hidden" style={{ width: stageW, height: stageH }}>
          {/* Canvas — 1920×1080, optionally rotated 90° */}
          <div
            data-landscape={landscapeMode ? "true" : "false"}
            className="absolute top-0 left-0"
            style={{
              width: BASE_W,
              height: BASE_H,
              transformOrigin: "top left",
              transform: landscapeMode
                ? `translate(${stageW}px, 0) rotate(90deg) scale(${stageScale})`
                : `scale(${stageScale})`,
            }}
          >
            {/* Slide rail */}
            <div
              ref={containerRef}
              style={{ width: BASE_W, height: BASE_H }}
              className="overflow-x-auto overflow-y-hidden snap-x snap-mandatory scroll-smooth flex [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden"
            >
              {/* ...slides built from templates... */}
            </div>
          </div>
        </div>
      </div>
      {/* Controls pill — paste from slide-templates.md (Controls pill) */}
    </div>
  );
}
```

> **Why this exact shape?** It's been validated in production (`bni-5min-deck.tsx`):
> - `fixed inset-0` makes the deck full-bleed with no frame chrome (no double-shrink of fonts).
> - `bottom-24` reserves a 96px strip so the floating controls pill never covers slide content — even when the canvas is rotated 90° in landscape mode.
> - Stage width/height (`stageW`/`stageH`) drives the *frame* size; `stageScale` drives the *canvas* transform. This separation lets the canvas rotate in place inside its scaled frame.
> - Slides themselves are always laid out as if the screen is exactly 1920×1080 — no responsive prefixes, no media queries. The shell does all the responsive work.

### Step 6 — Verify locally + visual layout audit

```bash
cd "/Users/tlej/Works (Local)/Vibe Docs/00 Made by Tle/madebytle"
pnpm dev   # background
# Wait for "Ready" then open http://localhost:3000/presentation/<slug>
```

**If chrome-devtools MCP is available, run the automated safe-area audit before reporting back.** Don't trust eyeballed screenshots alone — content that overflows the canvas safe area gets covered by the floating controls pill and is visually easy to miss in a screenshot taken at viewport size.

### Automated audit (run in chrome-devtools)

```js
// Paste this into chrome-devtools `evaluate_script` after navigating to the deck:
async () => {
  const slides = document.querySelectorAll('[data-slide]');
  const rail = slides[0].parentElement;
  const slide0 = slides[0];
  const scale = slide0.getBoundingClientRect().width / 1920;
  const controls = document.querySelector('.absolute.bottom-4');
  const cRect = controls?.getBoundingClientRect();
  const safetyZoneCanvasPx = ((window.innerHeight - (cRect?.top ?? window.innerHeight)) / scale);
  const failures = [];
  for (let i = 0; i < slides.length; i++) {
    rail.scrollTo({ left: 1920 * i, behavior: 'auto' });
    await new Promise(r => setTimeout(r, 200));
    const slide = slides[i];
    const rect = slide.getBoundingClientRect();
    let maxBottom = 0, offender = null;
    slide.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      // Skip background images that intentionally fill the canvas
      if (el.tagName === 'IMG' && el.className.includes('-z-10')) return;
      const b = (r.bottom - rect.top) / scale;
      if (b > maxBottom) { maxBottom = b; offender = el.tagName + '.' + (el.className||'').split(' ').slice(0,2).join('.'); }
    });
    if (maxBottom > 1080 - safetyZoneCanvasPx) {
      failures.push({ slide: i+1, bottomY: Math.round(maxBottom), offender: offender?.slice(0, 60) });
    }
  }
  return { scale, safetyZoneCanvasPx: Math.round(safetyZoneCanvasPx), failures };
}
```

**If `failures` is non-empty, fix every entry before deploying.** The most common culprits:
- Fixed-height media (`h-[480px]+` collages) — reduce to `h-[400px]` or use `aspect-[X/Y]` for a media-grid that scales with width
- `aspect-[4/3]` images in wide columns (`col-span-7+`) — switch to `aspect-[16/9]` or smaller column span
- Long Thai text in narrow cards — widen the container, soften wrap with `break-words`/`break-all`, or restructure
- Misconception/script lists with too-tall padding combined with multi-line text

### Visual layout checks (per slide)
1. **Top-anchored or hero-centered?** Anything that isn't Cover/LCD/Closing should use the default `align="top"`.
2. **Bands of content with empty stripes?** If yes, restructure into a single coherent block (per Layout principle #2).
3. **Content fills ≥ ~75% of canvas height (~750 of 920 budget)?** If far less, bump padding / use `aspect-[X/Y]` / add supporting content.
4. **2-column heights balanced?** If one column ends way before the other, fill the shorter one.
5. **Card text overflows its card boundary?** Widen container or apply `break-words` / `break-all`. Add `auto-rows-fr` on the parent grid to keep card heights equal.

Also verify Thai font renders, no kicker/heading overlap, no horizontal scrollbars within a slide.

### Step 7 — Report back

Report in Thai. Include:
- ✅ URL (dev + production)
- 📁 Files created
- ⚠️ **Anything you guessed** — list each `// TODO: confirm with Tle` so Tle can verify
- 🚀 Next step suggestion (e.g. "deploy via git push")

## Design Rules (apply every time — Tle's standing preferences)

- **Font**: `Noto Sans Thai` (already loaded in MakeByTle's `src/app/layout.tsx` — don't re-import)
- **Icons**: `@heroicons/react/24/outline` (and `/24/solid` when needed). **Never emoji.**
- **Colors**: Tailwind classes only. No hardcoded hex.
- **Typography**: follow [`typography.md`](./typography.md) — 5-size system (Large/H1/H2/Normal/Small), no others. **Never** use `text-Xxl text-Yxl` (duplicate-class trap) and **never** use `md:text-*` inside slide content (canvas mode invalidates responsive prefixes).
- **Layout**: follow the **Layout principles** section of [`slide-templates.md`](./slide-templates.md). Key rules: (a) default `align="top"` on `SlideShell`, only Cover/LCD/Closing use `align="center"`; (b) never split a slide into disconnected bands of content; (c) each card / row / column should fill ~75% of the canvas height — bump padding, use `aspect-[X/Y]` for hero images, balance 2-col heights.
- **Canvas mode**: every slide is a fixed 1920×1080 box scaled-to-fit by the deck root. Don't use `w-screen`/`h-screen` for slides — use the canonical `SlideShell` from [`slide-templates.md`](./slide-templates.md), which sets `width: 1920px; height: 1080px` explicitly.
- **Full-bleed canvas (no frame chrome)**: the deck root has `bg-white` and the canvas fills the *entire viewport* with `absolute inset-0` — **no** gray padding, **no** shadow/ring/rounded around the canvas. The earlier "frame inside gray bg" layout double-shrunk the slide; do not reintroduce it.
- **Dashed canvas frame on every slide (always on)**: `SlideShell` applies `theme.frameOutline` (e.g. `outline-dashed outline-1 -outline-offset-1 outline-gray-300`) on every slide, in development AND production. Tle's preference — the visible 1920×1080 boundary helps during live presentations and on portrait viewports where the canvas doesn't fill the screen. Do not remove it. New themes MUST define `frameOutline` (see [`themes.md`](./themes.md)).
- **Rotate support**: the deck root supports portrait phones via a 90° CSS rotation. Controls overlay lives **outside** the rotated canvas (floating pill at viewport bottom) so labels stay upright. Slides themselves are 1920×1080 in both orientations.
- **Whitespace**: generous — `px-20` padding inside slides, `max-w-[1600px]` content max width
- **Safe area**: `SlideShell` uses `pt-24 pb-40` (160 canvas-px bottom reserve). Visible content must end at canvas y ≤ 920 — anything past that is covered by the floating controls pill. Watch for: large fixed-height media (`h-[480px]+`), `aspect-[4/3]` images in wide columns (very tall), long Thai text wrapping. **Always run the safe-area audit** (Step 6) before reporting back.
- **Contrast**: never light-gray text on white bg
- **Aspect**: 16:9 (1920×1080) only — every slide is canvas-fixed at this size
- **Number formatting**: `Intl.NumberFormat('en-US')` for ≥1,000
- **A11y**: every icon-only button needs `aria-label`; every image needs `alt`
- **Theme**: respect the chosen theme tokens; don't mix presets

### Post-build audit (run before reporting back)

```bash
DECK=src/app/presentation/<slug>/<slug>-deck.tsx

# 1. No duplicate text-size classes (silent bug from removing `md:` half-way)
grep -nE 'text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)[^"]*text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)' "$DECK"

# 2. No responsive prefixes inside slides
grep -nE '(md|lg|sm):(text-|grid-cols-|col-span-)' "$DECK"

# 3. No tiny prose (text-xs or smaller) outside mockup chrome
grep -nE 'text-xs|text-\[1[0-3]px\]|text-\[9px\]' "$DECK"
```

If any of these return matches outside intentional mockup chrome, fix before delivering.

## Optional add-on: live audience messages (cover-QR + bottom-left ticker)

Some decks (e.g. BNI presentations where the audience is sitting in front of the speaker) include a real-time message wall:

- **On the cover slide** — a QR code badge inviting attendees to scan and submit a comment.
- **On every other slide** — a bottom-left "ticker" that flips between (a) the QR badge when idle, and (b) live messages as they arrive.

Build it only when Tle asks for "live messages", "comment ticker", "audience interaction", or similar. The pattern is documented in [`live-messages.md`](./live-messages.md). It uses Supabase Realtime + a public `/<slug>/comment` form page; it's gated behind a `LIVE_MESSAGES_ENABLED` flag so you can ship the deck without lighting up the realtime backend.

When NOT building this feature, just skip it — none of the core deck patterns depend on it.

## Templates are upgradable (do not modify during a build)

The slide templates in [`slide-templates.md`](./slide-templates.md) are the **source of truth**. When you build a deck, you **read** templates and apply them — you do not modify them.

When Tle asks to "upgrade the template" or "improve slide X", that is a separate task: **edit the template file directly**. The change applies to **future** decks only — existing decks (already-written `<slug>-deck.tsx` files) are static React snapshots and remain untouched.

This is the contract: **templates evolve, decks freeze**.

## Reference files (read these as needed)

| File | When to read |
|------|--------------|
| [`checklist.md`](./checklist.md) | **Always** — single source-of-truth for "deck complete?". Read before delivering, walk every line, fix every flag |
| [`typography.md`](./typography.md) | **Always** before sizing any text — fixed scale, minimum sizes, canvas-mode rules |
| [`themes.md`](./themes.md) | Step 3 (always) |
| [`slide-templates.md`](./slide-templates.md) | Step 5 (always — canvas root + primitives + every slide pattern) |
| [`bni-structure.md`](./bni-structure.md) | When audience = BNI |
| [`live-messages.md`](./live-messages.md) | When Tle asks for live audience messages / cover-QR + ticker |
| [`examples.md`](./examples.md) | When you want a working reference deck |

## Things to never do

- ❌ Build outside of `00 Made by Tle/madebytle/`. The deck **always** deploys to MakeByTle.com.
- ❌ Skip the theme question. Always ask, even when defaulting.
- ❌ Use emoji as icons.
- ❌ Hardcode hex colors.
- ❌ Modify slide-template files as part of building a deck.
- ❌ Invent personal-branding content. Mark guesses with `// TODO: confirm with Tle`.
- ❌ Use plain-text questions when you should use `AskUserQuestion`.
