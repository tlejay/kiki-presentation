# Slide Templates — v2 (Kevents brand)

> **This is v2** — the Kevents-branded gallery: indigo→purple→pink signature gradient, glass cards, a **3-tier background system** (cover / content / divider), a bleed-off-edge **signature motif**, and workshop/activity + section-divider archetypes. For the clean single-background MakeByTle gallery, see [`slide-templates-v1.md`](./slide-templates-v1.md). Pick the version in SKILL.md **Step 2**; pair v2 with the **Kevents** theme preset in [`themes.md`](./themes.md).

Source of truth for every v2 slide pattern. Read this when building a v2 deck. **Do not modify when building** — only Tle upgrades this file, and upgrades only affect future decks.

Each template lists:
- **When to use** — the situation that calls for this layout
- **Required data** — what content the slide consumes
- **JSX skeleton** — drop into the deck and fill in

All examples assume the **Kevents** `theme` token object from [`themes.md`](./themes.md) (Preset 5) is in scope — it carries the v1 shape **plus** the v2-only tokens (`variants`, `gradientText`, `glassCard`, `glow`, `pill`, `chip`, `numberBadge`, `underlineAccent`, `tint*`, `semantic*`). Replace literal colors with theme tokens so the deck stays consistent.

**Always read [`typography.md`](./typography.md)** before sizing any text. Every size in this file follows that 5-size scale — no `md:` prefixes, no responsive sizing, no free-styling.

**What's different from v1 (the whole point of v2):**
1. `SlideShell` gains a `variant` prop (`content` / `cover` / `divider`) + an optional `motif` — per-slide backgrounds instead of one `theme.bg` for the whole deck.
2. A `<SignatureMotif>` primitive (mesh-arcs / mark-ghost / dot-grid) bleeds off the slide edge behind content.
3. New primitives: `<CalloutBar>`, `<PillBadge>`, `<NumberBadge>`, plus gradient-title + underline-accent conventions.
4. Gallery K12–K24 adds section-divider, question, agenda, compare, process-flow, numbered-cards, 2×2 grid, quadrant matrix, chat bubbles, **activity/workshop**, criteria-columns, photo-strip, checklist-recap.

Deck chrome (stage, scrolling, controls pill, keyboard nav, landscape rotation) comes from the shared `DeckShell` — see [`canvas-shell.md`](./canvas-shell.md). `SlideNumber`, `Kicker` and MockFrame/phone are identical to v1 and reproduced below so v2 is self-contained.

---

## Canvas mode

Decks render at a **fixed 1920×1080 canvas** that `DeckShell` scales (and optionally rotates 90°) to the viewport. Stage, zoom, scroll math, deep links, keyboard nav, controls pill, section markers and the `.deck-digit-rotate` CSS all live in `madebytle/src/app/presentation/_shared/deck-shell.tsx` — **import it, never paste chrome into a deck**. Props, locked numbers and the three canvas rules (no responsive prefixes, no tiny text, 1760px width math) are in [`canvas-shell.md`](./canvas-shell.md).

---

## Primitives (always include in every deck)

### `<SlideShell>` — fixed-canvas slide wrapper with per-slide background variants

The one structural change vs v1: a `variant` prop swaps background + text + frame from `theme.variants[variant]`, with v1-safe fallbacks to `theme.bg` / `theme.text` / `theme.frameOutline`. An optional `motif` renders a `<SignatureMotif>` behind content.

```tsx
const BASE_W = 1920;
const BASE_H = 1080;

type SlideVariant = "content" | "cover" | "divider";

function SlideShell({
  children, number, total, label,
  variant = "content",
  motif,                    // optional: <SignatureMotif variant="mesh-arcs" tone="onLight" />
  bgImage, bgAlt, align = "top",
}: {
  children: React.ReactNode;
  number: number;
  total: number;
  label?: string;
  variant?: SlideVariant;
  motif?: React.ReactNode;
  bgImage?: string;
  bgAlt?: string;
  align?: "top" | "center";
}) {
  const alignClass =
    align === "center" ? "items-center justify-center" : "items-start justify-center";

  // Per-variant bg/text/frame from theme tokens, with v1-safe fallbacks.
  // A theme without `variants` (the four classic presets) still renders — it
  // just falls back to a single bg/text, so cover/divider look like content.
  const v = theme.variants?.[variant];
  const bgClass   = v?.bg   ?? theme.bg;
  const textClass = v?.text ?? theme.text;
  const frame     = v?.frameOutline ?? theme.frameOutline;

  return (
    <section
      data-slide={number}
      data-total={total}
      data-label={label}
      data-variant={variant}
      style={{ width: `${BASE_W}px`, height: `${BASE_H}px` }}
      className={`snap-start shrink-0 flex ${alignClass} px-20 pt-24 pb-40 relative overflow-hidden ${bgClass} ${textClass} ${frame}`}
    >
      {/* 1. optional photographic bg (v1 behavior) — deepest layer */}
      {bgImage && (
        <Image
          src={bgImage} alt={bgAlt ?? ""} fill sizes="100vw"
          aria-hidden={!bgAlt} priority={number <= 2}
          className="absolute inset-0 -z-20 object-cover pointer-events-none select-none"
        />
      )}

      {/* 2. signature motif — bleeds off-edge, behind content, above bg */}
      {motif && (
        <div className="absolute inset-0 -z-10 pointer-events-none select-none overflow-hidden">
          {motif}
        </div>
      )}

      {/* 3. content — always the top stacking layer */}
      <div className="relative z-10 w-full max-w-[1600px] mx-auto">{children}</div>
    </section>
  );
}
```

