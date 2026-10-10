# Slide Templates — v3 (The Standard · photo-led)

> **This is v3** — the full-bleed-photograph gallery: every slide sits on a real photo darkened by a scrim, with white type, one accent colour, pinned brand chrome and real media (phones, thumbnails, cut-out people) in the middle layer. For the clean white gallery see [`slide-templates-v1.md`](./slide-templates-v1.md); for the Kevents gradient gallery see [`slide-templates-v2.md`](./slide-templates-v2.md). Pick the version in SKILL.md **Step 3a**; pair v3 with the **The Standard** theme preset in [`themes.md`](./themes.md) (Preset 8).

> **Working reference (read before building):** `madebytle/src/app/presentation/cinematic-demo/cinematic-demo-deck.tsx` — all ten templates below, rendered and audited. Dev URL `/presentation/cinematic-demo`. Adapt it, don't re-derive.

> **Name:** Tle calls this template **"The Standard"** (named 8 ต.ค. 2569 after the proposal it was studied from). When Tle says "ใช้ template The Standard" / "แบบ The Standard" he means this gallery. It is a *style* name only — never put THE STANDARD's name, logos or content in a deck.

> **Where the look comes from:** ten slides of a media-partnership proposal Tle saved on 8 ต.ค. 2569 as "สวยมาก — layout, foreground, background, texts, ภาพประกอบ". v3 keeps the structure of those slides and none of their logos or content.

Source of truth for every v3 slide pattern. **Do not modify when building** — only Tle upgrades this file, and upgrades only affect future decks.

**Use v3 when** the deck sells something people can already *see*: an event, a venue, a content/media package, a sponsorship, a campaign recap, a portfolio. It needs photographs — if the project has none and Tle does not want generated ones, use v1.

**Do not use v3 for** teaching decks, rules/pricing tables, or anything text-dense. A scrimmed photo holds about half the words a white slide does.

---

## Why these slides read as "designed" — the five layers

Every slide is the same five layers, back to front. If a slide looks flat, one layer is missing.

| # | Layer | What it is | Rule |
|---|-------|-----------|------|
| 1 | **Photo** | One real photograph, full bleed, `object-cover` | Never a flat colour or a gradient alone. Blur it (`blur`) when a mid layer sits on top |
| 2 | **Scrim** | A black wash or a directional black gradient | Chosen by *where the text sits* — dark side under the type, photo left visible elsewhere |
| 3 | **Mid layer** | The proof: cut-out person, phone mockup, video thumbnails, sample posts | Real captures, not icons. Allowed to bleed off an edge |
| 4 | **Type** | White, bold; English caps with wide tracking + Thai bold | Two sizes per slide (H1 + Normal). Emphasis by weight, accent colour, or a highlight strip |
| 5 | **Chrome** | Programme badge top-left, partner lockup top-right | Same position on every content slide. This is what makes ten different layouts feel like one deck |

Recurring devices that carry the style (each one is a primitive below):

- **Highlight strip** — the key phrase on a solid accent block, white text. One or two per slide, never a whole paragraph.
- **Caps label** — `BRAND VISIBILITY`, `CONCEPT`: bold, uppercase, tracked. Replaces the tiny v1 kicker.
- **Rule label** — a label followed by a short hairline (`ตัวอย่างคอนเทนต์ ———`). Introduces a row of media.
- **Format line** — play icon · format · hairline · duration. States what the thing *is* in one line.
- **Stat row** — small two-line label over a big number, columns split by vertical hairlines. No cards, no boxes.
- **Check chips** — check-circle + a translucent pill. For inclusions/deliverables.
- **Bleed** — a thumbnail rail running off the right edge, tiles flush to the left edge, a rule that crosses the whole slide. It signals "there is more" and stops the slide looking boxed in.
- **One accent per programme.** Each sub-brand/section owns a colour (coral, amber, magenta, lilac). Yellow/amber is reserved for the one accent sub-line.

---

## Photos — plan them before writing slides

v3 fails without good photographs. Before any JSX, list one background photo per slide plus the mid-layer media.

**Where photos come from, in order:**

1. **The project's own photos** — event shots, the venue, the product, screenshots of real posts. Ask Tle where they are (`AskUserQuestion`) before generating anything.
2. **`/kiki-gpt`** for missing backgrounds — photoreal, `16:9 landscape`, `no text, no logos, no watermark`, and say where the empty area should be (`subject on the right third, left two-thirds dark and uncluttered`). Follow the background-agent procedure in [`illustrated-decks.md`](./illustrated-decks.md) §1.
3. Never hot-link stock photos or use another brand's photography.

**Picking a background:**

- It needs a **quiet zone** where the type will sit. A busy photo edge-to-edge needs `scrim="heavy"` and then stops reading as a photo.
- Decide the scrim from the composition, not the other way round: subject on the right → `scrim="left"` and left-aligned type.
- Minimum 1920px wide. Smaller photos are fine only as blurred backgrounds or thumbnails.
- Photos with **burnt-in text** (a slide on a projector, a banner) fight the type — use them blurred or as thumbnails.

**Files** go in `madebytle/public/presentation/<slug>/`. Use `.jpg` (quality ~82) for photos, `.png` only for cut-outs.

### Cut-out people (the foreground layer)

Two templates (C04, C05) put a person in front of the background. That needs a transparent PNG:

```bash
swift ~/.claude/skills/kiki-presentation/scripts/cutout.swift <photo.jpg> public/presentation/<slug>/<name>.png
```

Apple Vision lifts the main subject and crops to it (macOS 14+, ~3s, no install). It prints `no foreground subject found` on group shots and wide rooms — pick a photo where **one person fills at least a third of the frame**. Always look at the result on a coloured background before using it:

```bash
magick <name>.png -background red -flatten -resize x500 /tmp/check.jpg
```

No usable portrait? Use C07 or C09 instead — do not fake a cut-out with a rectangular photo.

---

