# Slide Templates

Source of truth for every slide pattern. Read this when building a deck. **Do not modify when building** — only Tle upgrades this file, and upgrades only affect future decks.

Each template lists:
- **When to use** — the situation that calls for this layout
- **Required data** — what content the slide consumes
- **JSX skeleton** — drop into the deck and fill in

All examples assume the `theme` token object from [`themes.md`](./themes.md) is in scope. Replace literal `bg-white` / `text-amber-500` etc. with theme tokens (`theme.bg`, `theme.accent`, …) so the deck respects the chosen preset.

**Always read [`typography.md`](./typography.md)** before sizing any text. Every size in this file follows that scale — no `md:` prefixes, no responsive sizing, no free-styling.

---

## Canvas mode (how decks actually render)

Decks render at a **fixed 1920×1080 canvas** that is CSS-scaled (and optionally rotated 90° for portrait phones) to fit the viewer's actual viewport. The `SlideShell` primitive takes care of this — slide content always lays out as if the screen is exactly 1920×1080.

Three rules that follow from this:

1. **No responsive prefixes** in slide content (`md:`, `lg:`, `sm:`). They lie about the available width because the *real* viewport is a smaller scaled box around the canvas. Always use a single absolute size.
2. **Tiny text disappears.** A `text-sm` (14px) at 0.78× viewport scale becomes ~11px on a laptop preview. Read [`typography.md`](./typography.md) for the hard minimum (`text-base` / 16px for prose).
3. **Width math is fixed.** Every slide has `1920 - 2×80 = 1760px` of content area inside the standard padding. Plan grids and max-widths against that.

The deck shell (the `<Bni5MinDeck>`-style root component) is the only place that uses responsive layout — it positions the scaled canvas inside the actual viewport, draws the controls bar, and handles rotation. The slides themselves are always layout-fixed.

### Canvas root (paste once at deck root, replaces the old responsive container)

```tsx
const BASE_W = 1920;
const BASE_H = 1080;

// Inside the deck component:
const stageBoxRef = useRef<HTMLDivElement>(null);
const [landscapeMode, setLandscapeMode] = useState(false);
const [stageScale, setStageScale] = useState(1);
const [stageW, setStageW] = useState(BASE_W);
const [stageH, setStageH] = useState(BASE_H);

useEffect(() => {
  const update = () => {
    const box = stageBoxRef.current?.getBoundingClientRect();
    if (!box) return;
    const wantedW = landscapeMode ? BASE_H : BASE_W;
    const wantedH = landscapeMode ? BASE_W : BASE_H;
    const scale = Math.min(box.width / wantedW, box.height / wantedH);
    setStageScale(scale);
    setStageW(wantedW * scale);
    setStageH(wantedH * scale);
  };
  update();
  const ro = new ResizeObserver(update);
  if (stageBoxRef.current) ro.observe(stageBoxRef.current);
  window.addEventListener("resize", update);
  window.addEventListener("orientationchange", update);
  return () => {
    ro.disconnect();
    window.removeEventListener("resize", update);
    window.removeEventListener("orientationchange", update);
  };
}, [landscapeMode]);

// Markup:
<div className="fixed inset-0 bg-white overflow-hidden">
  {/* Stage = viewport ABOVE the controls strip.
      `bottom-24` reserves a 96px tall zone at the viewport bottom for the
      floating controls pill. The canvas (in any orientation, including the
      rotated landscape mode) never extends behind the pill, so the pill
      never covers slide content.
      Top-aligned (items-start) so when the stage is taller than 16:9
      (mobile portrait, windowed desktop) the empty room sits at the bottom
      of the stage. */}
  <div ref={stageBoxRef} className="absolute top-0 left-0 right-0 bottom-24 flex items-start justify-center">
    {/* Frame — pure clipper, NO chrome (no shadow/ring/rounded/border).
        Slide content provides its own bg per-slide. */}
    <div
      className="relative overflow-hidden"
      style={{ width: stageW, height: stageH }}
    >
      <div
        // `data-landscape` is read by descendants (e.g. SlideNumber digits)
        // that want to counter-rotate so they stay upright in rotated mode.
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
        <div
          ref={containerRef}
          style={{ width: BASE_W, height: BASE_H }}
          className="overflow-x-auto overflow-y-hidden snap-x snap-mandatory scroll-smooth flex [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden"
        >
          {/* slides */}
        </div>
      </div>
    </div>
  </div>

  {/* Controls — floating pill overlay at bottom, always upright */}
  <div className="absolute bottom-4 left-1/2 -translate-x-1/2 ...">
    {/* nav arrows + dots + landscape toggle (see "Controls overlay" below) */}
  </div>
</div>
```