> **Variant cheatsheet (Kevents preset):** `content` → white bg / slate-900 text (default, most slides). `cover` → full-bleed indigo→purple→pink gradient / white text (title, closing, activity). `divider` → `#f5f3ff` tint / slate-900 text (section breaks, question slides).

> **Canvas frame outline stays on every variant.** On the dark `cover` gradient the Kevents preset uses `outline-white/25` so the dashed 1920×1080 boundary is still visible — Tle wants that cue on every slide. Never remove it.

> **z-layering guarantees no overlap:** bgImage `-z-20`, motif `-z-10`, content `z-10`. Content always paints above the motif. Combined with motifs that bias their energy to the right/bottom edges (§ SignatureMotif), text never fights decoration.

> **Alignment (same as v1):** default `top` for content slides (empty space falls to the bottom where controls live). `align="center"` only for hero variants (cover / statement / closing / divider). **Content must end at canvas y ≤ 920** — below that the controls overlay covers it.

### `<SignatureMotif>` — brand motif that bleeds off-edge

The distinctive Kevents decoration. Always `pointer-events-none`, always anchored to an edge/corner so it never sits under left/centered content. A `tone` prop (`onLight` | `onDark`) tunes opacity so the same motif reads on both the dark cover and the light divider. Uses `radial-gradient` + `blur-3xl` (a **static paint**, exports cleanly to PDF) and inline SVG — never `backdrop-blur`.

```tsx
type MotifTone = "onLight" | "onDark";

function SignatureMotif({
  variant = "mesh-arcs",
  tone = "onLight",
}: {
  variant?: "mesh-arcs" | "mark-ghost" | "dot-grid";
  tone?: MotifTone;
}) {
  if (variant === "mesh-arcs") {
    // Soft indigo/purple/pink "blobs" bleeding off the RIGHT edge + a bottom-left wash.
    const op = tone === "onDark" ? "opacity-70" : "opacity-40";
    return (
      <div className={`absolute inset-0 ${op}`} aria-hidden>
        <div className="absolute -right-40 -top-24 w-[820px] h-[820px] rounded-full blur-3xl"
          style={{ background: "radial-gradient(circle at 30% 30%, #7c3aed 0%, rgba(124,58,237,0) 60%)" }} />
        <div className="absolute -right-24 top-1/3 w-[620px] h-[620px] rounded-full blur-3xl"
          style={{ background: "radial-gradient(circle at 40% 40%, #ec4899 0%, rgba(236,72,153,0) 62%)" }} />
        <div className="absolute -left-40 -bottom-40 w-[720px] h-[720px] rounded-full blur-3xl"
          style={{ background: "radial-gradient(circle at 60% 60%, #4f46e5 0%, rgba(79,70,229,0) 60%)" }} />
      </div>
    );
  }

  if (variant === "mark-ghost") {
    // Giant ghosted rounded-square "k" mark, cropped off the bottom-right corner.
    const fill   = tone === "onDark" ? "rgba(255,255,255,0.06)" : "rgba(79,70,229,0.06)";
    const stroke = tone === "onDark" ? "rgba(255,255,255,0.12)" : "rgba(124,58,237,0.14)";
    return (
      <svg className="absolute -right-40 -bottom-48 w-[1100px] h-[1100px]" viewBox="0 0 100 100" aria-hidden fill="none">
        <rect x="6" y="6" width="88" height="88" rx="18" fill={fill} stroke={stroke} strokeWidth="1.5" />
        {/* lowercase k glyph as strokes */}
        <path d="M38 26 V74 M38 54 L64 30 M44 50 L66 74" stroke={stroke} strokeWidth="4"
          strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }

  // dot-grid: quiet brand-tinted dot field anchored bottom-right, faded via mask.
  const dot = tone === "onDark" ? "rgba(255,255,255,0.18)" : "rgba(79,70,229,0.16)";
  return (
    <div className="absolute right-0 bottom-0 w-[900px] h-[720px]" aria-hidden
      style={{
        backgroundImage: `radial-gradient(${dot} 2px, transparent 2px)`,
        backgroundSize: "28px 28px",
        WebkitMaskImage: "radial-gradient(120% 120% at 100% 100%, #000 30%, transparent 72%)",
        maskImage: "radial-gradient(120% 120% at 100% 100%, #000 30%, transparent 72%)",
      }} />
  );
}
```

> **Which motif where:** `mesh-arcs` = default for `cover` + `divider` (the hero-mesh brand look, biased right). `mark-ghost` = the most brand-specific — great on cover + closing. `dot-grid` = quietest — good on activity/recap slides. **On a centered `text-8xl` hero, prefer `mark-ghost` or `dot-grid`** (corner-anchored) so a mesh blob never lowers title contrast; if you use `mesh-arcs`, push it fully off the right edge.