## Canvas mode (how decks actually render)

**Identical to v1** — fixed 1920×1080 canvas, CSS-scaled, optional 90° rotation, no responsive prefixes inside slides. Copy these blocks verbatim from [`slide-templates-v1.md`](./slide-templates-v1.md): **Canvas root**, **Scrolling math**, **Controls pill**, **Keyboard nav**, **Landscape digit rotation**, and (optional) **Section progress markers**.

Three v3 differences:

1. **Deck root and layout wrapper are dark**: `fixed inset-0 bg-neutral-950 overflow-hidden` on the root, `bg-neutral-950 min-h-screen` in `layout.tsx`. A white root shows as a white bar under the canvas.
2. **Controls pill stays white** (it sits in the reserved strip, outside the canvas). Add `text-gray-900` to the pill and use literal `text-gray-500` / `bg-red-500` for its counter and active dot — The Standard theme's `muted` is white and would vanish on the pill.
3. **Content padding is `pt-28`** (112) instead of `pt-24`, to clear the brand chrome. Content area: x 80→1840, y 112→920.

---

## Theme + accent + scrim tokens

Paste at the top of the deck. This is Preset 8 in [`themes.md`](./themes.md).

```tsx
// --- Theme: v3 The Standard ---
const theme = {
  name: "The Standard",
  bg: "bg-neutral-950",
  text: "text-white",
  muted: "text-white/60",
  subtle: "text-white/85",
  hairline: "bg-white/50",
  divide: "divide-white/30",
  chip: "bg-white/15",
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-white/20",
  textShadow: "[text-shadow:0_2px_18px_rgba(0,0,0,0.55)]",
} as const;

// One accent per programme / section. Pick ONE per slide.
const ACCENT = {
  coral: {
    text: "text-red-400",
    bg: "bg-red-500 text-white",
    bar: "bg-red-500",
    border: "border-red-500",
    outline:
      "[filter:drop-shadow(5px_0_0_var(--color-red-500))_drop-shadow(-5px_0_0_var(--color-red-500))_drop-shadow(0_5px_0_var(--color-red-500))_drop-shadow(0_-5px_0_var(--color-red-500))]",
  },
  amber: {
    text: "text-amber-400",
    bg: "bg-amber-500 text-neutral-950",
    bar: "bg-amber-500",
    border: "border-amber-500",
    outline:
      "[filter:drop-shadow(5px_0_0_var(--color-amber-500))_drop-shadow(-5px_0_0_var(--color-amber-500))_drop-shadow(0_5px_0_var(--color-amber-500))_drop-shadow(0_-5px_0_var(--color-amber-500))]",
  },
  magenta: {
    text: "text-pink-400",
    bg: "bg-pink-600 text-white",
    bar: "bg-pink-600",
    border: "border-pink-600",
    outline:
      "[filter:drop-shadow(5px_0_0_var(--color-pink-600))_drop-shadow(-5px_0_0_var(--color-pink-600))_drop-shadow(0_5px_0_var(--color-pink-600))_drop-shadow(0_-5px_0_var(--color-pink-600))]",
  },
  lilac: {
    text: "text-fuchsia-300",
    bg: "bg-fuchsia-300 text-neutral-950",
    bar: "bg-fuchsia-300",
    border: "border-fuchsia-300",
    outline:
      "[filter:drop-shadow(5px_0_0_var(--color-fuchsia-300))_drop-shadow(-5px_0_0_var(--color-fuchsia-300))_drop-shadow(0_5px_0_var(--color-fuchsia-300))_drop-shadow(0_-5px_0_var(--color-fuchsia-300))]",
  },
} as const;
type AccentKey = keyof typeof ACCENT;

// Scrim = the dark layer between the photo and the type. Choose by where the text sits.
const SCRIM = {
  even: "bg-black/65",
  heavy: "bg-black/80",
  soft: "bg-gradient-to-t from-black/85 via-black/25 to-black/35",
  left: "bg-gradient-to-r from-black/90 via-black/60 to-black/15",
  right: "bg-gradient-to-l from-black/90 via-black/60 to-black/15",
  bottom: "bg-gradient-to-t from-black/95 via-black/60 to-black/40",
} as const;
type ScrimKey = keyof typeof SCRIM;
```

> **`outline` uses `var(--color-*)`**, not hex — Tailwind v4 exposes every palette colour as a CSS variable, so the no-hex rule holds. Four stacked `drop-shadow`s trace the alpha edge of a transparent PNG; that is the coloured line around the cut-out.