> **Full-bleed canvas with reserved controls strip** (current standard):
> - Stage area is the viewport MINUS a 96px bottom strip (`absolute top-0 left-0 right-0 bottom-24`). The canvas is scaled-to-fit *inside the stage*, so it never extends behind the controls pill — in any orientation, including the rotated landscape mode.
> - Controls live as a **floating pill** at viewport `bottom-4` inside the reserved strip. Never rotated, never inside the canvas transform.
> - Slide is **top-aligned** in the stage (`items-start`). Behavior by viewport aspect:
>   - viewport ≈ 16:9 (desktop full screen) → slide nearly fills the stage, gutter at top/bottom is small
>   - viewport > 16:9 tall (mobile portrait, windowed desktop) → slide sits at the top of the stage, empty white space below, then the controls strip
>   - viewport > 16:9 wide (ultrawide) → slide fits to height with left/right gutters
> - `SlideShell` keeps `pt-24 pb-40` for internal breathing room. Now that canvas can't reach the pill, the pb-40 is a comfort margin, not a safety reservation.
> - **Why a reserved strip** instead of pure overlay: in the rotated landscape mode, the canvas is taller-than-wide (rotated 90°). With a pure overlay the pill always covered the bottom of the rotated canvas; reserving a strip cleanly separates them.
> - The earlier "frame with shadow + gray bg + bottom controls bar" layout made fonts feel small because the canvas was rendered at ~75% of the viewport, then 1920px got scaled inside that smaller box (double shrink). Don't reintroduce frame chrome.

> **NO responsive prefixes inside slides.** The canvas root is non-responsive too now (only `bg-white`, `absolute inset-0`) — the only "responsive" piece is `hidden sm:flex` on the dot row inside the controls pill, where dots collapse on narrow phones.

### Scrolling math

Each slide is `BASE_W` wide. Snap-scroll uses canvas coordinates:

```tsx
const scrollToSlide = useCallback((index: number) => {
  const el = containerRef.current;
  if (!el) return;
  const clamped = Math.max(0, Math.min(totalSlides - 1, index));
  el.scrollTo({ left: clamped * BASE_W, behavior: "smooth" });
}, [totalSlides]);

useEffect(() => {
  const el = containerRef.current;
  if (!el) return;
  let frame = 0;
  const onScroll = () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      setActive(Math.round(el.scrollLeft / BASE_W));
    });
  };
  el.addEventListener("scroll", onScroll, { passive: true });
  return () => { el.removeEventListener("scroll", onScroll); cancelAnimationFrame(frame); };
}, []);
```

### Controls pill (lives in the reserved bottom strip)

A single compact pill at viewport `bottom-4`, centered. Combines: prev arrow · counter · dot row (sm+ only) · next arrow · divider · landscape toggle (icon-only). The pill lives **outside** the rotated canvas transform, so its labels stay upright regardless of orientation.

The pill sits inside the 96px stage-bottom reservation set by the stage area (`bottom-24`), so it never overlaps slide content in any orientation.

**Responsive sizing**: smaller buttons + tighter padding on mobile (where every pixel of the cramped viewport matters), normal sizing on `sm+`:

