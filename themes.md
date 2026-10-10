# Theme Presets

Always ask Tle to pick a theme via `AskUserQuestion` — never silently default. Each preset below is a complete token set you apply consistently across all slides in the deck.

## How to apply a theme

A theme is just a set of Tailwind class fragments. Decide them up-front (top of `<slug>-deck.tsx` as `const T = { ... }`) and reference them everywhere instead of repeating literal classes.

```tsx
// Example pattern at top of deck
const theme = {
  bg: "bg-white",
  text: "text-gray-900",
  muted: "text-gray-500",
  accent: "text-amber-500",
  accentBg: "bg-amber-500",
  accentSoft: "bg-amber-50 border-amber-200",
  border: "border-gray-200",
  card: "bg-white border-gray-200 hover:border-amber-300",
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-gray-300",
} as const;
```

> **`shellPadding`** mirrors the padding `SlideShell` hardcodes (`px-20 pt-24 pb-40`; v3 `pt-28`) — canvas mode has no `md:` breakpoints, so never write `px-6 md:px-20` here.

> **`frameOutline`** is non-optional — every theme MUST set it. It draws the dashed canvas border on every slide (visible in production, by Tle's preference, as a visual cue that "this is a 1920×1080 canvas"). Pick a stroke color that has gentle contrast against the theme's `bg`.

Then in slides:
```tsx
<h2 className={`text-6xl font-bold ${theme.text}`}>
  Hello <span className={theme.accent}>World</span>
</h2>
```

## Preset 1 — MakeByTle (default)

White, clean, amber accent. Matches `madebytle.com`.

```ts
{
  name: "MakeByTle",
  bg: "bg-white",
  text: "text-gray-900",
  muted: "text-gray-500",
  subtle: "text-gray-600",
  accent: "text-amber-500",
  accentBg: "bg-amber-500 text-white",
  accentSoft: "bg-amber-50 border border-amber-200",
  accentSoftHover: "hover:border-amber-300 hover:bg-amber-50",
  border: "border-gray-200",
  kicker: "text-amber-600",
  shellPadding: "px-20 pt-24 pb-40",
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-gray-300",
}
```

When to use: default, BNI presentations, anything that should feel consistent with MakeByTle.com.

## Preset 2 — Premium Dark

Navy/black background, gold accent. Feels like a luxury BNI blazer.

```ts
{
  name: "Premium Dark",
  bg: "bg-neutral-950",
  text: "text-neutral-50",
  muted: "text-neutral-400",
  subtle: "text-neutral-300",
  accent: "text-amber-400",
  accentBg: "bg-amber-400 text-neutral-950",
  accentSoft: "bg-amber-400/10 border border-amber-400/30",
  accentSoftHover: "hover:border-amber-400/60 hover:bg-amber-400/15",
  border: "border-neutral-800",
  kicker: "text-amber-400",
  shellPadding: "px-20 pt-24 pb-40",
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-neutral-700",
}
```

When to use: BNI premium chapters, executive pitches, gala/award contexts.

## Preset 3 — Gradient AI

Animated gradient background, white text — feels distinctly "AI / future". Use sparingly; great for AI/ML decks but loud for general business.

```ts
{
  name: "Gradient AI",
  bg: "bg-gradient-to-br from-violet-700 via-blue-700 to-cyan-600",
  text: "text-white",
  muted: "text-white/70",
  subtle: "text-white/85",
  accent: "text-cyan-300",
  accentBg: "bg-white text-violet-700",
  accentSoft: "bg-white/10 border border-white/20 backdrop-blur-sm",
  accentSoftHover: "hover:border-white/40 hover:bg-white/15",
  border: "border-white/15",
  kicker: "text-cyan-300",
  shellPadding: "px-20 pt-24 pb-40",
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-white/20",
}
```

When to use: AI / data / ML pitches, hackathon demos, conference keynotes.

## Preset 4 — Editorial Minimal

Cream background, charcoal text, single colored accent. Reads like a magazine spread.

```ts
{
  name: "Editorial Minimal",
  bg: "bg-stone-50",
  text: "text-stone-900",
  muted: "text-stone-500",
  subtle: "text-stone-700",
  accent: "text-rose-600",
  accentBg: "bg-stone-900 text-stone-50",
  accentSoft: "bg-rose-50 border border-rose-200",
  accentSoftHover: "hover:border-rose-300 hover:bg-rose-50",
  border: "border-stone-200",
  kicker: "text-rose-600",
  shellPadding: "px-20 pt-24 pb-40",
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-stone-300",
}
```

When to use: portfolio decks, brand stories, content/lifestyle work.

## Preset 5 — Kevents (v2 · Kevents brand)

The signature preset for the **v2 gallery** ([`slide-templates-v2.md`](./slide-templates-v2.md)). Indigo→purple→pink gradient, glass cards, and a **3-tier background system** (cover / content / divider). Built for `kevents.club` — event-ticketing, community, Korat.

> **This preset carries EXTRA tokens beyond the v1 shape** (`variants`, `gradientText`, `glassCard`, …). Those tokens are **v2-only** — the v2 `SlideShell` reads `theme.variants[variant]` to swap per-slide backgrounds, and falls back to `bg`/`text`/`frameOutline` if absent, so the four classic presets above still work with v1. Use Kevents only with the v2 gallery; use a classic preset with v1.

```ts
{
  name: "Kevents",

  // --- v1 core shape (used by every content slide) ---
  bg: "bg-white",
  text: "text-slate-900",
  muted: "text-slate-400",
  subtle: "text-slate-600",
  accent: "text-indigo-600",
  accentBg: "bg-indigo-600 text-white",
  accentSoft: "bg-indigo-50 border border-indigo-200",
  accentSoftHover: "hover:border-indigo-300 hover:bg-indigo-50",
  border: "border-slate-200",
  card: "bg-white border-slate-200 hover:border-indigo-300",
  kicker: "text-indigo-600",
  shellPadding: "px-20 pt-24 pb-40",
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-slate-300",

  // --- v2 additive: per-slide background system ---
  // SlideShell reads theme.variants[variant] → {bg, text, frameOutline}
  variants: {
    content: {
      bg: "bg-white",
      text: "text-slate-900",
      frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-slate-300",
    },
    cover: {
      // full-bleed signature gradient (swap to `bg-slate-900` for a solid cover)
      bg: "bg-[linear-gradient(135deg,#4f46e5_0%,#7c3aed_50%,#ec4899_100%)]",
      text: "text-white",
      frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-white/25",
    },
    divider: {
      bg: "bg-[#f5f3ff]", // violet-50-ish tint under the mesh motif
      text: "text-slate-900",
      frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-indigo-200",
    },
  },

  // --- v2 additive: brand effects ---
  gradientText: "bg-[linear-gradient(135deg,#4f46e5,#7c3aed,#ec4899)] bg-clip-text text-transparent",
  glassCard: "bg-white/70 backdrop-blur-xl border border-white/60 rounded-2xl shadow-[0_18px_50px_-24px_rgba(79,70,229,0.35)]",
  glow: "shadow-[0_10px_40px_-10px_rgba(124,58,237,0.45)]",
  pill: "bg-slate-900 text-white rounded-full",
  chip: "bg-slate-100 text-slate-700 rounded-full",
  numberBadge: "bg-[linear-gradient(135deg,#4f46e5,#7c3aed)] text-white",
  underlineAccent: "underline decoration-4 decoration-[#a78bfa] underline-offset-8",

  // context tints (NOT semantic — brand rhythm for cards)
  tintIndigo: "bg-indigo-50 border border-indigo-200 text-indigo-700",
  tintViolet: "bg-violet-50 border border-violet-200 text-violet-700",
  tintSlate:  "bg-slate-50 border border-slate-200 text-slate-700",
  // true right/wrong ONLY (use sparingly)
  semanticGood: "bg-emerald-50 border border-emerald-200 text-emerald-700",
  semanticBad:  "bg-rose-50 border border-rose-200 text-rose-700",
}
```

When to use: **v2 decks** — Kevents event/community content, workshops with hands-on Activity slides, any deck that wants the indigo→purple→pink signature + section dividers. Pair with `variant="cover"` on the title/closing slides, `variant="divider"` on section breaks, `variant="content"` (default) elsewhere. See [`slide-templates-v2.md`](./slide-templates-v2.md).

## Preset 6 — Custom

If Tle picks "Custom", ask a follow-up `AskUserQuestion` with these:

1. **Mode**: Light / Dark
2. **Primary accent**: pick from a palette (Amber, Blue, Emerald, Rose, Violet, Custom hex)
3. **Vibe**: Clean / Bold / Soft

Then synthesize a token set following the same shape as the presets above. **Always include `frameOutline`** — pick a stroke that has gentle (not harsh) contrast against the chosen `bg`: light themes → `outline-gray-300`-ish; dark themes → `outline-white/15`-to-`outline-neutral-700`-ish.

## Preset 7 — Korat City Show (v1 · อวดเมือง palette)

Blue / navy with yellow and coral accents, white content slides and navy cover + closing. Built for `korat-points`
from the working palette in `132 KORAT POINTS/~human/BRAND.md` (values estimated from reference images — **not** an
official brand spec, and the อวดเมือง logo must not be redrawn). Pairs with the illustrated pattern in
[`illustrated-decks.md`](./illustrated-decks.md).

```ts
{
  name: "Korat City Show",
  bg: "bg-white",
  text: "text-[#14263D]",
  muted: "text-[#526174]",
  subtle: "text-[#526174]",
  accent: "text-[#104C92]",
  accentBg: "bg-[#104C92] text-white",
  accentSoft: "bg-[#F4F7FB] border border-[#CBD5E1]",
  border: "border-[#CBD5E1]",
  card: "bg-white border-[#CBD5E1]",
  kicker: "text-[#104C92]",
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-[#CBD5E1]",
  // dark slides (cover, closing) — SlideShell/Kicker/SlideNumber take tone="dark"
  darkBg: "bg-[#002760]",
  darkText: "text-white",
  darkMuted: "text-white/75",
  darkKicker: "text-[#EFBB31]",
  darkFrameOutline: "outline-dashed outline-1 -outline-offset-1 outline-white/20",
  coral: "text-[#F36C75]",          // on navy only — fails contrast on white and on #104C92
  yellow: "text-[#EFBB31]",         // on navy only
  yellowBg: "bg-[#EFBB31] text-[#002760]",  // never white text on yellow
  navyBg: "bg-[#002760] text-white",
}
```

Illustration palette to pass to `/kiki-gpt`: primary `#104C92`, secondary `#F36C75`, accent `#EFBB31`, white,
skin `#E9B990`, hair `#14263D`; outline `#002760` on background `#F4F7FB` (light slides) or outline `#FFFFFF` on
background `#002760` (dark slides).

When to use: Korat / city-pride / chamber-of-commerce / public-campaign decks. This is the one place hex values are
allowed — keep them inside the `theme` object.

## Preset 8 — The Standard (v3 · photo-led)

The preset for the **v3 gallery** ([`slide-templates-v3.md`](./slide-templates-v3.md)). There is no background colour to speak of — every slide is a full-bleed photograph under a black scrim, with white type and one accent per programme. The token block has three parts: `theme` (type + chrome), `ACCENT` (per-programme colour sets) and `SCRIM` (how the photo is darkened). Copy all three from `slide-templates-v3.md` → "Theme + accent + scrim tokens"; the core of it:

```ts
{
  name: "The Standard",
  bg: "bg-neutral-950",            // only visible while a photo loads
  text: "text-white",
  muted: "text-white/60",
  subtle: "text-white/85",
  hairline: "bg-white/50",         // rules, lockup divider, step rail
  divide: "divide-white/30",       // StatRow column lines
  chip: "bg-white/15",             // CheckList pills
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-white/20",
  textShadow: "[text-shadow:0_2px_18px_rgba(0,0,0,0.55)]",
}
// ACCENT  = { coral, amber, magenta, lilac } → each { text, bg, bar, border, outline }
// SCRIM   = { even, heavy, soft, left, right, bottom }
```

Differences from every other preset:
- **No `accent` / `accentBg` / `kicker` on `theme`.** Colour comes from `ACCENT[key]`, chosen per slide, so a deck can give each programme its own colour.
- **Deck root + `layout.tsx` wrapper are `bg-neutral-950`**, and the white controls pill needs literal `text-gray-900` / `text-gray-500` / `bg-red-500` (the theme's `muted` is white).
- **Client palette:** swap the classes inside `ACCENT` (hex allowed there only, as with Korat City Show).

When to use: **v3 decks** — media / sponsorship / event proposals, venue and campaign decks, portfolio show-reels: anything sold through photographs. Needs real photos; see `slide-templates-v3.md` → "Photos". Don't pair it with v1/v2 templates, and don't use a light preset with v3 (the primitives assume white-on-dark).

## How to ask Tle (canonical AskUserQuestion form)

```ts
{
  question: "เลือก theme สำหรับ presentation นี้?",
  header: "Theme",
  multiSelect: false,
  options: [
    { label: "MakeByTle (default)", description: "ขาว/amber — match madebytle.com" },
    { label: "Premium Dark", description: "navy/gold — สไตล์ executive premium" },
    { label: "Gradient AI", description: "gradient purple/blue/cyan — สำหรับงาน AI/tech" },
    { label: "Editorial Minimal", description: "cream/charcoal — สไตล์ magazine portfolio" },
    { label: "Kevents (v2)", description: "indigo→purple→pink gradient, glass — Kevents brand · ต้องใช้กับ gallery v2" },
    // AskUserQuestion caps at 4 options — swap this in for Korat / city / chamber decks:
    { label: "Korat City Show", description: "น้ำเงิน/กรมท่า + เหลือง + coral — โทนอวดเมือง ใช้กับเด็คโคราช/หอการค้า" },
    // v3 gallery only — no theme question needed beyond the accent colours:
    { label: "The Standard (v3)", description: "ภาพถ่ายเต็มจอ + ตัวอักษรขาว + สีเน้นต่อรายการ — ต้องใช้กับ gallery v3" },
  ],
}
```

> **Version coupling:** offer **Kevents** only when SKILL.md Step 2 chose the **v2** gallery (it needs the v2 `SlideShell`). When v1 is chosen, offer the four classic presets. When **v3** is chosen the theme is always **The Standard** — ask instead which accent colour each programme/section gets (coral / amber / magenta / lilac, or the client's palette). Don't mix a v1 theme with v2 (cover/divider silently fall back to plain content).

If they pick "Other" / "Custom", follow up with the Mode + Accent + Vibe sub-question.

## Adding a new preset (Tle upgrades the skill)

When Tle wants a new preset:
1. Add a new `## Preset N — <Name>` section to this file with the token block.
2. Add it as an option in the canonical AskUserQuestion form above.
3. Future decks pick it up automatically. Existing decks are unaffected.
