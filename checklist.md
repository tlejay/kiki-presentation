# Presentation Deck Checklist

The single source-of-truth for "is this deck complete?" Read this **before delivering a new deck** and **before declaring an existing deck up-to-date**. Every item is a hard requirement unless explicitly marked optional.

When auditing an existing deck, walk every line and tick (✓) or flag (✗ + what's missing). Then fix every flag before reporting back to Tle.

---

## File structure

- [ ] `<slug>-deck.tsx` — the React component
- [ ] `slide-slugs.ts` — `SLIDE_SLUGS`, `SLIDE_TITLES`, `BASE_PATH` (NOT `"use client"`)
- [ ] `[slug]/page.tsx` — server component, calls `generateStaticParams` + `generateMetadata`, passes `initialSlide` to deck
- [ ] `page.tsx` — server component, renders `<Deck />` with no `initialSlide` (defaults to slide 1)
- [ ] `layout.tsx` — metadata (title template, description, OG)

## Canvas + Stage (layout shell)

- [ ] `BASE_W = 1920`, `BASE_H = 1080` constants — never edit
- [ ] Deck root: `<div className="fixed inset-0 bg-white overflow-hidden">` — no frame chrome, no gray padding
- [ ] Stage: `<div ref={stageBoxRef} className="absolute top-0 left-0 right-0 bottom-24 flex items-start justify-center">` — `bottom-24` reserves the controls strip
- [ ] Frame (clipper): `<div className="relative overflow-hidden" style={{ width: stageW, height: stageH }}>` — pure clipper, no shadow/ring/rounded
- [ ] Canvas: 1920×1080 div with `transformOrigin: "top left"` and `transform: scale(...)` (or rotate+scale in landscape)
- [ ] Canvas has `data-landscape={landscapeMode ? "true" : "false"}` attribute
- [ ] `useEffect` hooks resize observer + window resize + orientationchange listeners → recompute scale + stageW + stageH
- [ ] Slide rail: scroll container with `snap-x snap-mandatory scroll-smooth` and hidden scrollbars

## Primitives

- [ ] `SlideShell` accepts `{ children, number, total, label?, bgImage?, bgAlt?, align? }`, renders fixed `1920×1080` section with `snap-start shrink-0`, padding `px-20 pt-24 pb-40`, includes `${theme.bg} ${theme.frameOutline}`
- [ ] `Kicker` — `text-[11px] tracking-[0.3em] uppercase ${theme.kicker} font-semibold`, accepts `spacing` prop
- [ ] `SlideNumber` — `absolute top-6 right-8`, both digits wrapped in `<span className="deck-digit-rotate">`, slash NOT counter-rotated
- [ ] Every slide includes a `<SlideNumber current={N} total={totalSlides} />`

## Theme

- [ ] Theme tokens declared in one `const theme = { ... } as const` block at top of deck (or imported)
- [ ] Tokens include: `bg`, `text`, `muted`, `subtle`, `accent`, `accentBg`, `kicker`, **`frameOutline`** (mandatory)
- [ ] `theme.frameOutline` example: `"outline-dashed outline-1 -outline-offset-1 outline-gray-300"` — matches preset in [`themes.md`](./themes.md)
- [ ] No hardcoded hex colors anywhere in the deck

## CSS rule (in `globals.css`)

- [ ] `[data-landscape="true"] .deck-digit-rotate { transform: rotate(-90deg); ... }` rule present

## Deck state + behavior

- [ ] `useState(initialSlide)` for `active`
- [ ] `useState(false)` for `landscapeMode`
- [ ] `useState(BASE_W)` and `useState(BASE_H)` for stage dimensions, `useState(1)` for stage scale
- [ ] `useState(1)` for `zoom` (presenter canvas zoom) + `zoomIn`/`zoomOut`/`resetZoom`; auto-fit scale is multiplied by `zoom` and `zoom` is in the scale-effect deps
- [ ] Stage area is `overflow-auto` with a `min-w-full min-h-full flex items-start justify-center` wrapper around the frame (so a zoomed canvas can pan; top-aligned at zoom=1)
- [ ] `scrollToSlide(index)` callback uses `BASE_W` (NOT `el.clientWidth`)
- [ ] Scroll → setActive listener uses `Math.round(el.scrollLeft / BASE_W)`
- [ ] `useLayoutEffect` jumps to `initialSlide * BASE_W` on mount (deep-link support)
- [ ] `hasMountedRef` guard exists so the mount-time scroll doesn't clobber the URL
- [ ] URL sync `useEffect` mirrors `active` slide via `window.history.replaceState` (not router)
- [ ] Keyboard nav handles `← → Space PageUp PageDown Home End` + zoom `+` / `-` / `0` (reset) + clicker keys `Tab` (zoom in) / `Enter` (zoom out), both with `preventDefault`

## Controls pill (single bottom-centered overlay)

- [ ] One pill only — no separate top bar, no separate floating widgets
- [ ] Pill classes include: `absolute bottom-4 left-1/2 -translate-x-1/2 w-max max-w-[calc(100vw-1rem)] flex items-center gap-1 sm:gap-2 ... whitespace-nowrap` — **`w-max` and `whitespace-nowrap` are mandatory** (without them, the pill bg renders narrower than its content on mobile and the rightmost button visually floats outside)
- [ ] Pill contents in order: prev arrow → counter → dot row (`hidden sm:flex`) → next arrow → divider → zoom group (`hidden sm:flex`: − / % / +) → divider → landscape toggle
- [ ] Zoom group uses `MagnifyingGlassMinusIcon` / `MagnifyingGlassPlusIcon`; % button resets zoom; `−`/`+`/`0` keys also wired; group is `hidden sm:flex` (collapses on narrow phones)
- [ ] Optional add-on (e.g. audio player): goes on the **left** side of the pill, separated by a divider before the prev arrow. Never as a separate floating widget.
- [ ] Landscape toggle uses `ArrowsPointingOutIcon`, has `aria-pressed` + `aria-label` + `title` (Thai), active state uses `theme.accentBg text-white`, transform `rotate-45` when active
- [ ] All icon-only buttons have `aria-label`

## Routing

- [ ] `/<slug>` (root) lands on slide 1
- [ ] `/<slug>/<slide-slug>` deep-links to that slide
- [ ] `generateStaticParams` returns all `SLIDE_SLUGS`
- [ ] `generateMetadata` looks up `SLIDE_TITLES[slug]`, returns `{}` for unknown slugs (so `notFound()` triggers 404)
- [ ] `notFound()` called when slug is unknown

## Slide content rules

- [ ] Default `align="top"` on every content slide — only Cover / LCD-statement / Closing use `align="center"`
- [ ] No `md:` / `lg:` / `sm:` responsive prefixes anywhere inside slide content (only allowed: `sm:` on the controls pill)
- [ ] No duplicate text-size classes (`text-4xl text-5xl` etc.)
- [ ] No `text-xs` or sizes < 14px in body prose (only allowed inside intentional mockup chrome)
- [ ] All slide content ends at canvas y ≤ 920 (`pt-24 pb-40` reserves space; safe-area audit should show 0 failures)
- [ ] Heroicons only — `@heroicons/react/24/outline` (or `/24/solid` when needed). **Never emoji.**
- [ ] Numbers ≥ 1,000 formatted via `Intl.NumberFormat('en-US')`
- [ ] Every `<Image />` has `alt` (or `aria-hidden` if decorative)

## Audit & verification (run before reporting back)

- [ ] Type check passes (`npx tsc --noEmit`)
- [ ] Lint passes (`pnpm lint`) — no errors in deck files
- [ ] Production build succeeds (`pnpm build`) and prerenders all `[slug]` routes via SSG
- [ ] Safe-area audit script (in `SKILL.md`) returns `failures: []`
- [ ] Three grep checks from `SKILL.md` post-build audit — all clean inside slide content

## Always-ask gate

- [ ] Asked Tle about a **Table of Contents** via `AskUserQuestion` (Step 4.6) — required every build, even though the feature is opt-in. See [`toc.md`](./toc.md)
- [ ] Asked Tle about a **Download-as-PDF** button via `AskUserQuestion` (Step 4.7) — required every build, even though opt-in

## Optional features (build only when Tle opts in)

- [ ] Table of Contents (สารบัญ) — Agenda slide + floating menu button + overlay jump drawer — see [`toc.md`](./toc.md). If enabled: `SECTIONS`/`QUICK_LINKS` slide numbers are 1-based and ≤ `totalSlides`; menu button at deck root (`z-40`, top-left, every slide); overlay `z-50`; `M` opens / `Esc` closes; `goTo(n) → scrollToSlide(n-1)`
- [ ] Download-as-PDF — static PDF (Playwright screenshot per slide → `magick *.jpg deck.pdf`) under `public/presentation/<slug>/`, + `<a download>` button at deck root (top-left, paired with TOC). See SKILL.md "Optional add-on: Download-as-PDF". **If enabled: regenerated after the latest content change** (PDF is a snapshot)
- [ ] Live audience messages (Supabase realtime + comment QR + ticker) — see [`live-messages.md`](./live-messages.md)
- [ ] Audio narration player — pre-generated WAVs + inline player in the controls pill (left side); auto-advance on `ended`; gate autoplay behind first user click

## Things that should NOT be in the deck

- [ ] No `useSearchParams` / no `?slide=N` param handling — use deep-link slugs instead
- [ ] No `cleanMode` / no embed mode — single canonical view only
- [ ] No `w-screen` / `h-screen` on slides — only the deck root uses viewport units (via `fixed inset-0`)
- [ ] No `Suspense` around the deck unless the deck itself uses a hook that needs it
- [ ] No top-bar header — the controls pill is the only deck chrome
- [ ] No second floating widget (audio player, progress dots, etc.) — everything lives inside the single pill. **Exception:** when the TOC is enabled, the floating "สารบัญ" menu button (deck root, top-left) is allowed — see [`toc.md`](./toc.md)

## v3 (The Standard) deviations

When the deck uses [`slide-templates-v3.md`](./slide-templates-v3.md), these lines replace the matching ones above:

- [ ] Deck root is `fixed inset-0 bg-neutral-950 overflow-hidden`; `layout.tsx` wrapper is `bg-neutral-950 min-h-screen`
- [ ] `SlideShell` has `relative isolate`, padding `px-20 pt-28 pb-40` (or `bare`), takes `photo` / `scrim` / `position` / `blur`; the content wrapper is **not** positioned
- [ ] No `Kicker` — `CapsLabel` instead; theme has no `accent`/`accentBg`/`kicker` (colour comes from `ACCENT[key]`)
- [ ] Every slide has a photo layer; none is a flat colour
- [ ] Decorative layers that cross the safe area or an edge carry `data-bleed`; full-height structural wrappers carry `data-fill`; the audit skips both
- [ ] Controls pill uses literal `text-gray-900` / `text-gray-500` / `bg-red-500` (not theme tokens)
- [ ] Cut-outs are transparent PNGs from `scripts/cutout.swift`, checked on a coloured background
- [ ] The six visual checks in the v3 file's "Audit" section pass on every slide