### `<Kicker>` — small uppercase label above headings

```tsx
function Kicker({ children, spacing = "mb-4" }: { children: React.ReactNode; spacing?: string }) {
  return (
    <p className={`text-[11px] tracking-[0.3em] uppercase ${theme.kicker} font-semibold ${spacing}`}>
      {children}
    </p>
  );
}
```

> **Spacing rule for Thai** (same as v1): when the next heading is `text-7xl`+, pass `spacing="mb-10"` and add `pt-2 leading-[1.05]` to the heading — Thai diacritics (ไม้เอก/ตรี) overflow cap-height and overlap the kicker otherwise.

### `<SlideNumber>` — top-right counter

```tsx
function SlideNumber({ current, total }: { current: number; total: number }) {
  return (
    <div className={`absolute top-6 right-8 text-xs font-mono ${theme.muted} tabular-nums flex items-center gap-1`}>
      <span className="deck-digit-rotate">{String(current).padStart(2, "0")}</span>
      <span>/</span>
      <span className="deck-digit-rotate">{String(total).padStart(2, "0")}</span>
    </div>
  );
}
```

> On the dark `cover` variant, the default `theme.muted` (slate-400) reads faintly on the gradient — that's usually fine (the counter is chrome). If you need it crisper, wrap it locally in `text-white/70`.

### `<CalloutBar>` — icon + text in a soft tinted box

The signature takeaway strip (the "lead icon + one line" callout under compare/case-study slides). **The icon is always a Heroicon passed via `icon` — never an emoji in the text** (see the NO-EMOJI rule below).

```tsx
function CalloutBar({ icon: Icon, children, tone = "indigo" }: {
  icon?: React.ComponentType<{ className?: string }>;
  children: React.ReactNode;
  tone?: "indigo" | "violet" | "slate";
}) {
  const tint = tone === "violet" ? theme.tintViolet : tone === "slate" ? theme.tintSlate : theme.tintIndigo;
  return (
    <div className={`flex items-center gap-4 rounded-2xl px-7 py-5 ${tint}`}>
      {Icon && <Icon className="w-8 h-8 shrink-0" aria-hidden />}
      <p className="text-2xl leading-snug">{children}</p>
    </div>
  );
}
// Usage: <CalloutBar icon={PencilSquareIcon}>ข้อความสรุป…</CalloutBar>
```

> ### ⛔ NO EMOJI — anywhere, ever (hard rule)
> Emoji make a deck read as AI-generated. **Never** put an emoji in slide text, headings, labels, card "icons", callouts, tags, step lists, or even inside mockups. This applies to `✅ ❌ 🔒 🔁 🎯 💡 🏠 📄 🗄 💬 📁 📊 🧠 🎬 🙋 🔥 ⚠️ 🎁 📸 📝 ✍️` and every other emoji.
> - **Need an icon?** Import a Heroicon (`@heroicons/react/24/outline`) and render the component — e.g. status → `CheckCircleIcon` / `XCircleIcon`, lock → `LockClosedIcon`, database → `CircleStackIcon`, note → `PencilSquareIcon`, warning → `ExclamationTriangleIcon`, "your business" swap → `ArrowsRightLeftIcon`, gift → `GiftIcon`.
> - **Card that used an emoji as its icon?** Put the Heroicon in a badge (`w-12 h-12` in a `theme.tint*` or `theme.numberBadge` square/circle), not an emoji glyph.
> - **Plain typographic arrows** (`→ ← ↔ ↳`) inside flow text (e.g. `To do → Doing → Done`) are fine — they render as normal glyphs, not colored emoji. Everything pictographic is not.

### `<PillBadge>` — dark rounded-full label

The `bg-slate-900` pill (e.g. "ACTIVITY", "OGP Learning", "What went wrong?").

```tsx
function PillBadge({ children }: { children: React.ReactNode }) {
  return (
    <span className={`inline-flex items-center gap-2 ${theme.pill} px-4 py-1.5 text-[11px] tracking-[0.15em] uppercase font-semibold`}>
      {children}
    </span>
  );
}
```

### `<NumberBadge>` — gradient number circle

```tsx
function NumberBadge({ children }: { children: React.ReactNode }) {
  return (
    <span className={`inline-flex items-center justify-center w-14 h-14 rounded-full ${theme.numberBadge} text-2xl font-bold tabular-nums shrink-0`}>
      {children}
    </span>
  );
}
```

### Gradient title + underline-accent conventions

Two ways to emphasize a keyword in an H1/H2 (`text-5xl`+ only — never on body):

```tsx
{/* A. gradient-clip the one accent word (indigo→purple→pink). Add leading/pb so
      tall Thai combining marks aren't cut by the tight gradient box. */}
<h2 className={`text-5xl font-bold ${theme.text} leading-tight`}>
  ทำไมต้อง <span className={`${theme.gradientText} leading-[1.15] pb-1`}>ระบบเดียว</span>
</h2>

{/* B. underline-accent (a short violet stroke under a keyword) */}
<h2 className={`text-5xl font-bold ${theme.text} leading-tight`}>
  เริ่มที่ <span className={theme.underlineAccent}>ปัญหา</span> ไม่ใช่ไอเดีย
</h2>
```