> **Brand colours:** when the client has a palette, replace the classes inside `ACCENT` (keep the four keys' shape) and add hex only there — same rule as Korat City Show.

**Scrim picker**

| Type sits… | Scrim | Typical template |
|-----------|-------|------------------|
| centred, a lot of it | `heavy` | C02, C06, C09, C10 |
| centred, little | `even` | C01 halves |
| left third | `left` | C08 |
| right two-thirds | `right` | C07 |
| a logo over a bright photo | `soft` | C03 |
| bottom third only | `bottom` | captions over a hero photo |

---

## Primitives (always include in every deck)

Icons used by the primitives — `CheckCircleIcon`, `PlayCircleIcon`, `PlayIcon` come from **`@heroicons/react/24/solid`** (they must read as filled shapes on a photo); `CursorArrowRaysIcon` and the controls-pill icons from `/24/outline`.

```tsx
// --- Primitives ---
function PhotoLayer({
  src,
  scrim = "even",
  position = "object-center",
  blur = false,
  priority = false,
}: {
  src: string;
  scrim?: ScrimKey;
  position?: string;
  blur?: boolean;
  priority?: boolean;
}) {
  return (
    <div data-bleed className="absolute inset-0 -z-10 overflow-hidden pointer-events-none select-none">
      <Image
        src={src}
        alt=""
        aria-hidden="true"
        fill
        sizes="1920px"
        priority={priority}
        className={`object-cover ${position} ${blur ? "blur-md scale-110" : ""}`}
      />
      <div className={`absolute inset-0 ${SCRIM[scrim]}`} />
    </div>
  );
}

function SlideShell({
  children,
  number,
  total,
  label,
  photo,
  scrim = "even",
  position,
  blur,
  align = "top",
  bare = false,
}: {
  children: React.ReactNode;
  number: number;
  total: number;
  label?: string;
  photo?: string;
  scrim?: ScrimKey;
  position?: string;
  blur?: boolean;
  align?: "top" | "center";
  // bare — no padding and no max-width wrapper; the slide positions its own layers
  bare?: boolean;
}) {
  const alignClass =
    align === "center" ? "items-center justify-center" : "items-start justify-center";
  return (
    <section
      data-slide={number}
      data-total={total}
      data-label={label}
      style={{ width: `${BASE_W}px`, height: `${BASE_H}px` }}
      className={`snap-start shrink-0 relative isolate overflow-hidden ${theme.bg} ${theme.text} ${theme.frameOutline} ${
        bare ? "" : `flex ${alignClass} px-20 pt-28 pb-40`
      }`}
    >
      {photo && (
        <PhotoLayer src={photo} scrim={scrim} position={position} blur={blur} priority={number <= 2} />
      )}
      {/* wrapper is NOT positioned, so absolute chrome inside it anchors to the slide */}
      {bare ? children : <div className="w-full max-w-[1760px] mx-auto">{children}</div>}
    </section>
  );
}

function SlideNumber({ current, total }: { current: number; total: number }) {
  return (
    <div
      className={`absolute top-6 right-8 z-20 text-xs font-mono ${theme.muted} tabular-nums flex items-center gap-1`}
    >
      <span className="deck-digit-rotate">{String(current).padStart(2, "0")}</span>
      <span>/</span>
      <span className="deck-digit-rotate">{String(total).padStart(2, "0")}</span>
    </div>
  );
}

// Text stand-in for a real logo file. Swap for <Image> when the brand asset exists.
function Wordmark({ top, main, className = "" }: { top?: string; main: string; className?: string }) {
  return (
    <span className={`inline-flex flex-col items-center leading-none ${className}`}>
      {top && <span className="text-[11px] font-bold tracking-[0.3em] uppercase">{top}</span>}
      <span className="text-2xl font-extrabold tracking-[0.08em] uppercase">{main}</span>
    </span>
  );
}

// Pinned brand chrome: programme badge top-left, partner lockup top-right.
function BrandBar({
  badge,
  accent = "coral",
  lockup = "right",
}: {
  badge?: string;
  accent?: AccentKey;
  // "left" — park the partner lockup beside the badge when media occupies the right edge
  lockup?: "left" | "right";
}) {
  return (
    <>
      {badge && (
        <div
          className={`absolute top-8 left-20 z-20 w-16 h-16 rounded-full flex items-center justify-center ${ACCENT[accent].bg}`}
        >
          <span className="text-[11px] font-extrabold tracking-[0.08em] uppercase">{badge}</span>
        </div>
      )}
      <div
        className={`absolute top-12 z-20 flex items-center gap-6 ${
          lockup === "left" ? (badge ? "left-44" : "left-20") : "right-20"
        }`}
      >
        <Wordmark main="Made by Tle" />
        <span className={`w-px h-8 ${theme.hairline}`} aria-hidden="true" />
        <Wordmark top="AI" main="Workshop" />
      </div>
    </>
  );
}

function CapsLabel({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <p className={`text-2xl font-extrabold uppercase tracking-[0.16em] ${className}`}>{children}</p>
  );
}

function RuleLabel({ children, hint }: { children: React.ReactNode; hint?: string }) {
  return (
    <div className="flex items-center gap-5">
      <p className="text-2xl font-bold tracking-[0.08em] shrink-0">{children}</p>
      <span className={`h-px w-28 ${theme.hairline}`} aria-hidden="true" />
      {hint && <p className={`text-2xl ${theme.muted} shrink-0`}>{hint}</p>}
    </div>
  );
}

function Highlight({ children, accent = "coral" }: { children: React.ReactNode; accent?: AccentKey }) {
  return (
    <span className={`inline-block px-5 py-1 text-5xl font-bold leading-snug ${ACCENT[accent].bg}`}>
      {children}
    </span>
  );
}

function FormatLine({ format, length }: { format: string; length: string }) {
  return (
    <p className="flex items-center gap-4 text-2xl font-bold uppercase tracking-[0.14em]">
      <PlayCircleIcon className="w-8 h-8 shrink-0" aria-hidden="true" />
      <span>{format}</span>
      <span className={`w-px h-6 ${theme.hairline}`} aria-hidden="true" />
      <span>{length}</span>
    </p>
  );
}

function StatRow({ stats, className = "" }: { stats: { label: string; value: string }[]; className?: string }) {
  return (
    <div className={`flex divide-x ${theme.divide} ${className}`}>
      {stats.map((s) => (
        <div key={s.label} className="px-10 first:pl-0 last:pr-0 text-center">
          <p className={`text-2xl font-semibold leading-tight ${theme.subtle} whitespace-pre-line`}>{s.label}</p>
          <p className="mt-3 text-5xl font-extrabold tracking-tight tabular-nums">{s.value}</p>
        </div>
      ))}
    </div>
  );
}

function CheckList({ items, cols = 1 }: { items: string[]; cols?: 1 | 2 }) {
  return (
    <ul className={`grid ${cols === 2 ? "grid-cols-2" : "grid-cols-1"} gap-x-6 gap-y-3`}>
      {items.map((it) => (
        <li key={it} className="flex items-center gap-3">
          <CheckCircleIcon className="w-7 h-7 shrink-0 text-white/80" aria-hidden="true" />
          <span className={`rounded-full px-5 py-1 text-2xl font-medium uppercase tracking-wide whitespace-nowrap ${theme.chip}`}>
            {it}
          </span>
        </li>
      ))}
    </ul>
  );
}

function Thumb({
  src,
  alt,
  ratio = "aspect-video",
  play = false,
  caption,
  className = "",
}: {
  src: string;
  alt: string;
  ratio?: string;
  play?: boolean;
  caption?: string;
  className?: string;
}) {
  return (
    <div className={`relative ${ratio} overflow-hidden bg-neutral-900 ${className}`}>
      <Image src={src} alt={alt} fill sizes="640px" className="object-cover" />
      {caption && (
        <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/90 to-transparent px-4 pb-3 pt-10">
          <p className="text-2xl font-bold leading-tight">{caption}</p>
        </div>
      )}
      {play && (
        <span className="absolute inset-0 flex items-center justify-center" aria-hidden="true">
          <span className="w-16 h-16 rounded-full bg-black/55 border border-white/70 flex items-center justify-center">
            <PlayIcon className="w-7 h-7 translate-x-0.5" />
          </span>
        </span>
      )}
    </div>
  );
}

// Device mockup — width AND height are locked; the screen content never drives the size.
function PhoneFrame({
  src,
  alt,
  position = "object-center",
  children,
}: {
  src: string;
  alt: string;
  position?: string;
  children?: React.ReactNode;
}) {
  return (
    <div className="relative w-[250px] h-[520px] shrink-0 rounded-[40px] border-[7px] border-neutral-800 bg-black overflow-hidden shadow-2xl ring-1 ring-white/25">
      <Image src={src} alt={alt} fill sizes="960px" className={`object-cover ${position}`} />
      <span className="absolute top-2 left-1/2 -translate-x-1/2 w-20 h-5 rounded-full bg-black" aria-hidden="true" />
      {children}
    </div>
  );
}

function NumberDot({ n, accent = "magenta" }: { n: number; accent?: AccentKey }) {
  return (
    <span className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl font-extrabold ${ACCENT[accent].bg}`}>
      {n}
    </span>
  );
}

