# Presentation Deck Checklist

Design rules + the "is this deck complete?" gate. Read **before delivering a new deck** and **before declaring an existing deck up-to-date**. Walk every line: tick (✓) or flag (✗ + what's missing), then fix every flag before reporting back to Tle. Every item is a hard requirement unless marked optional.

---

## Design rules (Tle's standing preferences)

- **Font**: Noto Sans Thai — inherited from `madebytle/src/app/layout.tsx`; never re-import `next/font`, never `font-sans`/`font-*` on content (only `font-mono` on `SlideNumber` + pill counter)
- **Icons**: `@heroicons/react/24/outline` (or `/24/solid`). **Never emoji — anywhere** (icons, headings, labels, card text, callouts, tags, step lists, mockups; emoji read as AI-generated). Map: status → `CheckCircleIcon`/`XCircleIcon`, lock → `LockClosedIcon`, database → `CircleStackIcon`, note → `PencilSquareIcon`, warning → `ExclamationTriangleIcon`, gift → `GiftIcon`, swap/"your business" → `ArrowsRightLeftIcon`. Typographic arrows `→ ← ↔` in text are fine
- **Colours**: Tailwind classes only, no hardcoded hex (exceptions: inside the `theme`/`ACCENT` object for Korat City Show and v3 client palettes; v3 scrims are `bg-black/NN`, cut-out outline uses `var(--color-*)`)
- **Typography**: 5-size system (Large / H1 / H2 / Normal / Small) per [`typography.md`](./typography.md). Never `text-Xxl text-Yxl` (duplicate-class trap), never `md:text-*` inside slides
- **Layout**: default `align="top"`; only Cover / LCD / Closing use `align="center"`. Never split a slide into disconnected bands. Each card / row / column fills ~75% of canvas height — bump padding, `aspect-[X/Y]` for hero images, balance 2-col heights (gallery → "Layout principles")
- **Canvas mode**: every slide is a fixed 1920×1080 `SlideShell` scaled by `DeckShell` — no `w-screen`/`h-screen`, no responsive prefixes
- **Full-bleed canvas, no frame chrome**: the shell fills the viewport; no gray padding, shadow, ring or rounded corners around the canvas (the old "frame in gray bg" double-shrunk fonts — do not reintroduce)
- **Dashed canvas frame, always on**: `SlideShell` applies `theme.frameOutline` in dev AND prod — Tle wants the 1920×1080 boundary visible during live presentations and on portrait viewports. Every theme MUST define `frameOutline`
- **Rotate support**: controls live outside the rotated canvas (the pill) so labels stay upright; slides are 1920×1080 in both orientations
- **Whitespace**: `px-20` inside slides, `max-w-[1600px]` content width (v3 `max-w-[1760px]`)
- **Safe area**: `pt-24 pb-40` (v3 `pt-28`) reserves 160 canvas-px at the bottom. Visible content ends at canvas **y ≤ 920** — anything lower is under the pill. Watch `h-[480px]+` media, `aspect-[4/3]` in wide columns, long Thai wraps. Always run the safe-area audit (SKILL.md Step 5)
- **Contrast**: never light-gray text on white
- **Aspect**: 16:9 only
- **Numbers**: `Intl.NumberFormat('en-US')` for ≥ 1,000
- **A11y**: icon-only buttons have `aria-label`; every `<Image>` has `alt` (or `aria-hidden` when decorative)
- **Theme**: respect the chosen tokens; don't mix presets or versions

## File structure

- [ ] `<slug>-deck.tsx` (`"use client"`), `slide-slugs.ts` (NOT `"use client"` — importing constants from a client file into the server route fails the build), `[slug]/page.tsx`, `page.tsx`, `layout.tsx`
- [ ] `layout.tsx`: title / description / OG, `robots: { index: false }` when not public; wrapper `bg-white min-h-screen` (v3: `bg-neutral-950`)

## Shell (imported — not re-implemented)

- [ ] `import DeckShell, { BASE_W, BASE_H } from "../_shared/deck-shell"` — no local `BASE_W`/`BASE_H`, no stage / zoom / scroll / keyboard / pill code in the deck (incident 10 ต.ค. 2569: the same ~250 lines were pasted into every deck; chrome fixes never reached older decks)
- [ ] `<DeckShell slugs={SLIDE_SLUGS} basePath={BASE_PATH} initialSlide={initialSlide}>` wraps **only** `SlideShell`s; `chrome.rootBg` = `bg-white` for light decks (default is `bg-neutral-950`)
- [ ] Behaviours the shell guarantees — verify once after a shell edit, never re-implement: `scrollToSlide` uses `BASE_W` not `clientWidth` (the rail is transform-scaled; `clientWidth` broke nav at zoom ≠ 1); `useLayoutEffect` deep-link jump before paint + `hasMountedRef` so the mount-time scroll doesn't overwrite the deep-link URL with `/cover`; `history.replaceState` not the Next router; keys `← → Space PageUp PageDown Home End` + zoom `+ - 0` + clicker `Tab`/`Enter` with `preventDefault`; pill `w-max whitespace-nowrap max-w-[calc(100vw-1rem)]` (without them the pill bg rendered narrower than its content on phones and the landscape button floated outside); dot row + zoom group `hidden sm:flex`
- [ ] One pill only — no top bar, no second floating widget. Allowed extras: `extraTopLeft` (PDF / TOC buttons), viewport-pinned TOC drawer / ticker as siblings (see [`addons.md`](./addons.md))
- [ ] `globals.css` still has `[data-landscape="true"] .deck-digit-rotate { transform: rotate(-90deg) }`

## Primitives (per deck, from the chosen gallery)

- [ ] `SlideShell` → `<section data-slide data-total data-label>` 1920×1080, `snap-start shrink-0`, `px-20 pt-24 pb-40` (v3 `pt-28` or `bare`), `${theme.bg} ${theme.frameOutline}`; v1 takes `bgImage`/`bgAlt`/`align`, v2 adds `variant`/`motif`, v3 takes `photo`/`scrim`/`position`/`blur`
- [ ] `Kicker` — `text-[11px] tracking-[0.3em] uppercase ${theme.kicker} font-semibold`, `spacing` prop; Thai headings ≥ `text-7xl` get `spacing="mb-10"` + `pt-2 leading-[1.05]` (diacritics overlap the kicker otherwise). v3 uses `CapsLabel` instead
- [ ] `SlideNumber` — `absolute top-6 right-8 text-xs font-mono`, both digits in `<span className="deck-digit-rotate">`, slash NOT counter-rotated
- [ ] Every slide has `<SlideNumber current={N} total={totalSlides} />`
- [ ] Phone / device mockups lock **width AND height** — content never drives the size

## Theme

- [ ] One `const theme = { … } as const` at the top; tokens `bg text muted subtle accent accentBg kicker frameOutline` (v3: no `accent`/`accentBg`/`kicker` — colour comes from `ACCENT[key]`); matches a preset in [`themes.md`](./themes.md)

## Routing

- [ ] `/<slug>` lands on slide 1; `/<slug>/<slide-slug>` deep-links
- [ ] `generateStaticParams` returns all `SLIDE_SLUGS`; `generateMetadata` returns `{}` for unknown slugs; `notFound()` on unknown slug
- [ ] `SLIDE_SLUGS` order matches the `SlideShell` order

## Slide content

- [ ] No `sm:`/`md:`/`lg:` inside slides · no duplicate size classes · no `text-xs` or < 14px prose outside mockup chrome
- [ ] All content ends at y ≤ 920 — safe-area audit returns `failures: []`
- [ ] Teaching decks: every tool slide has an illustrative mockup tagged `ภาพประกอบ`
- [ ] Client decks: numbers/dates not given by Tle are principles tagged `รอเคาะ`; proposals tagged `ข้อเสนอ`; guesses `// TODO: confirm with Tle`

## Verification

- [ ] `npx tsc --noEmit` · `pnpm lint` · `pnpm build` prerenders every `[slug]` route
- [ ] Safe-area audit `failures: []` · the three greps clean (SKILL.md Step 5)
- [ ] Deployed with `vercel deploy --prod --yes` and `curl` on the prod URL returned 200 (`git push` alone publishes nothing)

## Optional features (only what Tle ticked — [`addons.md`](./addons.md))

- [ ] TOC: `SECTIONS`/`QUICK_LINKS` slide numbers 1-based and ≤ `totalSlides`; menu button via `extraTopLeft`; drawer `z-50`; `M` opens / `Esc` closes; nav keys ignored while open
- [ ] PDF: under `public/presentation/<slug>/`, `<a download>` via `extraTopLeft`, **regenerated after the latest content change**
- [ ] Progress markers: `sections` prop, 0-based `start`
- [ ] Live messages: ticker outside the canvas, hidden on the cover, `LIVE_MESSAGES_ENABLED` flag
- [ ] Audio narration (if ever): inline player on the **left** of the pill behind a divider, auto-advance on `ended`, autoplay gated behind first click — never a separate widget

## Must NOT be in the deck

- [ ] No `useSearchParams` / `?slide=N` — deep-link slugs only
- [ ] No `cleanMode` / embed mode — single canonical view
- [ ] No `Suspense` around the deck unless a hook needs it
- [ ] No `next/font` import in deck or layout

## v3 (The Standard) deviations

- [ ] `layout.tsx` wrapper `bg-neutral-950 min-h-screen`; `DeckShell` default `rootBg` already dark
- [ ] `SlideShell` has `relative isolate`, `px-20 pt-28 pb-40` (or `bare`); content wrapper is **not** positioned so absolute chrome anchors to the slide
- [ ] Every slide has a photo layer — none is a flat colour
- [ ] Layers crossing the safe area or an edge carry `data-bleed`; full-height structural wrappers carry `data-fill` (the audit skips both)
- [ ] Cut-outs are transparent PNGs from `scripts/cutout.swift`, checked on a coloured background
- [ ] The six visual checks in the v3 "Audit" section pass on every slide