> **Never** apply `gradientText` to a whole multi-line Thai paragraph or to body text — gradient-clip lowers contrast; keep it to one display-size accent word.

---

## Layout principles (read before composing any slide)

Tle's standing rule: **"empty space is fine — but never make the viewer wonder why it's there."** Principles 1–6 are identical to v1; principle 7 is new for v2's background tiers.

### 1. Default to top-aligned content
Use `align="top"` (default) on every content slide — empty space then falls at the bottom where the controls pill lives, reading as deliberate breathing room. Reserve `align="center"` for hero variants (cover / statement / closing / divider).

### 2. Don't split a slide into disconnected bands
Don't put a heading at top and a metadata row at the bottom with a wide empty stripe between. Collapse to a single coherent block — a 2-column unit sharing a top edge, or a single top-to-bottom column.

### 3. Make cards tall when the slide is sparse
For 2–4 card grids, give short cards more vertical room: bigger padding (`p-10`/`p-12`), internal gaps, a divider inside the card. A 380–500px-tall card reads as substantial; a 200px one looks lonely.

### 4. Balance the two columns of a 2-col layout
If one column is much shorter, add supporting content (checklist, small mockup, stat callout) until both finish at roughly the same height.

### 5. Use `aspect-[X/Y]` for hero images, not fixed pixel heights
`aspect-[4/3]` grows with the column and fills the canvas; a fixed `h-[260px]` leaves dead space on sparse slides.

### 6. Vertical-fill audit
After composing, eyeball it: does content occupy ≥ ~75% of canvas height (~750px of the 888px content area)? If not, is the empty band *explained* (bottom of a top-aligned slide, or a deliberate hero)? If neither, fix via principles 3–5.

### 7. Background-tier discipline (NEW in v2)
The 3-tier system only reads as intentional if you use it with rhythm:
- **`cover`** (solid/gradient) — the title, the closing, and full-bleed **activity** slides. One big thing on a bold field.
- **`content`** (white) — the workhorse. The vast majority of slides.
- **`divider`** (tint + motif) — announces a new section/part or poses a transition question. **Never place two dividers back-to-back**, and never use a divider for ordinary content — it loses its "a new chapter starts here" signal.
- **Motif energy stays right/bottom/corner** so it never fights left-aligned or centered content. One motif per slide; don't stack variants.

---

## Gallery

v2 template ids are `K01…K24`. K01–K11 are the v1 patterns restyled to Kevents tokens; K12–K24 are the new archetypes. When a ref elsewhere names a template, use its **name** (e.g. `tool-feature`) — ids differ between v1 (T13) and v2 (K10).

### K01 · `cover` — title + tagline (gradient bg + motif)

**When to use**: Slide 1. `variant="cover"` puts the title on the full-bleed signature gradient.

**Data**: `kicker, meta, titleLead, titleAccent, tagline, presenterName, presenterRole`

```tsx
<SlideShell number={1} total={totalSlides} label="Cover" variant="cover" align="center"
  motif={<SignatureMotif variant="mark-ghost" tone="onDark" />}>
  <SlideNumber current={1} total={totalSlides} />
  {/* top row: wordmark left, event meta right */}
  <div className="absolute top-16 left-20 right-20 flex items-center justify-between text-white/90">
    <span className="text-2xl font-bold tracking-tight lowercase">kevents</span>
    <span className="text-2xl text-white/70">{meta}</span>
  </div>
  <div>
    <Kicker spacing="mb-8"><span className="text-white/80">{kicker}</span></Kicker>
    <h1 className="text-8xl font-bold tracking-tight text-white leading-[1.05] pt-2">
      {titleLead}<br />{titleAccent}
    </h1>
    <p className="mt-6 text-3xl text-white/85 font-medium leading-relaxed">{tagline}</p>
    <div className="mt-12 space-y-1 text-white/80">
      <p className="text-2xl font-semibold text-white">{presenterName}</p>
      <p className="text-2xl">{presenterRole}</p>
    </div>
  </div>
</SlideShell>
```

> On `cover`, text is already white via the variant. Use `text-white/85` for the tagline and `text-white/70` for meta — solid gradient text (`gradientText`) is invisible on the gradient, so don't use it here; the whole title is white.

### K02 · `statement` — single huge statement (LCD)

**When to use**: The one line to remember. `variant="divider"` (tint) or `cover` (gradient) with the accent word in `gradientText` (divider) or plain white emphasis (cover).

```tsx
<SlideShell number={N} total={totalSlides} label="Statement" variant="divider" align="center"
  motif={<SignatureMotif variant="dot-grid" tone="onLight" />}>
  <SlideNumber current={N} total={totalSlides} />
  <div className="text-center">
    <Kicker spacing="mb-10">{kicker}</Kicker>
    <h2 className={`text-8xl font-bold ${theme.text} leading-[1.05] pt-2`}>
      {mainText} <span className={`${theme.gradientText} leading-[1.15] pb-1`}>{accentText}</span>
    </h2>
    {supportingText && <p className={`mt-8 text-2xl ${theme.subtle} max-w-3xl mx-auto`}>{supportingText}</p>}
  </div>
</SlideShell>
```

