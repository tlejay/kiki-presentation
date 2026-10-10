# Slide Templates — v1 (MakeByTle style)

> **This is v1** — the clean, single-background MakeByTle gallery (amber / any of the four classic presets). For the **Kevents-branded** gallery with the 3-tier background system (cover / content / divider), signature motif, glass cards, and workshop/activity + section-divider archetypes, see [`slide-templates-v2.md`](./slide-templates-v2.md). Pick the version in SKILL.md **Step 3a**.

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
const [zoom, setZoom] = useState(1); // presenter canvas zoom, multiplied on top of auto-fit

const zoomIn = useCallback(() => setZoom((z) => Math.min(2, +(z + 0.1).toFixed(2))), []);
const zoomOut = useCallback(() => setZoom((z) => Math.max(0.5, +(z - 0.1).toFixed(2))), []);
const resetZoom = useCallback(() => setZoom(1), []);

useEffect(() => {
  const update = () => {
    const box = stageBoxRef.current?.getBoundingClientRect();
    if (!box) return;
    const wantedW = landscapeMode ? BASE_H : BASE_W;
    const wantedH = landscapeMode ? BASE_W : BASE_H;
    // auto-fit to the visible stage, then apply the presenter's zoom on top
    const scale = Math.min(box.width / wantedW, box.height / wantedH) * zoom;
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
}, [landscapeMode, zoom]); // zoom in deps so the stage re-fits when it changes

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
  {/* Stage scroll area: `overflow-auto` so a zoomed-in canvas can be panned. */}
  <div ref={stageBoxRef} className="absolute top-0 left-0 right-0 bottom-24 overflow-auto">
    {/* Centering wrapper: `min-w/h-full` keeps the frame centered when it fits
        (zoom ≤ fit), and lets it overflow + scroll (pan) when the presenter
        zooms beyond the viewport. Keeps `items-start` so at zoom=1 the slide
        stays top-aligned exactly like before. */}
    <div className="min-w-full min-h-full flex items-start justify-center">
      {/* Frame — pure clipper, NO chrome (no shadow/ring/rounded/border).
          Slide content provides its own bg per-slide. */}
      <div
        className="relative overflow-hidden shrink-0"
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
> - **Presenter zoom** (`zoom` state): a multiplier applied *on top of* the auto-fit so the presenter can enlarge the dashed-frame canvas when it reads too small on a projector/small screen — or shrink it. At `zoom=1` everything behaves exactly as before. When `zoom > 1` the canvas overflows the stage and the `overflow-auto` stage area lets the presenter scroll/pan to the part they want; the centering wrapper keeps it centered when it still fits. Controlled from the pill (− / % / +) and keys (`+` / `-` / `0`-to-reset). The slide-rail nav (`containerRef.scrollTo` in canvas coords) is unaffected by zoom.

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

A single compact pill at viewport `bottom-4`, centered. Combines: prev arrow · counter · dot row (sm+ only) · next arrow · divider · zoom group (− / % / +, sm+ only) · divider · landscape toggle (icon-only). The pill lives **outside** the rotated canvas transform, so its labels stay upright regardless of orientation.

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

  {/* Zoom group — presenter resizes the dashed-frame canvas (hidden on narrow phones).
      `zoomIn`/`zoomOut`/`resetZoom` from the canvas-root block above. */}
  <div className="hidden sm:flex items-center gap-0.5">
    <button type="button" onClick={zoomOut} disabled={zoom <= 0.5}
      aria-label="ย่อขนาด Canvas" title="ย่อ (กด −)"
      className="w-8 h-8 sm:w-9 sm:h-9 rounded-full hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center shrink-0">
      <MagnifyingGlassMinusIcon className="w-4 h-4" aria-hidden="true" />
    </button>
    <button type="button" onClick={resetZoom}
      aria-label="รีเซ็ตขนาด Canvas" title="รีเซ็ตพอดีจอ (กด 0)"
      className={`text-xs font-mono ${theme.muted} tabular-nums shrink-0 w-12 text-center hover:${theme.accent} transition-colors`}>
      {Math.round(zoom * 100)}%
    </button>
    <button type="button" onClick={zoomIn} disabled={zoom >= 2}
      aria-label="ขยายขนาด Canvas" title="ขยาย (กด +)"
      className="w-8 h-8 sm:w-9 sm:h-9 rounded-full hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center shrink-0">
      <MagnifyingGlassPlusIcon className="w-4 h-4" aria-hidden="true" />
    </button>
  </div>

  <span className="hidden sm:block w-px h-5 sm:h-6 bg-gray-200 mx-0.5 sm:mx-1" aria-hidden="true" />

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

> **Zoom group is `hidden sm:flex`** — it's a presentation aid for big screens/projectors, so it collapses on narrow phones to keep the pill within `max-w-[calc(100vw-1rem)]` (same rationale as the dot row). Needs `MagnifyingGlassMinusIcon` + `MagnifyingGlassPlusIcon` from `@heroicons/react/24/outline`.

Why one pill: every pixel of viewport height matters because the canvas scales-to-fit. A single ~52px-tall pill leaves more room for slide content than two stacked rows (~120px tall). On mobile portrait the pill is even shorter (~44px) thanks to the responsive padding shrink. The landscape toggle is icon-only with `aria-label` and `title` for the verbose Thai label on hover.

> **`w-max whitespace-nowrap` is mandatory on the pill** — without them, the pill's bg-white box can render narrower than its content on certain viewports, leaving the rightmost button (landscape toggle) visually floating outside the pill. `max-w-[calc(100vw-1rem)]` caps the pill so it never bleeds past the viewport edge on phones; if your pill content is wider than that cap, hide non-essential elements at narrow breakpoints (e.g. wrap the dot row in `hidden sm:flex`) — never let the pill grow wider than the viewport.

### Section progress markers on the dot row (optional add-on)

For a long deck split into named sections (Day 1 / Day 2, Part 1 / Part 2, Week 6 / Week 8…), the presenter often wants a *glanceable* sense of "how far in am I / how close to the end" without reading the counter. Add markers to the existing dot row — it's deck **chrome** (no slide-content change, so editing it needs **no PDF regen**).

Two cheap, composable touches inside the `{Array.from({length: totalSlides}).map(...)}` dot loop:
1. **Tint a section's dots** — give the later section's inactive dots the accent at low opacity instead of gray, so the final block reads as a distinct cluster.
2. **Insert a labelled tick before a section boundary** — a thin vertical divider + a tiny label (e.g. `W8`, `วันที่ 2`) right before the first dot of that section.

```tsx
{Array.from({ length: totalSlides }).map((_, i) => {
  const isLater = i >= SECTION2_INDEX;            // 0-based index of section-2's first slide
  const dot = (
    <button key={i} type="button" onClick={() => scrollToSlide(i)}
      aria-label={`Go to slide ${i + 1}`} aria-current={active === i ? "true" : undefined}
      className={`h-1.5 rounded-full transition-all ${
        active === i ? `w-5 ${theme.accentBg}`
        : isLater ? "w-1.5 bg-[--accent]/35 hover:bg-[--accent]/60"  // tint section 2
        : "w-1.5 bg-slate-300 hover:bg-slate-400"
      }`}
    />
  );
  if (i === SECTION2_INDEX) {                       // labelled tick before the boundary
    return (
      <span key="sec2-marker" className="flex items-center gap-1" title="Section 2 · home stretch">
        <span className="w-px h-3.5 bg-[--accent]/60" aria-hidden="true" />
        <span className="text-[9px] font-bold tracking-wide text-[--accent] mr-0.5">W8</span>
        {dot}
      </span>
    );
  }
  return dot;
})}
```

> The `text-[9px]` label is allowed here — the dot row is chrome (like the counter), not slide content, so it's exempt from the 5-size typography scale. Use theme tokens for the accent; keep the tick subtle (a notch, not a wall).

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
    // Presenter zoom. Tab/Enter are also wired because presentation clickers
    // commonly send them (alongside ←/→); preventDefault stops Tab from moving
    // focus and Enter from activating a focused control.
    else if (e.key === "+" || e.key === "=" || e.key === "Tab") { e.preventDefault(); zoomIn(); }
    else if (e.key === "-" || e.key === "_" || e.key === "Enter") { e.preventDefault(); zoomOut(); }
    else if (e.key === "0") resetZoom();
  };
  window.addEventListener("keydown", onKey);
  return () => window.removeEventListener("keydown", onKey);
}, [active, scrollToSlide, totalSlides, zoomIn, zoomOut, resetZoom]);
```

> **Presentation-clicker keys.** Many clickers send `←`/`→` for slides plus `Tab`/`Enter` as their two extra buttons. Mapping `Tab → zoom in` and `Enter → zoom out` lets the presenter resize the canvas from the clicker. **`preventDefault` is required** on Tab (else focus jumps between buttons) and Enter (else it re-triggers a focused control). Update the two zoom buttons' `title` to advertise it (e.g. `"ขยาย (กด + หรือ Tab)"`, `"ย่อ (กด − หรือ Enter)"`).

> If the deck also has a TOC overlay (see [`toc.md`](./toc.md)), the keyboard handler additionally guards `if (tocOpen) return;` after the `Escape` check so zoom/nav keys (incl. Tab/Enter) don't fire while the menu is open — letting Tab/Enter navigate the menu normally.

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

## Illustrative mockups (REQUIRED for teaching tool/feature slides)

When a slide teaches "what tool/feature X looks like and does", **show a mockup of its UI** — a clean, on-brand HTML stand-in built from `div`s — instead of describing the screen in words. Learners need to *see* it. This is mandatory for teaching/workshop decks (see SKILL.md → "Teaching / Workshop decks"). Reference implementation: `aviationx-deck.tsx` (`Window`, `MockFrame`, `*Mock` components, `GeminiFeatureSlide`).

Mockups are **illustrative, not real screenshots** — always tag them `ภาพประกอบ` so nobody mistakes them for the real product, and so Tle can swap in a real capture later.

### `MockFrame` — app-window wrapper with "ภาพประกอบ" badge

```tsx
function MockFrame({ children, app = "App" }: { children: React.ReactNode; app?: string }) {
  return (
    <div className="relative h-full min-h-[420px] rounded-2xl border border-slate-200 bg-white shadow-[0_18px_50px_-20px_rgba(0,0,0,0.25)] overflow-hidden flex flex-col">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-100 bg-slate-50 shrink-0">
        <span className="w-3 h-3 rounded-full bg-slate-300" />
        <span className="w-3 h-3 rounded-full bg-slate-300" />
        <span className="w-3 h-3 rounded-full bg-slate-300" />
        <span className={`ml-3 text-sm font-semibold ${theme.accent} flex items-center gap-1.5`}>{app}</span>
        <span className="ml-auto text-[10px] tracking-[0.15em] uppercase font-semibold text-slate-400 border border-slate-200 rounded-full px-2.5 py-0.5">
          ภาพประกอบ
        </span>
      </div>
      <div className="flex-1 p-5 overflow-hidden">{children}</div>
    </div>
  );
}
```

> **Mockup sizing is chrome, not content** — inside a `MockFrame`/`Window`, `text-sm`/`text-[13px]`/`text-[15px]` etc. ARE allowed (you're mimicking real app chrome). This is the one place the 5-size typography rule relaxes. Keep slide *content* (headings, leads, cards) on the normal scale.

Build the inner mock from simple primitives that *suggest* the real UI — chat bubbles, sidebar + channel list, a calendar grid, a kanban with To-do/In-Progress/Done columns, a data table, bar/line chart bars (`<span>` with `height`), skeleton text rows (`<div className="h-2 rounded bg-slate-100 w-..." />`). A few representative rows beat a pixel-perfect clone.

### Phone / device mockup — LOCK width AND height (never let content drive it)

When the mockup is a **device** (phone, tablet, watch) rather than a desktop app window, you MUST give the device frame an **explicit `w-[…px] h-[…px]`** so it keeps a real device aspect ratio. The single most common mistake: setting only the width and letting the inner content (chat bubbles, list rows) determine the height — the frame then renders almost **square**, which reads as broken. A phone that isn't visibly taller-than-wide looks wrong to everyone.

**The rule:**
- **Phone** → lock to roughly **1 : 2.05–2.16** (modern 9:19.5–9:20). Canonical: `w-[300px] h-[620px]`. Other safe sizes: `w-[280px] h-[580px]`, `w-[330px] h-[680px]`.
- **Tablet** → `aspect-[3/4]` (portrait) or `aspect-[4/3]` (landscape) with a locked width.
- The inner screen is `flex flex-col`; the **scrolling content area gets `flex-1 overflow-hidden`** so it fills leftover height instead of stretching the device.
- Mark **every** fixed region (`status bar`, `photographed item`, `input bar`) with `shrink-0`. Only the conversation/list area flexes.
- **Budget check**: a `620px` phone plus a slide heading must fit the **920-canvas-px** content budget (`SlideShell` reserves the rest). If the slide also has a tall heading, drop the heading to `text-5xl` or shrink the phone to `h-[580px]` — don't let the device overflow into the controls-pill safe area. Always run the Step-6 safe-area audit after adding one.

Canonical phone (the locked pattern — copy this shape, swap the inner mock):

```tsx
function PhoneMock({ question, bubbles }: { question: string; bubbles: { who: "ai" | "user"; text: string }[] }) {
  return (
    // LOCKED 300×620 (ratio ~1:2.07). Content NEVER drives the height.
    <div className="relative mx-auto w-[300px] h-[620px] rounded-[2.6rem] bg-slate-900 p-2.5 shadow-2xl">
      <div className="w-full h-full rounded-[2.1rem] bg-white overflow-hidden flex flex-col">
        <div className="flex items-center justify-between px-5 pt-3 pb-1.5 text-xs font-mono text-slate-400 shrink-0">
          <span>9:41</span>
          <span className={`flex items-center gap-1 ${theme.accent} font-semibold`}>App</span>
        </div>
        <div className={`mx-3 mt-1.5 rounded-xl border-2 border-dashed ${theme.accentSoft} px-3.5 py-3 shrink-0`}>
          <p className="text-sm text-slate-700 leading-snug">{question}</p>
        </div>
        {/* conversation — the ONLY part that flexes */}
        <div className="flex-1 px-3 py-3 space-y-2.5 bg-slate-50/60 overflow-hidden">
          {bubbles.map((b, i) => (
            <p key={i} className={`max-w-[200px] rounded-2xl px-3 py-2 text-sm leading-snug ${b.who === "user" ? `ml-auto ${theme.accentBg}` : "bg-white border border-slate-200 text-slate-800"}`}>{b.text}</p>
          ))}
        </div>
        <div className="px-3 pb-4 pt-1 shrink-0">
          <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3.5 py-2">
            <span className="text-sm text-slate-400 flex-1">พิมพ์ข้อความ…</span>
          </div>
        </div>
      </div>
    </div>
  );
}
```

> Same principle for a **paper / worksheet** mockup (e.g. a sheet of problems for the audience to photograph): lock the sheet with a real proportion and a header strip, keep text large enough to read from the back of a room (`text-3xl`+), and lay items on a grid so the sheet doesn't grow lopsided. Reference: `dreamlab-deck.tsx` (`PhoneMock` + the Worksheet slide).

### T13 · `tool-feature` — teach one tool/feature (explanation + mockup)

**When to use**: The core teaching slide. One capability of a tool, with a "what / how" explanation beside an illustrative mockup. Use one per capability.

**Data**: `kicker, name, tag?, what, how: string[], Icon, mock: ReactNode`

```tsx
<SlideShell number={N} total={totalSlides} label={name}>
  <SlideNumber current={N} total={totalSlides} />
  <div className="flex items-center gap-3 mb-3">
    <Kicker spacing="mb-0">{kicker}</Kicker>
    {tag && <span className={`text-[11px] tracking-[0.15em] uppercase font-semibold text-white ${theme.accentBg} rounded-full px-3 py-1`}>{tag}</span>}
  </div>
  <h2 className={`text-5xl font-bold ${theme.text} leading-tight`}>{name}</h2>
  <div className="mt-7 grid grid-cols-12 gap-8 items-stretch">
    <div className="col-span-6 flex flex-col gap-5">
      <div className={`rounded-2xl ${theme.accentSoft} p-7`}>
        <div className="flex items-center gap-3 mb-3">
          <div className={`w-12 h-12 rounded-2xl ${theme.accentBg} flex items-center justify-center`}><Icon className="w-6 h-6" aria-hidden /></div>
          <p className={`text-2xl font-bold ${theme.accent}`}>คืออะไร</p>
        </div>
        <p className={`text-2xl ${theme.subtle} leading-relaxed`}>{what}</p>
      </div>
      <div className={`rounded-2xl border ${theme.border} p-7`}>
        <p className={`text-[11px] tracking-[0.3em] uppercase ${theme.kicker} font-semibold mb-4`}>ทำงานยังไง</p>
        <ul className="space-y-3">
          {how.map((h) => (
            <li key={h} className={`flex gap-3 items-start text-2xl ${theme.subtle}`}>
              <CheckCircleIcon className={`w-7 h-7 ${theme.accent} shrink-0 mt-0.5`} aria-hidden />
              <span className="leading-snug">{h}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
    <div className="col-span-6"><MockFrame app={name}>{mock}</MockFrame></div>
  </div>
</SlideShell>
```

### T14 · `tool-landscape` — survey the category before the chosen tool

**When to use**: Right before you introduce the tool you'll teach. Show the other options in the category and why you picked this one — give learners the whole map before the single pin (Start-With-Why build-up).

**Data**: `kicker, heading, options: { name, note, chosen? }[], whyChosen`

```tsx
<SlideShell number={N} total={totalSlides} label="Landscape">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <h2 className={`text-5xl font-bold ${theme.text} leading-tight`}>{heading}</h2>
  <div className={`mt-10 grid grid-cols-${Math.min(options.length, 4)} gap-5`}>
    {options.map((o) => (
      <div key={o.name} className={`p-7 rounded-2xl border ${o.chosen ? theme.accentSoft + " ring-2 ring-[--accent]" : "border-slate-200 bg-white"} flex flex-col`}>
        <p className={`text-2xl font-bold ${o.chosen ? theme.accent : theme.text}`}>{o.name}</p>
        <p className={`mt-2 text-2xl ${theme.subtle} leading-snug`}>{o.note}</p>
        {o.chosen && <span className={`mt-4 inline-block w-fit text-[11px] tracking-[0.15em] uppercase font-semibold text-white ${theme.accentBg} rounded-full px-3 py-1`}>เราจะใช้ตัวนี้</span>}
      </div>
    ))}
  </div>
  <div className={`mt-8 rounded-2xl ${theme.accentSoft} p-7`}>
    <p className={`text-2xl ${theme.text} leading-relaxed`}><span className="font-bold">ทำไมเลือกตัวนี้:</span> {whyChosen}</p>
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
| Teach one tool/feature (with mockup) | T13 tool-feature |
| Survey tools in a category before teaching one | T14 tool-landscape |
| Picture + short text (default for client decks) | T15 illustrated-split — see [`illustrated-decks.md`](./illustrated-decks.md) |
| Last slide | T12 closing |

## Adding / upgrading a template

1. Add a new `### TXX · <name>` section to **Gallery** with: when-to-use, data shape, JSX skeleton.
2. Add a row to the **Cheat sheet**.
3. If the template needs new icons, note them in the data shape.
4. Future decks pick it up. Existing decks unchanged (they are static React snapshots).
