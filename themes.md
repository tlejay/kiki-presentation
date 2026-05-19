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
  shellPadding: "px-6 md:px-20 py-16",
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
  shellPadding: "px-6 md:px-20 py-16",
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
  shellPadding: "px-6 md:px-20 py-16",
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
  shellPadding: "px-6 md:px-20 py-16",
  frameOutline: "outline-dashed outline-1 -outline-offset-1 outline-stone-300",
}
```

When to use: portfolio decks, brand stories, content/lifestyle work.

## Preset 5 — Custom

If Tle picks "Custom", ask a follow-up `AskUserQuestion` with these:

1. **Mode**: Light / Dark
2. **Primary accent**: pick from a palette (Amber, Blue, Emerald, Rose, Violet, Custom hex)
3. **Vibe**: Clean / Bold / Soft

Then synthesize a token set following the same shape as the presets above. **Always include `frameOutline`** — pick a stroke that has gentle (not harsh) contrast against the chosen `bg`: light themes → `outline-gray-300`-ish; dark themes → `outline-white/15`-to-`outline-neutral-700`-ish.

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
  ],
}
```

If they pick "Other" / "Custom", follow up with the Mode + Accent + Vibe sub-question.

## Adding a new preset (Tle upgrades the skill)

When Tle wants a new preset:
1. Add a new `## Preset N — <Name>` section to this file with the token block.
2. Add it as an option in the canonical AskUserQuestion form above.
3. Future decks pick it up automatically. Existing decks are unaffected.