### K03 · `stat-grid` — 3–4 numbers with labels

**When to use**: Scale/traction numbers. `variant="content"`. Grid of `theme.glassCard` cells; each = big `text-8xl` number (`gradientText` optional) + `text-2xl` label. Bump padding to `p-10` when only 3 cells (principle 3).

### K04 · `feature-grid` — 2–4 features (icon + title + desc)

**When to use**: Services/features side-by-side. Cards alternate `theme.tintIndigo` / `tintViolet` / `tintSlate` for rhythm; icon in a `theme.numberBadge`-style gradient square, `text-2xl` title + `theme.subtle` desc.

### K05 · `two-column` — heading + lead left, list/visual right

**When to use**: One topic + supporting examples. Left: `Kicker` + `text-5xl` heading + `text-2xl` lead. Right: a `theme.glassCard` with a bulleted list or a small `MockFrame`. Balance heights (principle 4).

### K06 · `case-study` — featured case (visual + narrative)

**When to use**: One hero project/example. See also **K20 chat-bubbles** for the conversational case-study treatment. Layout: `text-5xl` heading, then a 2-col: narrative bullets in a `glassCard` left, a `MockFrame`/image right, a `CalloutBar` takeaway at the bottom.

### K07 · `callout-list` — personas / segments

**When to use**: 2–4 personas (Looking-for / ICP). Bordered `theme.card` rows, each: icon + `text-2xl` title + one-line `theme.subtle` desc.

### K08 · `comparison` — wrong vs right / before-after

**When to use**: Misconceptions or A-vs-B where one side is *literally* correct. 2-col; use the **restrained** semantic tints — `theme.semanticBad` (rose) for wrong, `theme.semanticGood` (emerald) for right. For non-judgemental "option A vs B" use **K15 compare-columns** with brand tints instead.

```tsx
<div className="grid grid-cols-2 gap-8">
  <div className={`rounded-2xl p-8 ${theme.semanticBad}`}>
    <p className="text-2xl font-bold flex items-center gap-2"><XMarkIcon className="w-7 h-7" /> Idea first</p>
    <p className="mt-4 text-2xl leading-relaxed">…</p>
  </div>
  <div className={`rounded-2xl p-8 ${theme.semanticGood}`}>
    <p className="text-2xl font-bold flex items-center gap-2"><CheckBadgeIcon className="w-7 h-7" /> Problem first</p>
    <p className="mt-4 text-2xl leading-relaxed">…</p>
  </div>
</div>
```

### K09 · `closing` — thank-you + contact

**When to use**: Last slide. `variant="cover"` (gradient) + `mark-ghost` motif, or `variant="divider"` + `mesh-arcs`. Big `text-8xl` "ขอบคุณ" / "Thank you", then contact chips (`theme.chip`) or a line of contact info.

### K10 · `tool-feature` — teach one tool/feature (explanation + mockup)

**When to use**: The core teaching slide — one capability, "what/how" beside an illustrative mockup. `variant="content"`. Same structure as v1's tool-feature: left column has a `คืออะไร` card (`theme.tintIndigo`) + a `ทำงานยังไง` card (`theme.card`) with a checklist; right column is a `<MockFrame app={name}>`. See "Illustrative mockups" below.

### K11 · `tool-landscape` — survey the category before the chosen tool

**When to use**: Right before introducing the tool you'll teach — show the alternatives and why you picked this one (Start-With-Why build-up). Grid of option cards; the chosen one gets `theme.tintIndigo` + `ring-2 ring-indigo-400` + a `PillBadge` "เราจะใช้ตัวนี้"; a `CalloutBar` explains why.

### K12 · `section-divider` — full-page "PART N" break

**When to use**: A full-page break announcing a new section/part (the thing Tle wants *before every new topic*). `variant="divider"`, `align="center"`, `mesh-arcs` motif.

**Data**: `part, titleLead, titleAccent, supporting`

```tsx
<SlideShell number={N} total={totalSlides} label={`PART ${part}`} variant="divider" align="center"
  motif={<SignatureMotif variant="mesh-arcs" tone="onLight" />}>
  <SlideNumber current={N} total={totalSlides} />
  <div>
    <p className={`text-[11px] tracking-[0.3em] uppercase font-semibold ${theme.accent} mb-10`}>PART {part}</p>
    <h2 className={`text-8xl font-bold leading-[1.05] pt-2 ${theme.text}`}>
      {titleLead} <span className={`${theme.gradientText} leading-[1.15] pb-1`}>{titleAccent}</span>
    </h2>
    {supporting && (
      <p className={`mt-8 text-2xl italic ${theme.subtle} max-w-3xl leading-relaxed`}>{supporting}</p>
    )}
  </div>
</SlideShell>
```

> Left-aligned title (not centered) matches the reference deck's PART slides. The `mesh-arcs` motif sits off the right edge, clear of the title.

### K13 · `question` / transition — big provocative one-liner

**When to use**: A transition question between sections ("What are we doing today?"). Like K12 but no "PART N" kicker, and the title is centered or left with one word in `gradientText` or `underlineAccent`.