```tsx
<div className="absolute bottom-4 left-1/2 -translate-x-1/2 w-max max-w-[calc(100vw-1rem)] flex items-center gap-1 sm:gap-2 bg-white/95 backdrop-blur border border-gray-200 rounded-full px-1.5 sm:px-2 py-1.5 sm:py-2 shadow-lg whitespace-nowrap">
  <button type="button" onClick={() => scrollToSlide(active - 1)} disabled={active === 0}
    aria-label="Previous slide"
    className="w-8 h-8 sm:w-9 sm:h-9 rounded-full hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center shrink-0">
    <ArrowLeftIcon className="w-4 h-4" aria-hidden="true" />
  </button>

  <span className={`text-xs font-mono ${theme.muted} tabular-nums shrink-0 px-1`}>
    {String(active + 1).padStart(2, "0")} / {String(totalSlides).padStart(2, "0")}
  </span>

  {/* Dot row hidden on mobile to keep the pill compact */}
  <div className="hidden sm:flex items-center gap-1 px-1">
    {Array.from({ length: totalSlides }).map((_, i) => (
      <button
        key={i}
        type="button"
        onClick={() => scrollToSlide(i)}
        aria-label={`Go to slide ${i + 1}`}
        aria-current={active === i ? "true" : undefined}
        className={`h-1.5 rounded-full transition-all ${
          active === i ? `w-5 ${theme.accentBg}` : "w-1.5 bg-gray-300 hover:bg-gray-400"
        }`}
      />
    ))}
  </div>

  <button type="button" onClick={() => scrollToSlide(active + 1)} disabled={active === totalSlides - 1}
    aria-label="Next slide"
    className="w-8 h-8 sm:w-9 sm:h-9 rounded-full hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center shrink-0">
    <ArrowRightIcon className="w-4 h-4" aria-hidden="true" />
  </button>

  <span className="w-px h-5 sm:h-6 bg-gray-200 mx-0.5 sm:mx-1" aria-hidden="true" />

  <button type="button" onClick={() => setLandscapeMode((v) => !v)}
    aria-pressed={landscapeMode}
    aria-label={landscapeMode ? "กลับแนวตั้ง" : "หมุนเป็นแนวนอน"}
    title={landscapeMode ? "กลับแนวตั้ง" : "หมุนเป็นแนวนอน"}
    className={`w-8 h-8 sm:w-9 sm:h-9 rounded-full flex items-center justify-center shrink-0 transition-colors ${
      landscapeMode ? `${theme.accentBg} text-white` : `${theme.subtle} hover:bg-gray-100`
    }`}>
    <ArrowsPointingOutIcon className={`w-4 h-4 transition-transform ${landscapeMode ? "rotate-45" : ""}`} aria-hidden="true" />
  </button>
</div>
```

Why one pill: every pixel of viewport height matters because the canvas scales-to-fit. A single ~52px-tall pill leaves more room for slide content than two stacked rows (~120px tall). On mobile portrait the pill is even shorter (~44px) thanks to the responsive padding shrink. The landscape toggle is icon-only with `aria-label` and `title` for the verbose Thai label on hover.

> **`w-max whitespace-nowrap` is mandatory on the pill** — without them, the pill's bg-white box can render narrower than its content on certain viewports, leaving the rightmost button (landscape toggle) visually floating outside the pill. `max-w-[calc(100vw-1rem)]` caps the pill so it never bleeds past the viewport edge on phones; if your pill content is wider than that cap, hide non-essential elements at narrow breakpoints (e.g. wrap the dot row in `hidden sm:flex`) — never let the pill grow wider than the viewport.

---

## Primitives (always include in every deck)

### `<SlideShell>` — fixed-canvas slide wrapper with snap

Every slide is a `1920×1080` box. `SlideShell` enforces those dimensions; the controls bar is **outside** the canvas (rendered by the deck root), so the slide does not need to reserve bottom space for it.

```tsx
const BASE_W = 1920;
const BASE_H = 1080;

function SlideShell({
  children, number, total, label, bgImage, bgAlt, align = "top",
}: {
  children: React.ReactNode;
  number: number;
  total: number;
  label?: string;
  bgImage?: string;
  bgAlt?: string;
  // "top" (default) — content starts at the top, empty space (if any) falls at the
  //   bottom where the floating controls live, so it reads as intentional breathing room.
  // "center" — true vertical centering. Use only on hero slides where empty space
  //   above and below is part of the visual statement (Cover, LCD/Statement, Closing).
  align?: "top" | "center";
}) {
  const alignClass =
    align === "center" ? "items-center justify-center" : "items-start justify-center";
  return (
    <section
      data-slide={number}
      data-total={total}
      data-label={label}
      style={{ width: `${BASE_W}px`, height: `${BASE_H}px` }}
      className={`snap-start shrink-0 flex ${alignClass} px-20 pt-24 pb-40 relative overflow-hidden ${theme.bg} ${theme.frameOutline}`}
    >
      {bgImage && (
        <Image
          src={bgImage}
          alt={bgAlt ?? ""}
          fill
          sizes="100vw"
          aria-hidden={!bgAlt}
          className="absolute inset-0 -z-10 object-cover pointer-events-none select-none"
          priority={number <= 2}
        />
      )}
      {/* Content uses near-full canvas width (1920 - 2×80 padding = 1760px) */}
      <div className="w-full max-w-[1600px] mx-auto">{children}</div>
    </section>
  );
}
```