function ChannelTile({ label, className }: { label: string; className: string }) {
  return (
    <span className={`w-[84px] h-[84px] flex items-center justify-center text-[11px] font-extrabold uppercase tracking-[0.12em] ${className}`}>
      {label}
    </span>
  );
}
```

**Notes that are not obvious from the code**

- **`isolate` on the section + `-z-10` on `PhotoLayer`.** The photo sits above the section's background colour and below everything else, and the content wrapper stays *unpositioned*. That matters: `SlideNumber`, `BrandBar` and an inner frame are `absolute` and must anchor to the slide. Give the wrapper `relative` and they all jump inward by the padding (this happened in the first build).
- **`bare`** removes padding and the wrapper so a slide can place its own absolute layers (C01, C04, C05, C07, C08). Everything in a `bare` slide is positioned in canvas pixels.
- **`data-bleed`** marks a decorative layer that may cross the safe area or the slide edge (photo, cut-out, thumbnail rail, hairline, inner frame). **`data-fill`** marks a structural wrapper that is full-height by design. The audit skips both — see "Audit" below. Never put text you need read inside `data-bleed`.
- **`Wordmark` is a stand-in.** Use the client's real logo file via `<Image>` whenever it exists; never redraw a logo. `BrandBar` shows the two-party lockup — edit its contents once per deck.
- **`BrandBar lockup="left"`** when media occupies the top-right corner (C05).
- **`PhoneFrame`** locks width and height (250×520). Never let the screen content size the phone. Its image asks for `sizes="960px"` on purpose: a landscape photo cropped into a tall screen is scaled by *height*, so a 250px request comes back blurry (seen in the first test deck). Feed it a portrait photo when you can, and use `position` (`object-right`, `object-[70%_center]`) to keep the subject in the crop.
- **`Thumb`** takes a `ratio`: `aspect-video` (YouTube), `aspect-[9/16]` (Reels/TikTok), `aspect-[3/4]` (portrait card). `play` adds the play disc; `caption` adds a gradient-backed title.
- **No `Kicker` in v3.** The 11px kicker disappears on a photo. Use `CapsLabel`.

---

## Typography on photos

The 5-size system in [`typography.md`](./typography.md) still holds. v3 mapping:

| Role | Class | Notes |
|------|-------|-------|
| Section / hero title | `text-8xl font-extrabold uppercase tracking-[0.06em] leading-none` | C01, C02, C08, C10 only |
| Slide headline | `text-5xl font-bold leading-tight` (Thai) / `font-extrabold uppercase tracking-[0.04em–0.08em]` (English) | Two lines max |
| Highlight strip | `text-5xl font-bold` inside `Highlight` | Same size as the headline, so it reads as its second half |
| Stat number | `text-5xl font-extrabold tabular-nums` | |
| Body, labels, chips, captions, stat labels | `text-2xl` | Role by weight: `font-extrabold tracking-[0.16em]` caps label · `font-bold` accent line · regular body in `theme.subtle` |
| Chrome only | `text-[11px]` | Wordmark top line, badge text, channel tiles, slide number |

- Add `theme.textShadow` to any headline that crosses a bright part of the photo.
- Add `text-balance` to centred paragraphs — it removes one-word last lines.
- Thai line length: keep body blocks ≤ 900px wide when centred, ≤ 2–3 lines. More than that → cut copy or use v1.

---

## Layout principles (read before composing any slide)

The six v1 principles still apply (top-aligned by default, no disconnected bands, balance columns). v3 adds:

1. **The photo fills the empty space, so let it.** A v3 slide may end at y≈500 (C08) — the lower half is the photograph. Do not add cards to "fill" it.
2. **Text never sits on the brightest or busiest part of the photo.** If it must, darken *that region* with a local gradient layer (`data-bleed`, see C04), not the whole slide.
3. **One mid-layer idea per slide**: a cut-out *or* phones *or* a tile row. Two compete.
4. **Bleed on purpose, or not at all.** A rail that ends 12px inside the edge looks like a mistake; run it clearly past the edge (`w-[1200px]` inside a 1020px column, `-top-24`).
5. **Chrome is fixed.** Badge `top-8 left-20`, lockup `top-12 right-20`, slide number `top-6 right-8`. Content starts at y=112.
6. **Rhythm:** never two text-heavy slides (C05, C06, C09) in a row. Put a breather (C02, C03, C08) between programmes. See "Deck rhythm" below.
7. **Safe area still applies to anything meant to be read:** y ≤ 920.

---

## Gallery

Ids are `C01…C10`. Each maps to one slide in the working reference deck, in the same order.

### C01 · `split-overview` — two worlds, one medallion

**When to use**: The map of the whole proposal on one slide — two tracks/phases/audiences side by side. Usually slide 1 or 2.

**Data**: per half `n, photo, title[2 lines], sub, tiles[≤4], marks[4]` · medallion `eyebrow, line1, line2`

```tsx
<SlideShell number={N} total={totalSlides} label="Overview" bare>
  <SlideNumber current={N} total={totalSlides} />
  <div data-fill className="absolute inset-0 grid grid-cols-2">
    {halves.map((half) => (
      <div key={half.n} data-fill className="relative isolate overflow-hidden">
        <PhotoLayer src={half.photo} scrim="even" priority />
        <div data-fill className="h-full flex flex-col items-center text-center pt-24 px-16">
          <span className="w-14 h-14 rounded-full bg-white text-neutral-950 flex items-center justify-center text-2xl font-extrabold">{half.n}</span>
          <h2 className={`mt-8 text-8xl font-extrabold uppercase leading-[0.95] ${theme.textShadow}`}>
            {half.title[0]}<br />{half.title[1]}
          </h2>
          <CapsLabel className="mt-6 text-yellow-300">{half.sub}</CapsLabel>
          <div className="mt-8 flex gap-3">
            {half.tiles.map((t) => <ChannelTile key={t.label} label={t.label} className={t.className} />)}
          </div>
          <div className="mt-12 grid grid-cols-2 gap-x-16 gap-y-10">
            {half.marks.map((m) => (
              <p key={m} className="text-5xl font-extrabold uppercase tracking-tight whitespace-nowrap">{m}</p>
            ))}
          </div>
        </div>
      </div>
    ))}
  </div>
  {/* medallion sits on the seam and ties the halves together */}
  <div className="absolute left-1/2 top-[530px] -translate-x-1/2 -translate-y-1/2 z-20 w-[300px] h-[300px] rounded-full bg-gradient-to-b from-red-400 to-red-600 ring-[12px] ring-red-500/25 shadow-2xl flex flex-col items-center justify-center text-center">
    <Wordmark main={brand} />
    <p className="mt-4 text-[11px] font-bold uppercase tracking-[0.3em]">{eyebrow}</p>
    <p className="text-5xl font-extrabold uppercase leading-none mt-1">{line1}</p>
    <p className="text-5xl font-extrabold leading-none mt-1">{line2}</p>
  </div>
