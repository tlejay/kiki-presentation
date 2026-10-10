# Typography Scale

Authoritative font-size system. **Read this before sizing any text.** This deck system uses only 5 sizes — no exceptions for content.

## Font family (locked — do not import in deck)

The deck inherits **Noto Sans Thai** from MakeByTle's root layout (`madebytle/src/app/layout.tsx`):

```tsx
// Already wired at the app root — DO NOT re-import in your deck.
const notoSansThai = Noto_Sans_Thai({
  variable: "--font-noto-sans-thai",
  subsets: ["thai", "latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
});
```

Decks live under `src/app/presentation/<slug>/` and share that font automatically. Things to remember:

- **Never** add `next/font` imports inside the deck or its layout — duplicates load and cause FOUT.
- **Never** use `font-sans`, `font-mono`, or custom `font-*` utilities on slide content. Inherit the default.
- The mono digits in `SlideNumber` and the controls pill counter use `font-mono` — that's the only allowed font override (Geist Mono, also from the root layout).
- Weights available: `font-light` (300) → `font-extrabold` (800). Bold (700) is the headline default; 800 only when a hero brand line needs extra punch.
- All weights are subset to `["thai", "latin"]` — don't write text in other scripts in slides.

## The 5-size system (Tle's standing rule)

| Token | px | Tailwind | Use |
|-------|----|----|-----|
| **Large** | 96 | `text-8xl` | Hero brand text — Cover, LCD/Statement, Closing. Reserved for the 2-3 slides where the brand name itself IS the content. Use sparingly. |
| **H1** | 48 | `text-5xl` | Every other slide's main headline (section title, slide heading) |
| **H2** | 24 | `text-2xl` | Lead paragraph under H1 — "what this slide is about" intro |
| **Normal** | 24 | `text-2xl` | All body content — card titles, descriptions, list items, bullets, captions, taglines, labels with values |
| **Small** | 11 | `text-[11px] tracking-[0.3em] uppercase` | Kicker labels above headings, section eyebrows. **Never** for prose, bullets, or descriptions. |

Large is a hero-only size. The default for slide headlines is H1 (text-5xl). Reach for Large only when the line of text *is* the slide's whole point (the brand name on the Cover, the one-liner on the LCD/Statement slide, the sign-off on the Closing).

H2 and Normal are the same px (24px) — the difference is role/style:
- **H2** is typically `text-2xl text-gray-600 leading-relaxed` (lead-paragraph treatment, lighter color)
- **Normal** is typically `text-2xl text-gray-900 font-bold` for card titles, `text-2xl text-gray-700` for body

Pick weight/color by role; the size is locked.

## Forbidden in content

- `text-base`, `text-sm`, `text-xs`, `text-[Xpx]` for any reading prose, bullets, list items, captions, footers, taglines.
- `text-3xl`, `text-4xl`, `text-6xl`, `text-7xl`, `text-9xl` anywhere — they break the system.
- `text-8xl` (Large) outside hero slides — never use for normal section headings.

## Allowed exceptions (chrome only — never for content)

| Class | Allowed only for |
|-------|------------------|
| `text-xs` (12px) | Slide-number badge in the corner (`SlideNumber` primitive), counter inside the controls pill, monospace tabular-nums chrome |
| `text-sm`, `text-base`, `text-[Npx]` | Inside **mockups** (phone UI status bars, AI agent dashboards, dashboard widget chrome) where mimicking real device chrome is the point |

If you find yourself reaching for these on a card description, lead paragraph, bullet, or tagline, **stop** — use Normal (text-2xl) instead.

## How H2/Lead "looks smaller" than H1

H1 (text-5xl, 48px) and Normal (text-2xl, 24px) have a 2× ratio. That's enough to read as "headline vs body" without needing a 4× ratio. If a lead paragraph feels weak, increase **vertical spacing** above it (`mt-8` not `mt-3`) or use a slightly heavier weight — don't bump the font size.

## Example slide sized correctly

```tsx
<SlideShell number={N} total={totalSlides} label="Looking For">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>Looking For</Kicker>                                {/* Small (built-in) */}
  <h2 className="text-5xl font-bold text-gray-900 leading-tight">  {/* H1 */}
    ลูกค้าที่อยากให้ <span className="text-amber-500">refer มา</span>
  </h2>
  <p className="mt-8 text-2xl text-gray-600 leading-relaxed max-w-3xl">  {/* H2 — lead */}
    ใครก็ตามที่กำลังคิดเรื่องเหล่านี้ ส่งมาให้เติ้ลได้เลย
  </p>
  <div className="mt-12 grid grid-cols-2 gap-6">
    {items.map((p) => (
      <div key={p.title} className="p-7 rounded-2xl border bg-white flex gap-5">
        <Icon className="w-16 h-16 ..." />
        <div>
          <h3 className="text-2xl font-bold text-gray-900">{p.title}</h3>     {/* Normal */}
          <p className="text-2xl text-gray-700 mt-2 leading-relaxed">{p.desc}</p>  {/* Normal */}
        </div>
      </div>
    ))}
  </div>
</SlideShell>
```

Two sizes on the slide: text-5xl (H1) and text-2xl (everything else, including card titles + body). Plus the Kicker for the eyebrow label.

## Quick audit script

```bash
DECK=src/app/presentation/<slug>/<slug>-deck.tsx

# 1. Forbidden sizes outside mockup chrome
#    (text-base/sm/xs/lg/xl/3xl/4xl/6xl/7xl/8xl/9xl)
grep -nE 'text-(base|sm|lg|xl|3xl|4xl|6xl|7xl|8xl|9xl)\b' "$DECK"

# 2. Duplicate-class trap
grep -nE 'text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)[^"]*text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)\b' "$DECK"

# 3. Responsive prefixes (canvas mode forbids them)
grep -nE '(md|lg|sm):text-' "$DECK"
```

For (1), the only allowed matches should be inside known mockup blocks (phone UIs, dashboard widgets) and the SlideNumber/controls chrome. Everything else is a violation.