> **Canvas frame outline** — `theme.frameOutline` (e.g. `outline-dashed outline-1 -outline-offset-1 outline-gray-300`) draws a thin dashed border around every slide. **Always on, including production.** Tle's visual cue that "this is a 1920×1080 canvas, not the viewport"; it makes the active slide boundary obvious during live presentation regardless of viewport aspect ratio. Tokenized per-theme so dark themes can use a lighter dash. Do not remove or hide it.

> **Default alignment is `top`** — almost every content slide should keep the default. Empty space then falls *below* the content, where the floating controls live; that reads as deliberate breathing room. Centering content vertically on a sparse slide creates "lost in the middle" empty space at both top and bottom that looks accidental.

> **Use `align="center"` only on the 2–3 hero slides** (Cover, LCD/Statement, Closing). Their visual idea *is* "one big thing surrounded by quiet space."

> **Padding**: `pt-24 pb-40` — `pt-24` (96 canvas-px) keeps headings clear of the slide-number badge in the corner; `pb-40` (160 canvas-px) clears the floating controls pill at typical desktop zoom levels (scale ≥ 0.84). **Critical**: any visible content must end at canvas y ≤ 920. Anything beyond gets covered by the controls overlay.

> **Width budget**: `max-w-[1600px]` keeps long lines from sprawling edge-to-edge while still using most of the 1760px content area. For text-heavy slides you can drop to `max-w-[1280px]` for better line lengths.

### `<Kicker>` — small uppercase label above headings

```tsx
function Kicker({
  children, spacing = "mb-4",
}: {
  children: React.ReactNode;
  spacing?: string; // override mb-* when heading is huge — e.g. "mb-10"
}) {
  return (
    <p className={`text-[11px] tracking-[0.3em] uppercase ${theme.kicker} font-semibold ${spacing}`}>
      {children}
    </p>
  );
}
```

> **Spacing rule for Thai**: when the next heading is `text-7xl` or larger, pass `spacing="mb-10"` and add `pt-2 leading-[1.05]` to the heading. Thai diacritics (ไม้เอก/ตรี) overflow the cap-height and overlap the kicker otherwise.

### `<SlideNumber>` — top-right counter

```tsx
function SlideNumber({ current, total }: { current: number; total: number }) {
  // `.deck-digit-rotate` counter-rotates -90° when an ancestor has
  // `data-landscape="true"` (rule lives in globals.css; see "Landscape digit
  // rotation" below). Digits stay upright in rotated mode; the slash is
  // intentionally NOT counter-rotated so the separator visually aligns with
  // the rest of the rotated canvas.
  return (
    <div className={`absolute top-6 right-8 text-xs font-mono ${theme.muted} tabular-nums flex items-center gap-1`}>
      <span className="deck-digit-rotate">{String(current).padStart(2, "0")}</span>
      <span>/</span>
      <span className="deck-digit-rotate">{String(total).padStart(2, "0")}</span>
    </div>
  );
}
```

### Landscape digit rotation (add to `globals.css`)

The slide-number digits need to read upright in rotated landscape mode (where the canvas is `rotate(90deg)`). Tailwind's arbitrary variants don't reliably emit a CSS rule for ancestor-based attribute selectors with quoted values, so define the rule explicitly in `globals.css`:

```css
/* Presentation deck — counter-rotate digits inside the slide-number badge
   so they read upright when the canvas is in rotated landscape mode.
   The slash is intentionally NOT counter-rotated. */
[data-landscape="true"] .deck-digit-rotate {
  display: inline-block;
  transform: rotate(-90deg);
  transition: transform 0.2s ease;
}
```

The deck root sets `data-landscape={landscapeMode ? "true" : "false"}` on the canvas wrapper (the div with the rotate transform), so the rule cascades into every slide's `SlideNumber`.

### Keyboard nav (paste once in the deck)

```tsx
useEffect(() => {
  const onKey = (e: KeyboardEvent) => {
    if (e.key === "ArrowRight" || e.key === " " || e.key === "PageDown") { e.preventDefault(); scrollToSlide(active + 1); }
    else if (e.key === "ArrowLeft" || e.key === "PageUp") { e.preventDefault(); scrollToSlide(active - 1); }
    else if (e.key === "Home") scrollToSlide(0);
    else if (e.key === "End") scrollToSlide(totalSlides - 1);
  };
  window.addEventListener("keydown", onKey);
  return () => window.removeEventListener("keydown", onKey);
}, [active, scrollToSlide, totalSlides]);
```

---

## Layout principles (read before composing any slide)

Tle's standing rule: **"empty space is fine — but never make the viewer wonder why it's there."**

### 1. Default to top-aligned content