</SlideShell>
```

> Each half needs its own `isolate` so its `PhotoLayer` stays inside it. Medallion at `top-[530px]`, 300px: it clears the sub-lines (y≈405) and overlaps only the gap between the two columns of marks. Move it and re-check both. `marks` are sub-brand names — real logo files here if they exist.

### C02 · `section-divider` — huge caps over a dimmed photo

**When to use**: Start of a phase (`PRE-EVENT` / `DURING-EVENT` / `POST-EVENT`). `align="center"`, `scrim="heavy"`.

**Data**: `photo, title, tiles[]` (the programmes inside this section)

```tsx
<SlideShell number={N} total={totalSlides} label="Section" photo={photo} scrim="heavy" align="center">
  <SlideNumber current={N} total={totalSlides} />
  <div className="flex flex-col items-center text-center">
    <div className="flex items-center gap-6">{/* partner lockup — Wordmark | hairline | Wordmark */}</div>
    <h2 className={`mt-10 text-8xl font-extrabold uppercase tracking-[0.06em] leading-none ${theme.textShadow}`}>{title}</h2>
    <div className="mt-12 flex gap-5">
      {tiles.map((t) => <ChannelTile key={t.label} label={t.label} className={t.className} />)}
    </div>
  </div>
</SlideShell>
```

> No `BrandBar` here — the lockup moves to the centre above the title. Never two dividers back to back.

### C03 · `logo-hero` — the programme's title card

**When to use**: Opens one programme: just its logo on a bright, on-theme photo. The only slide where the photo is barely darkened.

**Data**: `photo, logo (Image or badge), presentedBy`

```tsx
<SlideShell number={N} total={totalSlides} label="Logo hero" photo={photo} scrim="soft" align="center">
  <SlideNumber current={N} total={totalSlides} />
  <div data-bleed className="absolute inset-10 border border-white/60 pointer-events-none" aria-hidden="true" />
  <div className="flex flex-col items-center text-center">
    {/* real logo: <Image src=… width height className="h-[500px] w-auto" /> */}
    <div className="w-[330px] h-[500px] rounded-full bg-white text-neutral-950 ring-[10px] ring-neutral-950 outline outline-4 outline-white flex flex-col items-center justify-center shadow-2xl">
      {/* badge stand-in */}
    </div>
    <p className={`mt-12 text-2xl uppercase tracking-[0.18em] ${theme.subtle}`}>{presentedBy}</p>
  </div>