```tsx
<SlideShell number={N} total={totalSlides} label="Question" variant="divider" align="center"
  motif={<SignatureMotif variant="dot-grid" tone="onLight" />}>
  <SlideNumber current={N} total={totalSlides} />
  <h2 className={`text-8xl font-bold leading-[1.05] pt-2 ${theme.text}`}>
    {lead} <span className={`${theme.gradientText} leading-[1.15] pb-1`}>{accent}</span>
  </h2>
</SlideShell>
```

### K14 · `agenda` / schedule table — time · topic · description rows

**When to use**: Run-of-show for a day/session. `variant="content"`.

**Data**: `heading, rows: { time, topic, desc, highlight? }[]`

```tsx
<SlideShell number={N} total={totalSlides} label="Agenda">
  <SlideNumber current={N} total={totalSlides} />
  <h2 className={`text-5xl font-bold ${theme.text} leading-tight mb-8`}>{heading}</h2>
  <div className="space-y-2">
    {rows.map((r, i) => (
      <div key={r.topic}
        className={`grid grid-cols-12 items-center gap-6 rounded-xl px-6 py-4
          ${r.highlight ? theme.tintIndigo : i % 2 === 0 ? "bg-white" : "bg-slate-50"}`}>
        <span className="col-span-2 text-2xl font-bold tabular-nums text-indigo-600">{r.time}</span>
        <span className={`col-span-3 text-2xl font-bold ${theme.text}`}>{r.topic}</span>
        <span className={`col-span-7 text-2xl ${theme.subtle}`}>{r.desc}</span>
      </div>
    ))}
  </div>
</SlideShell>
```

> Keep every cell at `text-2xl`. If the table overflows the 920 budget, **cut rows** (split across two agenda slides), don't shrink the font.

### K15 · `compare-columns` — 2 or 3 glass columns

**When to use**: Option A vs B (vs C) with no right/wrong verdict. 2–3 `theme.glassCard` columns, each with a tinted header (`tintIndigo` / `tintViolet` / `tintSlate`) + a bulleted `text-2xl` list. A `CalloutBar` takeaway optional at the bottom. (For a true right/wrong verdict use **K08** with semantic tints.)

```tsx
<div className={`grid grid-cols-3 gap-6`}>
  {cols.map((c) => (
    <div key={c.title} className={`rounded-2xl ${theme.glassCard} overflow-hidden`}>
      <div className={`px-6 py-4 ${c.tint}`}><p className="text-2xl font-bold">{c.title}</p></div>
      <ul className="p-6 space-y-3">
        {c.items.map((it) => <li key={it} className={`text-2xl ${theme.subtle} leading-snug`}>{it}</li>)}
      </ul>
    </div>
  ))}
</div>
```

### K16 · `process-flow` — cards + arrows

**When to use**: A 3–4 step pipeline (Idea → Assume → Build → Demo). The key/active step gets `theme.accentBg` + `theme.glow`; the rest `theme.tintSlate`. Arrows between cards.

```tsx
<div className="flex items-stretch gap-4">
  {steps.map((s, i) => (
    <React.Fragment key={s.title}>
      <div className={`flex-1 rounded-2xl p-7 ${s.active ? `${theme.accentBg} ${theme.glow}` : theme.tintSlate}`}>
        <p className={`text-2xl font-bold ${s.active ? "text-white" : theme.text}`}>{s.title}</p>
        <p className={`mt-3 text-2xl leading-snug ${s.active ? "text-white/85" : theme.subtle}`}>{s.desc}</p>
      </div>
      {i < steps.length - 1 && <ArrowRightIcon className={`w-10 h-10 ${theme.accent} shrink-0 self-center`} aria-hidden />}
    </React.Fragment>
  ))}
</div>
```

> Use fixed `flex`/`grid-cols-N` — **no responsive prefixes** even though a 4-card row "wants" to wrap.

### K17 · `numbered-cards` — ordered points as cards

**When to use**: An ordered list of 3–4 points. `grid grid-cols-4 gap-6`; each card has a `<NumberBadge>` top-left, `text-2xl` title, `theme.subtle` desc. Optional fill-in-the-blank sentence with `theme.underlineAccent` blanks underneath.

### K18 · `grid-2x2` — four peer items

**When to use**: Four equal items (e.g. Frequency / Severity / Evidence / Outcome). `grid grid-cols-2 gap-8`; alternate tints (indigo/violet/slate/indigo) or all `glassCard`. Each: `text-2xl` bold title + `theme.subtle` line.

### K19 · `quadrant-matrix` — 2×2 with axes

**When to use**: Positioning on two axes (risk × evidence, effort × impact). Keep the plotting area square and within budget.