Use `<SlideShell ... align="top">` (the default) on every content slide. The reason: when content is shorter than the canvas, top-alignment puts the empty space at the bottom, where the floating controls pill lives. That makes the empty space *read* as deliberate breathing room around the controls, not as "your content got lost in the middle."

Centering content vertically (`align="center"`) on a sparse slide produces empty bands above *and* below the content — the worst look, because nothing on the slide explains either band.

Reserve `align="center"` for **hero slides only**: Cover, LCD/Statement, Closing. There, empty space *is* the design.

### 2. Don't split a slide into disconnected bands

The classic mistake (e.g., earlier About slide): heading at top, then a metadata row at the bottom, with a wide empty stripe between them. Two "bands" of content with a visible no-man's-land gap in the middle reads as broken.

Fix: collapse to a single coherent block. Either
- **Merge into a 2-column unit** where the two halves share a common top edge (e.g., heading + metadata cards stacked on the left, supporting visual on the right at the same height), or
- **Flow content as a single column** (header → lead → cards) so the viewer reads top-to-bottom without crossing a void.

### 3. Make cards tall when the slide is sparse

For grids with 2–4 cards (stats, features, looking-for, misconceptions), if the cards naturally come out short, give them more vertical room: bigger padding (`p-10`/`p-12` vs `p-6`), internal gaps (`flex flex-col gap-8`), and a divider line between sections inside the card. A 200px-tall stat card on a 1080-canvas slide looks lonely; a 380–500px-tall card with the same content reads as substantial.

Same principle for trigger/script row lists: bump row padding (`p-10`) and the spacing between rows (`space-y-6`) when there are only 3 rows.

### 4. Balance the two columns of a 2-col layout

In service-detail or "two-column" slides, if the right column has 3 stacked cards (~600px tall) and the left column has only icon+heading+lead (~250px tall), the left feels truncated. Add supporting content to the shorter column — a checklist of deliverables, a small mockup, a stat callout — until both columns finish at roughly the same height.

### 5. Use `aspect-[X/Y]` for hero images, not fixed pixel heights

`aspect-[4/3]` on a hero image inside a column grows naturally with the column width and fills the canvas. A `h-[260px]` photo collage on a sparse slide leaves dead space; `h-[480px]` or aspect-based works better.

### 6. Vertical-fill audit

After composing a slide, eyeball it: does the content occupy ≥ ~75% of the canvas height (~750px of the 888px content area)? If not, ask yourself whether the empty band is *explained* — either by being at the bottom (top-aligned, controls live there) or by being a deliberate hero treatment. If neither, fix by bumping padding/sizes/content per principles 3–5 above.

---

## Gallery

### T01 · `cover` — title + tagline + visual

**When to use**: Slide 1 of every deck. Brand + audience hook + presenter identity.

**Data**: `kicker, brandName, accentName, tagline, presenterName, presenterRole, visual`

```tsx
<SlideShell number={1} total={totalSlides} label="Cover" align="center">
  <SlideNumber current={1} total={totalSlides} />
  <div className="grid grid-cols-2 gap-12 items-center">
    <div>
      <Kicker spacing="mb-8">{kicker}</Kicker>
      <h1 className={`text-8xl font-bold tracking-tight ${theme.text} leading-[1.05] pt-2`}>
        {brandName} <span className={theme.accent}>{accentName}</span>
      </h1>
      <p className={`mt-6 text-3xl ${theme.subtle} font-medium leading-relaxed`}>
        {tagline}
      </p>
      <div className="mt-12 space-y-2">
        <p className={`text-2xl ${theme.text} font-semibold`}>{presenterName}</p>
        <p className={`text-lg ${theme.muted}`}>{presenterRole}</p>
      </div>
    </div>
    <div className="flex justify-center">
      {/* visual: photo OR icon-in-card OR product render */}
      <div className={`aspect-square w-full max-w-sm rounded-3xl ${theme.accentSoft} flex items-center justify-center`}>
        {/* Heroicon placeholder until real photo provided */}
      </div>
    </div>
  </div>
</SlideShell>
```

### T02 · `statement` — single huge statement (LCD)