</SlideShell>
```

> The hairline inner frame (`inset-10`) is the "title card" cue — keep it. Pick a photo whose subject *is* the programme's theme (maps and a magnifier for a history show).

### C04 · `host-profile` — cut-out host + concept + proof

**When to use**: Introduces a person-led programme: who hosts it, what the episode is, what a sponsor gets, how it performs.

**Data**: `photo (blurred), cutout, hostName, hostRole, visibility[4], stats[3], title[2 lines], accentLine, format, length, concept, thumbs[3]`

```tsx
<SlideShell number={N} total={totalSlides} label="Host profile" photo={photo} scrim="even" blur bare>
  <SlideNumber current={N} total={totalSlides} />
  <BrandBar badge={badge} accent="magenta" />
  {/* mid layer: cut-out anchored to the bottom edge */}
  <div data-bleed className="absolute bottom-0 left-[150px] w-[760px] h-[1000px] pointer-events-none">
    <Image src={cutout} alt={cutoutAlt} fill sizes="760px" className="object-contain object-bottom" />
  </div>
  {/* local fade so the type over the body stays readable */}
  <div data-bleed className="absolute bottom-0 inset-x-0 h-[640px] bg-gradient-to-t from-black via-black/70 to-transparent pointer-events-none" />

  <div className="absolute z-10 left-20 top-[470px] w-[800px]">
    <div className="ml-[520px]">
      <p className="text-2xl font-semibold uppercase tracking-[0.14em]">{hostName}</p>
      <p className={`mt-1 text-2xl ${theme.subtle} leading-snug`}>{hostRole}</p>
    </div>
    <CapsLabel className="mt-4 leading-tight">Brand<br />Visibility</CapsLabel>
    <div className="mt-4"><CheckList cols={2} items={visibility} /></div>
    <StatRow stats={stats} className="mt-10" />
  </div>

  <div className="absolute z-10 left-[900px] right-0 top-28">
    <div className="pr-20">
      <h2 className={`text-5xl font-bold leading-tight ${theme.textShadow}`}>{title[0]}<br />{title[1]}</h2>
      <p className={`mt-4 text-2xl font-bold ${ACCENT.amber.text}`}>{accentLine}</p>
      <div className="mt-6"><FormatLine format={format} length={length} /></div>
      <CapsLabel className="mt-6">Concept</CapsLabel>
      <p className={`mt-3 text-2xl leading-relaxed ${theme.subtle}`}>{concept}</p>
      <div className="mt-8 flex items-center gap-4">
        <CursorArrowRaysIcon className="w-7 h-7" aria-hidden="true" />
        <RuleLabel>PLEASE CLICK TO VIEW</RuleLabel>
      </div>
    </div>
    {/* rail is wider than its column on purpose — the third thumb is cut by the edge */}
    <div data-bleed className="mt-5 flex gap-3 w-[1200px]">
      {thumbs.map((t) => <Thumb key={t.src} src={t.src} alt={t.alt} play className="w-[360px] shrink-0" />)}
    </div>
  </div>
</SlideShell>
```

> The fade layer spans the full width (`inset-x-0`). A fade that stops mid-slide leaves a visible vertical seam. Concept ≤ 2 lines at this width; 3 lines push the rail past y=920 for the rule label.

### C05 · `program-detail` — copy · outlined cut-out · vertical rail

**When to use**: A programme with a strong on-screen personality and several sample clips. Three columns: centred copy, cut-out with an accent outline, a rail of thumbs bleeding top and bottom.

**Data**: `photo (blurred), logo, format, length, title[2], desc, stats[3], cutout, nameTag, visibility[3], thumbs[5]`

```tsx
<SlideShell number={N} total={totalSlides} label="Program detail" photo={photo} scrim="heavy" blur bare>
  <SlideNumber current={N} total={totalSlides} />
  <BrandBar badge={badge} accent="coral" lockup="left" />
  <div data-bleed className="absolute -top-24 right-10 w-[440px] flex flex-col gap-3">
    {thumbs.map((t, i) => (
      <Thumb key={t.src} src={t.src} alt={t.alt} caption={t.caption}
        className={`w-full ${i === 1 ? `border-2 ${ACCENT.coral.border}` : ""}`} />
    ))}
  </div>
  <div data-bleed className="absolute bottom-0 left-[800px] w-[640px] h-[860px] pointer-events-none">
    <Image src={cutout} alt={cutoutAlt} fill sizes="640px"
      className={`object-contain object-bottom ${ACCENT.coral.outline}`} />
  </div>
  <span className={`absolute z-10 left-[1010px] top-[640px] px-5 py-1 text-2xl font-bold ${ACCENT.coral.bg}`}>{nameTag}</span>
  <div className={`absolute z-10 left-[860px] top-[760px] w-[520px] flex items-center gap-8 border-2 ${ACCENT.coral.border} bg-black/80 px-7 py-5`}>
    <CapsLabel className="leading-tight shrink-0">Brand<br />Visibility</CapsLabel>
    <ul className="space-y-1">
      {visibility.map((it) => (
        <li key={it} className="flex items-center gap-3 text-2xl">
          <CheckCircleIcon className="w-6 h-6 text-white/80 shrink-0" aria-hidden="true" />{it}
        </li>
      ))}
    </ul>
  </div>
  <div className="absolute z-10 left-20 top-48 w-[720px] flex flex-col items-center text-center">
    {/* programme logo */}
    <div className="mt-8"><FormatLine format={format} length={length} /></div>
    <CapsLabel className={`mt-6 ${ACCENT.amber.text}`}>Concept</CapsLabel>
    <h2 className="mt-3 text-5xl font-bold leading-tight">{title[0]}<br />{title[1]}</h2>
    <p className={`mt-6 text-2xl leading-relaxed text-balance ${theme.subtle}`}>{desc}</p>
    <StatRow stats={stats} className="mt-12" />
  </div>