```tsx
<SlideShell number={N} total={totalSlides} label="Matrix">
  <SlideNumber current={N} total={totalSlides} />
  <h2 className={`text-5xl font-bold text-center ${theme.text} mb-8`}>{heading}</h2>
  <div className="relative mx-auto aspect-square max-w-[720px]">
    {/* 4 quadrants */}
    <div className="absolute inset-0 grid grid-cols-2 grid-rows-2 gap-2">
      <div className={`rounded-tl-2xl flex items-center justify-center ${theme.tintViolet}`}><span className="text-2xl font-bold">{q.tl}</span></div>
      <div className={`rounded-tr-2xl flex items-center justify-center ${theme.semanticBad}`}><span className="text-2xl font-bold">{q.tr}</span></div>
      <div className={`rounded-bl-2xl flex items-center justify-center ${theme.tintSlate}`}><span className="text-2xl font-bold">{q.bl}</span></div>
      <div className={`rounded-br-2xl flex items-center justify-center ${theme.tintIndigo}`}><span className="text-2xl font-bold">{q.br}</span></div>
    </div>
    {/* axis labels — outside the square */}
    <span className={`absolute -left-4 top-1/2 -translate-x-full -translate-y-1/2 -rotate-90 text-2xl ${theme.subtle}`}>{yAxis}</span>
    <span className={`absolute left-1/2 -bottom-12 -translate-x-1/2 text-2xl ${theme.subtle}`}>{xAxis}</span>
  </div>
</SlideShell>
```

### K20 · `chat` / case-study bubbles

**When to use**: Show a real conversation/quotes as evidence. Chat bubbles + a `PillBadge` header + optional `MockFrame` screenshot + a `CalloutBar` takeaway.

```tsx
<SlideShell number={N} total={totalSlides} label="Case study">
  <SlideNumber current={N} total={totalSlides} />
  <h2 className={`text-5xl font-bold ${theme.text} leading-tight mb-8`}>{heading}</h2>
  <div className="grid grid-cols-12 gap-8">
    <div className="col-span-7 space-y-4">
      <div className="flex justify-end"><PillBadge>{badge}</PillBadge></div>
      {bubbles.map((b, i) => (
        <p key={i} className={`max-w-[80%] rounded-2xl px-6 py-4 text-2xl leading-snug
          ${b.who === "user" ? `ml-auto ${theme.accentBg} text-white` : theme.tintSlate}`}>{b.text}</p>
      ))}
    </div>
    <div className="col-span-5"><MockFrame app={app}>{mock}</MockFrame></div>
  </div>
  <div className="mt-8"><CalloutBar icon={PencilSquareIcon} tone="indigo">{takeaway}</CalloutBar></div>
</SlideShell>
```

### K21 · `activity` / workshop — floating glass card on a gradient

**When to use**: A hands-on exercise (high value — Tle runs workshops). `variant="cover"` gradient with a floating white glass card holding the steps.

**Data**: `title, duration, steps: string[], goal`

```tsx
<SlideShell number={N} total={totalSlides} label="Activity" variant="cover" align="center"
  motif={<SignatureMotif variant="dot-grid" tone="onDark" />}>
  <SlideNumber current={N} total={totalSlides} />
  <div className={`w-full max-w-[1200px] mx-auto rounded-3xl bg-white/80 backdrop-blur-xl border border-white/60 ${theme.glow} p-12`}>
    <div className="flex items-center gap-3 mb-6">
      <PillBadge>Activity</PillBadge>
      <span className={`inline-flex items-center gap-2 ${theme.chip} px-4 py-1.5 text-2xl font-semibold`}>
        <ClockIcon className="w-6 h-6" aria-hidden /> {duration}
      </span>
    </div>
    <h2 className={`text-5xl font-bold ${theme.text} leading-tight`}>{title}</h2>
    <ol className="mt-8 space-y-5">
      {steps.map((s, i) => (
        <li key={s} className="flex items-start gap-5">
          <NumberBadge>{i + 1}</NumberBadge>
          <p className="text-2xl text-slate-700 leading-relaxed pt-2">{s}</p>
        </li>
      ))}
    </ol>
    <div className="mt-8">
      <CalloutBar icon={FlagIcon} tone="indigo"><span className="font-bold">เป้าหมาย:</span> {goal}</CalloutBar>
    </div>
  </div>
</SlideShell>
```

> The card is `bg-white/80` over the gradient — high contrast, so it stays legible even if `backdrop-blur` degrades in PDF export. **Budget**: keep the card ≤ ~820px tall — cap steps at 4–5 or drop the goal bar. If it overflows, split into two activity slides.

### K22 · `criteria-columns` — colored header card + neutral body list

**When to use**: Selection/judging criteria (User value / Public goal / Build risk). 3 columns; each = a colored **header card** (`theme.accentBg` or a tint) stacked directly above a **neutral body list** (`theme.card`, `space-y-3`, `text-2xl`) so header + body read as one unit.

### K23 · `photo-strip` — 3–4 images/screenshots in a row

**When to use**: A journey/timeline shown in real captures. `grid grid-cols-4 gap-6`; each = `aspect-[4/3] rounded-2xl overflow-hidden ${theme.glow}` with `<Image fill className="object-cover" />` + a `text-2xl ${theme.subtle} mt-3` caption. Tag illustrative frames `ภาพประกอบ` (see mockups). Use real `w`/`h` or `aspect-*`; never let content drive image height.

### K24 · `checklist-recap` — numbered rows + side callout

**When to use**: End-of-section recap ("Do you have these five answers now?"). 2-col: numbered rows left (`col-span-8`), a `theme.glassCard` callout right (`col-span-4`). Last row highlighted `theme.tintIndigo` with a `theme.numberBadge` circle to signal completion.

