# Canvas shell — `DeckShell` (shared deck chrome)

Every deck renders a **fixed 1920×1080 canvas** that is CSS-scaled (and optionally rotated 90° for portrait phones) to fit the viewer's viewport. Since 10 ต.ค. 2569 all of that chrome lives in **one shared component** — do not paste it into a deck again.

```
madebytle/src/app/presentation/_shared/deck-shell.tsx
```

```tsx
import DeckShell, { BASE_W, BASE_H } from "../_shared/deck-shell";

<DeckShell
  slugs={SLIDE_SLUGS}          // readonly string[] — order = rail order, length = slide count
  basePath={BASE_PATH}         // "/presentation/<slug>" — for history.replaceState deep links
  initialSlide={index}         // 0-based, from [slug]/page.tsx (default 0)
  sections={SECTIONS}          // optional: { start: number; label: string }[] → markers on the dot row
  chrome={{                    // optional, all keys optional
    rootBg: "bg-neutral-950",  // bg of the fixed root (default bg-neutral-950; v1/v2 light decks pass "bg-white")
    pillAccent: "bg-red-500 text-white", // landscape toggle while active
    dotActive: "bg-red-500",   // active dot + section tick
  }}
  extraTopLeft={<PdfButton />} // optional node pinned top-left of the viewport (PDF / TOC buttons)
>
  {/* <SlideShell …> … </SlideShell> × N — nothing else */}
</DeckShell>
```

## What DeckShell owns (never re-implement in a deck)

- `fixed inset-0` root → stage (`absolute top-0 left-0 right-0 bottom-24 overflow-auto`) → centering wrapper (`min-w-full min-h-full flex items-start justify-center`) → frame (pure clipper, no shadow/ring/rounded) → canvas (`transformOrigin: "top left"`, `scale()` or `translate + rotate(90deg) + scale()`, `data-landscape`) → slide rail (`snap-x snap-mandatory scroll-smooth`, scrollbars hidden).
- Stage-fit scale: `ResizeObserver` + `resize` + `orientationchange`; presenter zoom **0.5–2** in 0.1 steps multiplied on top of auto-fit (`+` / `=` / `Tab` in, `-` / `_` / `Enter` out, `0` reset — Tab/Enter carry `preventDefault` so clickers work).
- `scrollToSlide(index)` = `clamped * BASE_W` (**never** `clientWidth` — the rail is transform-scaled); scroll → active via rAF; deep link `useLayoutEffect` sets `scrollLeft` before paint + `hasMountedRef` guard; `history.replaceState` URL sync (no Next router).
- Keyboard nav: `← → Space PageUp PageDown Home End`.
- Controls pill: prev · counter · dot row (`hidden sm:flex`, with optional section ticks + `text-[9px]` labels) · next · zoom group (`hidden sm:flex`: − / % / +) · landscape toggle. Pill classes include `w-max whitespace-nowrap max-w-[calc(100vw-1rem)]` (mandatory — without them the bg renders narrower than its content on phones and the last button floats outside). Pill text is literal `text-gray-900` / `text-gray-500` so it reads on any `rootBg`.
- `.deck-digit-rotate` support: the canvas carries `data-landscape`, and `globals.css` already has `[data-landscape="true"] .deck-digit-rotate { transform: rotate(-90deg) }` — nothing to add.

## Locked numbers

| | |
|---|---|
| Canvas | `BASE_W = 1920`, `BASE_H = 1080` — import, never redeclare |
| Controls strip | 96px (`bottom-24`) reserved under the stage; pill at `bottom-4` |
| Safe area | visible content ends at canvas **y ≤ 920** |
| SlideShell padding | `px-20 pt-24 pb-40` (v3: `pt-28`) |
| Content width | 1760px inside padding; `max-w-[1600px]` wrapper (v3: `max-w-[1760px]`); text-heavy slides may drop to `max-w-[1280px]` |
| Zoom | 0.5 – 2, step 0.1 |

Three rules that follow from canvas mode: **no responsive prefixes** (`sm:`/`md:`/`lg:`) inside slides — the only `sm:` is in the pill; **tiny text disappears** (`text-sm` at 0.78× ≈ 11px) — follow [`typography.md`](./typography.md); **width math is fixed** against 1760px.

## What stays per-deck (theme-coupled)

`SlideShell`, `Kicker` (v1/v2) or `CapsLabel` (v3), `SlideNumber`, the `theme` object and all slide templates — copy them from the chosen gallery (`slide-templates-v1/v2/v3.md`). `SlideShell` is a `<section data-slide data-total data-label>` of exactly 1920×1080 with `snap-start shrink-0` and `theme.frameOutline` (the dashed canvas border — always on, also in production).

## Add-ons that hang off the shell

PDF button and TOC menu button → `extraTopLeft`. Section/progress markers → `sections`. TOC drawer + live-message ticker render as siblings of `<DeckShell>` (they are viewport-pinned). See [`addons.md`](./addons.md).

Older decks (`bni-5min`, `korat-points`, …) still carry their own copy of this chrome — leave them frozen. `cinematic-demo` and `hare-and-tortoise` are the reference decks on `DeckShell`.