</SlideShell>
```

> Five thumbs at 440px wide run from y=-96 to past the bottom — both ends are cut, which is the point. The second one gets the accent border and a `Highlight` caption. The name tag and the boxed checklist are placed in canvas pixels over the cut-out; re-place them for each new portrait.

### C06 · `format-steps` — numbered rail, phones and samples

**When to use**: "What you get": 2–3 deliverable types side by side, each shown as it appears on a phone, with examples.

**Data**: `photo (blurred), title, sub, steps[2–3] = { title, accentLine, desc, phone?, thumbs[] }`

```tsx
<SlideShell number={N} total={totalSlides} label="Format steps" photo={photo} scrim="heavy" blur>
  <SlideNumber current={N} total={totalSlides} />
  <BrandBar badge={badge} accent="magenta" />
  <div className="text-center">
    <h2 className={`text-5xl font-extrabold italic uppercase tracking-[0.04em] ${theme.textShadow}`}>{title}</h2>
    <p className={`mt-4 text-2xl ${theme.subtle}`}>{sub}</p>
  </div>
  {/* rail: hairline edge to edge, a dot at each column start */}
  <div className="relative mt-8 h-12">
    <span data-bleed className={`absolute top-1/2 -left-20 -right-20 h-px ${theme.hairline}`} aria-hidden="true" />
    <div className="relative grid grid-cols-[600px_600px_1fr] gap-10">
      {[1, 2, 3].map((n) => <div key={n} className="pl-6"><NumberDot n={n} /></div>)}
    </div>
  </div>
  <div className="mt-8 grid grid-cols-[600px_600px_1fr] gap-10">
    {phoneSteps.map((s) => (
      <div key={s.title} className="flex gap-6">
        <PhoneFrame src={s.phone} alt={s.phoneAlt} />
        <div className="pt-6 min-w-0">
          <CapsLabel>{s.title}</CapsLabel>
          <p className={`mt-4 text-2xl font-bold ${ACCENT.amber.text}`}>{s.accentLine}</p>
          <p className={`mt-2 text-2xl leading-snug ${theme.subtle}`}>{s.desc}</p>
          <p className="mt-8 text-2xl font-bold">ตัวอย่าง</p>
          <div className="mt-3 grid grid-cols-2 gap-2">
            {s.thumbs.map((t) => <Thumb key={t} src={t} alt="…" ratio="aspect-[3/4]" />)}
          </div>
        </div>
      </div>
    ))}
    <div className="pt-6">{/* third column: no phone — CapsLabel, accent line, desc, RuleLabel, one wide Thumb with play */}</div>
  </div>
</SlideShell>
```

> The same `grid-cols-[600px_600px_1fr]` on the rail and on the columns keeps each dot above its column. Descriptions ≤ 2 lines (≈280px wide beside a phone).

### C07 · `vertical-media` — 9:16 tiles + a centred pitch

**When to use**: Short-form/vertical content. Two portrait tiles flush to the left edge with their numbers underneath; the pitch centred on the right with highlight strips.

**Data**: `photo, tiles[2] = { src, caption }, stats[2], logo, titleEn[2], leadTh, highlights[1–2], paras[2]`

```tsx
<SlideShell number={N} total={totalSlides} label="Vertical media" photo={photo} scrim="right" bare>
  <SlideNumber current={N} total={totalSlides} />
  <BrandBar />
  <div className="absolute z-10 left-0 top-[150px] flex gap-3">
    {tiles.map((t) => (
      <Thumb key={t.src} src={t.src} alt={t.alt} ratio="aspect-[9/16]" caption={t.caption}
        className="w-[330px] border border-white/40" />
    ))}
  </div>
  <StatRow className="absolute z-10 left-[190px] top-[770px]" stats={stats} />
  <div className="absolute z-10 left-[820px] right-20 top-[150px] flex flex-col items-center text-center">
    {/* programme logo */}
    <h2 className={`mt-8 text-5xl font-extrabold uppercase tracking-[0.08em] leading-tight ${theme.textShadow}`}>
      {titleEn[0]}<br />{titleEn[1]}
    </h2>
    <p className="mt-8 text-5xl font-bold">{leadTh}</p>
    <div className="mt-3 flex flex-col items-center gap-2">
      {highlights.map((h) => <Highlight key={h}>{h}</Highlight>)}
    </div>
    {paras.map((p, i) => (
      <p key={i} className={`${i === 0 ? "mt-10" : "mt-6"} text-2xl leading-relaxed text-balance ${theme.subtle} max-w-[900px]`}>{p}</p>
    ))}
  </div>
</SlideShell>
```

> Two 330px tiles are 587px tall: 150 → 737, stats 770 → 890. A third tile does not fit beside the copy. Each highlight line ≤ ~32 Thai characters at `text-5xl` or it wraps inside the strip.

### C08 · `action-title` — title block on a live-action photo

**When to use**: A breather that names the next programme over its best photograph. Almost no words.

**Data**: `photo, logo, title, format, length, platforms[]`

```tsx
<SlideShell number={N} total={totalSlides} label="Action title" photo={photo} scrim="left" bare>
  <SlideNumber current={N} total={totalSlides} />
  <BrandBar />
  <div className="absolute z-10 left-[140px] top-[170px] flex gap-10">
    <span className={`w-2 self-stretch ${ACCENT.lilac.bar}`} aria-hidden="true" />
    <div>
      {/* programme logo */}
      <h2 className={`mt-6 text-8xl font-extrabold uppercase tracking-[0.1em] leading-none ${ACCENT.lilac.text} ${theme.textShadow}`}>{title}</h2>
      <div className="mt-8"><FormatLine format={format} length={length} /></div>
      <div className="mt-8 flex gap-3">
        {platforms.map((p) => (
          <span key={p} className="rounded-full border border-white/70 bg-black/40 px-5 py-1 text-2xl font-semibold">{p}</span>
        ))}
      </div>
    </div>
  </div>