```tsx
<div className="grid grid-cols-12 gap-8">
  <div className="col-span-8 space-y-3">
    {rows.map((r, i) => (
      <div key={r} className={`flex items-center gap-5 rounded-xl px-5 py-4 ${i === rows.length - 1 ? theme.tintIndigo : "border-b border-slate-200"}`}>
        <NumberBadge>{i + 1}</NumberBadge>
        <p className={`text-2xl ${theme.text}`}>{r}</p>
      </div>
    ))}
  </div>
  <div className={`col-span-4 rounded-2xl ${theme.glassCard} p-8 flex items-center`}>
    <div className="flex items-start gap-3">
      <PencilSquareIcon className="w-8 h-8 shrink-0 text-indigo-500" aria-hidden />
      <p className={`text-2xl ${theme.subtle} leading-relaxed`}>{sideNote}</p>
    </div>
  </div>
</div>
```

---

## Illustrative mockups (REQUIRED for teaching tool/feature slides)

When a slide teaches "what tool/feature X looks like and does", **show a mockup of its UI** — a clean, on-brand HTML stand-in built from `div`s — instead of describing it in words. Mandatory for teaching/workshop decks (see SKILL.md → "Teaching / Workshop decks"). Mockups are **illustrative, not real screenshots** — always tag them `ภาพประกอบ`.

### `MockFrame` — app-window wrapper with "ภาพประกอบ" badge

```tsx
function MockFrame({ children, app = "App" }: { children: React.ReactNode; app?: string }) {
  return (
    <div className={`relative h-full min-h-[420px] rounded-2xl border border-slate-200 bg-white ${theme.glow} overflow-hidden flex flex-col`}>
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

> **Mockup sizing is chrome, not content** — inside a `MockFrame`, `text-sm`/`text-[13px]`/`text-[15px]` ARE allowed (mimicking real app chrome). This is the one place the 5-size rule relaxes. Keep slide *content* on the normal scale. Build the inner mock from primitives that *suggest* the UI (chat bubbles, sidebar + channel list, kanban columns, a table, chart bars, skeleton rows).

### Phone / device mockup — LOCK width AND height (never let content drive it)

When the mockup is a **device**, give the frame an explicit `w-[…px] h-[…px]` so it keeps a real aspect ratio. The classic mistake: setting only width and letting content drive height → the frame renders almost square, which reads as broken.

- **Phone** → lock to ~**1 : 2.05–2.16**. Canonical `w-[300px] h-[620px]`; also `w-[280px] h-[580px]`, `w-[330px] h-[680px]`.
- Inner screen is `flex flex-col`; the scrolling content area gets `flex-1 overflow-hidden`. Mark every fixed region (`status bar`, `input bar`) `shrink-0`.
- **Budget**: a 620px phone + a heading must fit the 920-canvas-px budget. Shrink the heading to `text-5xl` or the phone to `h-[580px]` before letting it overflow. Run the principle-6 audit after adding one.

Copy the canonical `PhoneMock` shape from [`slide-templates-v1.md`](./slide-templates-v1.md) → "Phone / device mockup" (identical), swapping `theme.accent`/`accentBg`/`accentSoft` — with Kevents those resolve to indigo automatically. Same principle for a paper/worksheet mockup: lock a real proportion, keep text `text-3xl`+ to read from the back of the room.

---

## Cheat sheet — pick a template

| Situation | Template | Variant |
|-----------|----------|---------|
| First slide | K01 cover | cover |
| The one line they must remember | K02 statement | divider/cover |
| 3–4 numbers showing scale | K03 stat-grid | content |
| 3 services/features side-by-side | K04 feature-grid | content |
| One topic + supporting examples | K05 two-column | content |
| One hero project in detail | K06 case-study | content |
| Target personas (Looking-for / ICP) | K07 callout-list | content |
| Misconceptions / right-vs-wrong | K08 comparison | content |
| **New section / "PART N" break** | **K12 section-divider** | **divider** |
| **Transition question** | **K13 question** | **divider** |
| Day/session run-of-show | K14 agenda | content |
| Option A vs B vs C (no verdict) | K15 compare-columns | content |
| A 3–4 step pipeline | K16 process-flow | content |
| Ordered list of points | K17 numbered-cards | content |
| Four peer items | K18 grid-2x2 | content |
| Positioning on two axes | K19 quadrant-matrix | content |
| A conversation / quotes as evidence | K20 chat-bubbles | content |
| **Hands-on exercise (workshop)** | **K21 activity** | **cover** |
| Selection/judging criteria | K22 criteria-columns | content |
| Real screenshots/photos in a row | K23 photo-strip | content |
| End-of-section recap | K24 checklist-recap | content |
| Teach one tool/feature (with mockup) | K10 tool-feature | content |
| Survey tools before teaching one | K11 tool-landscape | content |
| Last slide | K09 closing | cover/divider |

## Adding / upgrading a template

1. Add a new `### KXX · <name>` section to **Gallery** with: when-to-use, data shape, JSX skeleton, and its default `variant`.
2. Add a row to the **Cheat sheet** (include the variant column).
3. If it needs new icons or theme tokens, note them (new tokens go in [`themes.md`](./themes.md) Preset 5, kept additive).
4. Future decks pick it up. Existing decks unchanged (static React snapshots).