**When to use**: The one line you want the audience to remember (BNI's "LCD" slide; pitch deck's tagline; talk's one-liner).

**Data**: `kicker, mainText, accentText, supportingText`

```tsx
<SlideShell number={N} total={totalSlides} label="Statement" align="center">
  <SlideNumber current={N} total={totalSlides} />
  <div className="text-center">
    <Kicker spacing="mb-10">{kicker}</Kicker>
    <h2 className={`text-8xl font-bold ${theme.text} leading-[1.05] pt-2`}>
      {mainText} <span className={theme.accent}>{accentText}</span>
    </h2>
    <div className="mt-10 inline-block">
      <p className={`text-5xl font-semibold ${theme.subtle}`}>{supportingText}</p>
    </div>
  </div>
</SlideShell>
```

### T03 · `stat-grid` — 3-4 numbers with labels

**When to use**: Why-choose-us, traction, scale ("100+ projects", "30+ team", "2023 award").

**Data**: `kicker, heading, items: { stat, label }[]` (use `Intl.NumberFormat('en-US')` for ≥1,000)

```tsx
<SlideShell number={N} total={totalSlides} label="Stats">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <h2 className={`text-6xl font-bold ${theme.text} leading-tight`}>{heading}</h2>
  <div className={`mt-16 grid grid-cols-${items.length} gap-6`}>
    {items.map((item) => (
      <div key={item.label} className={`p-6 rounded-2xl border ${theme.card} transition-colors`}>
        <p className={`text-5xl font-bold ${theme.accent} tabular-nums`}>{item.stat}</p>
        <p className={`mt-3 ${theme.subtle} leading-snug`}>{item.label}</p>
      </div>
    ))}
  </div>
</SlideShell>
```

### T04 · `feature-grid` — 2-4 features with icon + title + desc

**When to use**: Services overview, what-we-built, capabilities. The default for "show me 3 things side by side."

**Data**: `kicker, heading, items: { icon, title, desc }[]` (icon = Heroicon component)

```tsx
<SlideShell number={N} total={totalSlides} label="Features">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <h2 className={`text-6xl font-bold ${theme.text} leading-tight`}>{heading}</h2>
  <div className={`mt-16 grid grid-cols-${items.length} gap-8`}>
    {items.map((item) => (
      <div key={item.title} className={`p-8 rounded-3xl ${theme.accentSoft} flex flex-col`}>
        <div className={`w-14 h-14 rounded-2xl ${theme.accentBg} flex items-center justify-center`}>
          <item.icon className="w-7 h-7" aria-hidden="true" />
        </div>
        <h3 className={`mt-6 text-2xl font-bold ${theme.text}`}>{item.title}</h3>
        <p className={`mt-3 ${theme.subtle} leading-relaxed text-xl`}>{item.desc}</p>
      </div>
    ))}
  </div>
</SlideShell>
```

### T05 · `two-column` — heading + lead on left, list on right

**When to use**: Service detail, deep dive on a single thing with supporting bullets/examples.

**Data**: `kicker, icon, title, lead, items: { name, desc }[]`

```tsx
<SlideShell number={N} total={totalSlides} label={title}>
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <div className="grid grid-cols-2 gap-12 items-start">
    <div>
      <div className={`w-16 h-16 rounded-2xl ${theme.accentBg} flex items-center justify-center mb-6`}>
        <Icon className="w-8 h-8" aria-hidden="true" />
      </div>
      <h2 className={`text-6xl font-bold ${theme.text} leading-tight`}>{title}</h2>
      <p className={`mt-6 text-xl ${theme.subtle} leading-relaxed`}>{lead}</p>
    </div>
    <div className="space-y-4">
      <h3 className={`text-sm uppercase tracking-wider ${theme.muted} font-semibold`}>Examples</h3>
      {items.map((p) => (
        <div key={p.name} className={`p-5 rounded-xl border ${theme.border} ${theme.bg}`}>
          <p className={`font-semibold ${theme.text}`}>{p.name}</p>
          <p className={`text-sm ${theme.subtle} mt-1`}>{p.desc}</p>
        </div>
      ))}
    </div>
  </div>
</SlideShell>
```

### T06 · `logo-grid` — customer logos (text or image)

**When to use**: Social proof. Notable clients, partners, integrations.

**Data**: `kicker, heading, logos: string[] | { name, src }[]`, `footer?`

```tsx
<SlideShell number={N} total={totalSlides} label="Customers">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <h2 className={`text-6xl font-bold ${theme.text} leading-tight`}>{heading}</h2>
  <div className={`mt-16 grid grid-cols-${cols} gap-4`}>
    {logos.map((name) => (
      <div key={name} className={`aspect-[3/2] rounded-2xl border ${theme.card} flex items-center justify-center transition-colors`}>
        <p className={`text-2xl font-bold ${theme.subtle}`}>{name}</p>
      </div>
    ))}
  </div>
  {footer && <p className={`mt-8 text-sm ${theme.muted} text-center`}>{footer}</p>}
</SlideShell>
```

### T07 · `case-study` — featured case (visual + narrative)

**When to use**: Hero project. Award winner. Case study with 1 strong example beats a wall of logos.

**Data**: `kicker, projectName, projectClient, headline, subheadline, lead, bullets: string[], visualIcon`

```tsx
<SlideShell number={N} total={totalSlides} label="Case Study">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <div className="grid grid-cols-5 gap-12 items-center">
    <div className="col-span-2">
      <div className={`aspect-square rounded-3xl ${theme.accentSoft} flex flex-col items-center justify-center p-8`}>
        <VisualIcon className={`w-20 h-20 ${theme.accent}`} aria-hidden="true" />
        <p className={`mt-4 text-2xl font-bold ${theme.text} text-center`}>{projectName}</p>
        <p className={`text-sm ${theme.subtle} text-center mt-1`}>{projectClient}</p>
      </div>
    </div>
    <div className="col-span-3">
      <h2 className={`text-5xl font-bold ${theme.text} leading-tight`}>{headline}</h2>
      <p className={`mt-3 text-2xl ${theme.accent} font-semibold`}>{subheadline}</p>
      <p className={`mt-6 text-lg ${theme.subtle} leading-relaxed`}>{lead}</p>
      <ul className="mt-6 space-y-2">
        {bullets.map((item) => (
          <li key={item} className={`flex gap-3 ${theme.subtle}`}>
            <CheckBadgeIcon className={`w-5 h-5 ${theme.accent} shrink-0 mt-0.5`} aria-hidden="true" />
            {item}
          </li>
        ))}
      </ul>
    </div>
  </div>
</SlideShell>
```

### T08 · `callout-list` — iconed personas/segments

**When to use**: "Looking for", target audience, ICP segments. 2-4 items with icon + title + 1-line desc.

**Data**: `kicker, heading, items: { icon, title, desc }[]`

```tsx
<SlideShell number={N} total={totalSlides} label="Looking For">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <h2 className={`text-6xl font-bold ${theme.text} leading-tight`}>{heading}</h2>
  <div className="mt-12 grid grid-cols-2 gap-6">
    {items.map((p) => (
      <div key={p.title} className={`p-6 rounded-2xl border-2 ${theme.accentSoft} flex gap-5`}>
        <div className={`w-14 h-14 shrink-0 rounded-xl ${theme.accentBg} flex items-center justify-center`}>
          <p.icon className="w-7 h-7" aria-hidden="true" />
        </div>
        <div>
          <h3 className={`text-xl font-bold ${theme.text}`}>{p.title}</h3>
          <p className={`${theme.subtle} mt-2 leading-relaxed`}>{p.desc}</p>
        </div>
      </div>
    ))}
  </div>
</SlideShell>
```

### T09 · `trigger-list` — keyword → outcome

**When to use**: BNI "trigger words" slide; or "common scenarios where you'd think of us".

**Data**: `kicker, heading, items: { keyword, context }[], outcomeLabel`

```tsx
<SlideShell number={N} total={totalSlides} label="Triggers">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <h2 className={`text-6xl font-bold ${theme.text} leading-tight`}>
    {heading} → <span className={theme.accent}>{outcomeLabel}</span>
  </h2>
  <div className="mt-12 space-y-4">
    {items.map((t, i) => (
      <div key={t.keyword} className={`flex items-center gap-6 p-6 rounded-2xl ${theme.bg} border ${theme.border}`}>
        <div className={`w-14 h-14 shrink-0 rounded-full ${theme.accentBg} flex items-center justify-center font-bold text-xl tabular-nums`}>
          {i + 1}
        </div>
        <div className="flex-1">
          <p className={`text-3xl font-bold ${theme.text}`}>&ldquo;{t.keyword}&rdquo;</p>
          <p className={`${theme.subtle} mt-1`}>{t.context}</p>
        </div>
        <ArrowRightIcon className={`w-8 h-8 ${theme.accent} shrink-0`} aria-hidden="true" />
        <p className={`font-bold ${theme.accent} text-lg shrink-0`}>{outcomeLabel}</p>
      </div>
    ))}
  </div>
</SlideShell>
```

### T10 · `script-box` — labeled script lines (ถาม/เชีย/นัด)

**When to use**: Hand the audience a literal script to repeat. BNI Ask/Hand-off pattern; sales playbook example dialogue.

**Data**: `kicker, heading, lines: { tag, text }[]`

```tsx
<SlideShell number={N} total={totalSlides} label="Script">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <h2 className={`text-6xl font-bold ${theme.text} leading-tight`}>{heading}</h2>
  <div className="mt-12 space-y-5">
    {lines.map((item) => (
      <div key={item.tag} className={`flex gap-5 p-6 rounded-2xl border ${theme.accentSoft}`}>
        <span className={`shrink-0 w-20 text-center font-bold ${theme.accent} text-lg pt-1`}>{item.tag} :</span>
        <p className={`text-lg text-xl ${theme.text} leading-relaxed`}>{item.text}</p>
      </div>
    ))}
  </div>
</SlideShell>
```

### T11 · `comparison` — wrong vs right (misconceptions)

**When to use**: Address objections, dispel misconceptions, before/after, then/now.

**Data**: `kicker, heading, pairs: { wrong, right }[]`

```tsx
<SlideShell number={N} total={totalSlides} label="Comparison">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <h2 className={`text-6xl font-bold ${theme.text} leading-tight`}>{heading}</h2>
  <div className="mt-12 grid grid-cols-2 gap-8">
    {pairs.map((m) => (
      <div key={m.wrong} className={`p-8 rounded-2xl border ${theme.border} ${theme.bg}`}>
        <div className="flex items-start gap-3">
          <XMarkIcon className="w-7 h-7 text-red-500 shrink-0 mt-0.5" aria-hidden="true" />
          <p className={`text-xl font-bold ${theme.muted} line-through`}>{m.wrong}</p>
        </div>
        <div className="mt-5 flex items-start gap-3">
          <CheckBadgeIcon className={`w-7 h-7 ${theme.accent} shrink-0 mt-0.5`} aria-hidden="true" />
          <p className={`text-lg ${theme.text} leading-relaxed`}>{m.right}</p>
        </div>
      </div>
    ))}
  </div>
</SlideShell>
```

### T12 · `closing` — big name + contact cards

**When to use**: Final slide. Make it easy to reach you.

**Data**: `kicker, brandName, accentName, presenter, contacts: { icon, label, value, href }[], farewell?`

```tsx
<SlideShell number={N} total={totalSlides} label="Closing" align="center">
  <SlideNumber current={N} total={totalSlides} />
  <div className="text-center">
    <Kicker spacing="mb-10">{kicker}</Kicker>
    <h2 className={`text-9xl font-bold ${theme.text} leading-[1.05] pt-2`}>
      {brandName} <span className={theme.accent}>{accentName}</span>
    </h2>
    <p className={`mt-4 text-xl ${theme.subtle}`}>{presenter}</p>

    <div className={`mt-14 max-w-3xl mx-auto grid grid-cols-${contacts.length} gap-4`}>
      {contacts.map((c) => (
        <a key={c.label} href={c.href}
          className={`group p-6 rounded-2xl border ${theme.card} transition-colors flex flex-col items-center gap-3`}>
          <c.icon className={`w-8 h-8 ${theme.accent}`} aria-hidden="true" />
          <p className={`text-xs uppercase tracking-wider ${theme.muted} font-semibold`}>{c.label}</p>
          <p className={`text-[13px] ${theme.text} font-medium ${c.label === "Phone" ? "tabular-nums text-lg" : ""}`}>{c.value}</p>
        </a>
      ))}
    </div>

    {farewell && <p className={`mt-12 text-2xl ${theme.subtle} font-medium`}>{farewell}</p>}
  </div>
</SlideShell>
```

---

## Cheat sheet — pick a template

| Situation | Template |
|-----------|----------|
| First slide | T01 cover |
| The one line they must remember | T02 statement |
| 3-4 numbers showing scale | T03 stat-grid |
| 3 services/features side-by-side | T04 feature-grid |
| One service + supporting examples | T05 two-column |
| Logos for credibility | T06 logo-grid |
| One hero project in detail | T07 case-study |
| Target personas (Looking-for / ICP) | T08 callout-list |
| Trigger words → action | T09 trigger-list |
| Literal script for someone to repeat | T10 script-box |
| Misconceptions / before-after | T11 comparison |
| Last slide | T12 closing |

## Adding / upgrading a template

1. Add a new `### TXX · <name>` section to **Gallery** with: when-to-use, data shape, JSX skeleton.
2. Add a row to the **Cheat sheet**.
3. If the template needs new icons, note them in the data shape.
4. Future decks pick it up. Existing decks unchanged (they are static React snapshots).