</SlideShell>
```

> The photo is the slide. Choose one with movement and a subject on the right; the lower two-thirds stay empty on purpose. Platform names are text pills — Heroicons has no brand icons and brand logos need the owner's files.

### C09 · `concept-samples` — centred concept, samples + proof below

**When to use**: The detail slide after C08: the idea in a headline and one strip, a short paragraph, then sample episodes on the left and inclusions + numbers on the right.

**Data**: `photo, logo, title[2], highlight, para, samples[4] = { src, cap }, visibility[3], stats[2]`

```tsx
<SlideShell number={N} total={totalSlides} label="Concept" photo={photo} scrim="heavy">
  <SlideNumber current={N} total={totalSlides} />
  <BrandBar badge={badge} accent="lilac" />
  <div className="flex flex-col items-center text-center">
    {/* programme logo with a vertical accent bar */}
    <h2 className={`mt-6 text-5xl font-extrabold leading-tight ${theme.textShadow}`}>{title[0]}<br />{title[1]}</h2>
    <div className="mt-4"><Highlight>{highlight}</Highlight></div>
    <p className={`mt-6 text-2xl leading-relaxed text-balance ${theme.subtle} max-w-[1400px]`}>{para}</p>
  </div>
  <div className="mt-8 grid grid-cols-12 gap-10 items-end">
    <div className="col-span-8 pl-16">
      <RuleLabel hint="คลิกที่รูปเพื่อดูตัวอย่างรายการ">ตัวอย่างรายการ</RuleLabel>
      <div className="mt-4 grid grid-cols-4 gap-3 w-[760px]">
        {samples.map((t) => <Thumb key={t.src} src={t.src} alt={t.alt} ratio="aspect-[3/4]" caption={t.cap} />)}
      </div>
    </div>
    <div className="col-span-4">
      <CapsLabel className="leading-tight">Brand<br />Visibility</CapsLabel>
      <ul className="mt-4 space-y-1">{/* CheckCircleIcon + text-2xl uppercase rows */}</ul>
      <StatRow className="mt-6" stats={stats} />
    </div>
  </div>
</SlideShell>
```

> This is the fullest slide in the set — it ends at y≈907. Paragraph ≤ 2 lines at 1400px; a third line breaks the safe area. `items-end` lines the stat numbers up with the bottom of the sample row.

### C10 · `closing` — thank-you on a dimmed photo

**When to use**: Last slide. Same construction as C02 plus the inner frame and contact pills.

```tsx
<SlideShell number={N} total={totalSlides} label="Closing" photo={photo} scrim="heavy" align="center">
  <SlideNumber current={N} total={totalSlides} />
  <div data-bleed className="absolute inset-10 border border-white/40 pointer-events-none" aria-hidden="true" />
  <div className="flex flex-col items-center text-center">
    <div className="flex items-center gap-6">{/* partner lockup */}</div>
    <h2 className={`mt-10 text-8xl font-extrabold uppercase tracking-[0.06em] leading-none ${theme.textShadow}`}>{title}</h2>
    <p className={`mt-8 text-2xl ${theme.subtle}`}>{line}</p>
    <div className="mt-10 flex gap-4">
      {contacts.map((c) => (
        <span key={c} className="rounded-full border border-white/60 bg-black/40 px-7 py-2 text-2xl font-semibold">{c}</span>
      ))}
    </div>
  </div>
</SlideShell>
```

---

## Deck rhythm

A v3 proposal is a loop repeated per programme, wrapped in an overview and a close:

```
C01 overview
└─ per phase:    C02 section-divider
   └─ per programme:   C03 logo-hero  or  C08 action-title      ← breather, names it
                       C04 / C05 / C07 / C09                     ← one detail slide
                       C06 format-steps (optional: spin-offs / deliverables)
C10 closing
```

Vary the detail template between neighbouring programmes — C04 then C07 then C05 — and give each programme its own accent. Pricing, timeline or terms tables do not belong on a photo: build those slides with a v1 layout on `scrim="heavy"` + a `bg-black/70` panel, or split them into a v1 appendix deck.

---

## Audit

The standard safe-area audit (SKILL.md Step 6) flags full-bleed layers. For v3 add one line at the top of its per-element callback:

```js
if (el.closest('[data-bleed]') || el.hasAttribute('data-fill')) return;
```

Then also look at every slide — the numeric audit cannot see these:

- [ ] Type is readable where it crosses the photo (no white text over a white wall or a projector screen).
- [ ] No hard edge where a local fade layer ends.
- [ ] Bleeding rails are clearly cut by the edge, not ending just inside it.
- [ ] Brand chrome does not sit on top of media in the corners (`lockup="left"` if it does).
- [ ] Cut-out edges are clean; nothing from the old background is left attached.
- [ ] Every photo is ≥ the size it is shown at (no upscaled blur on a sharp layer).

Playwright script for screenshots + the numeric check: see [`illustrated-decks.md`](./illustrated-decks.md) §5.

---

## Cheat sheet — pick a template

| Situation | Template | Scrim | Needs |
|-----------|----------|-------|-------|
| The whole proposal on one slide (two tracks) | C01 split-overview | even ×2 | 2 photos |
| A new phase starts | C02 section-divider | heavy | 1 photo |
| Introduce a programme by its logo | C03 logo-hero | soft | on-theme photo + logo |
| A person-led programme | C04 host-profile | even + blur | **cut-out**, 3 thumbs |
| A programme with many sample clips | C05 program-detail | heavy + blur | **cut-out**, 5 thumbs |
| What the sponsor receives (2–3 formats) | C06 format-steps | heavy + blur | 2 phone screens, thumbs |
| Vertical / short-form content | C07 vertical-media | right | 2 portrait tiles |
| Name the next programme (breather) | C08 action-title | left | 1 strong action photo |
| Concept + samples + numbers | C09 concept-samples | heavy | 4 portrait tiles |
| Last slide | C10 closing | heavy | 1 photo |

## Adding / upgrading a template

1. Build and audit it in `cinematic-demo` first (the reference deck is the test bed).
2. Add a `### CXX · <name>` section to **Gallery**: when-to-use, data shape, JSX skeleton, the pixel budget that makes it fit.
3. Add a row to the **Cheat sheet** (scrim + what media it needs).
4. New tokens go in [`themes.md`](./themes.md) Preset 8, kept additive.
5. Future decks pick it up. Existing decks unchanged (static React snapshots).
