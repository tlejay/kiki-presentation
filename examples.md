# Reference Decks

Working decks built with this skill. Open these when you need a concrete example of templates applied end-to-end.

## bni-5min — เติ้ล AI (BNI presentation)

- **URL**: https://madebytle.com/presentation/bni-5min
- **Source**: `/Users/tlej/Works (Local)/Vibe Docs/00 Madebytle Profile/madebytle/src/app/presentation/bni-5min/`
  - `layout.tsx` — Metadata + light wrapper
  - `page.tsx` — Re-export
  - `bni-5min-deck.tsx` — Full 15-slide deck (~600 lines)
- **Theme**: MakeByTle (white + amber)
- **Audience**: BNI (full 15-slide structure)
- **What it demonstrates**:
  - All 12 slide templates (T01–T12) applied with the MakeByTle theme
  - Horizontal scroll-snap container + keyboard navigation (← → Space Home End)
  - Slide indicator dots + prev/next nav pill
  - Heroicons usage throughout (no emoji)
  - Thai-aware kicker spacing (mb-10 + pt-2 + leading-[1.05] on huge headings)
  - Number formatting (`100+`, `30+`, `80+`)
  - Contact cards with `mailto:` and `tel:` href

When you start a new BNI deck, **read this file first** to see how the patterns compose. Don't re-derive — adapt.

## korat-points — KORAT POINTS (client working session) · BENCHMARK

- **URL**: https://madebytle.com/presentation/korat-points
- **Source**: `/Users/tlej/Works (Local)/Vibe Docs/00 Madebytle Profile/madebytle/src/app/presentation/korat-points/`
- **Theme**: Korat City Show (v1 custom brand palette)
- **Audience**: working session with a partner team (ทีมมีดี) ahead of a chamber-of-commerce pitch
- **Tle's verdict (1 ต.ค. 2569)**: "นี่ถือเป็นสไลด์ที่ดีที่สุดที่เราทำมา"
- **What it demonstrates**:
  - 16 generated illustrations across 21 slides, all square, palette-matched, background baked in
  - `Art` + `illustrated-split` layouts (art left, art right, art as one of three columns, art + 2×2 cards)
  - `Tag` status pills (ล็อกแล้ว / ข้อเสนอ / รอเคาะ) on every rule and number
  - LINE chat / rewards phone mockups and two dashboard mockups labelled "ภาพประกอบ · ตัวเลขสมมติ"
  - light + dark `tone` on `SlideShell`, section markers on the dot row, PDF download, presenter zoom
  - commercial terms shown as principles with no invented prices

Start here for any client-facing deck. Pattern notes: [`illustrated-decks.md`](./illustrated-decks.md).

## cinematic-demo — v3 template showcase (photo-led) · TEST BED

- **URL**: `/presentation/cinematic-demo` (dev). Not a client deck — sample content, every number illustrative.
- **Source**: `/Users/tlej/Works (Local)/Vibe Docs/00 Madebytle Profile/madebytle/src/app/presentation/cinematic-demo/`
- **Theme**: The Standard (v3)
- **What it demonstrates**: all ten v3 templates (C01–C10) in order — split overview with medallion, section divider, logo hero, host profile with a cut-out, programme detail with an outlined cut-out + vertical thumbnail rail, numbered format steps with phone mockups, vertical-media pitch with highlight strips, action title, concept + samples, closing. Reuses the `bni-5min` photos; `host.png` was made with `scripts/cutout.swift`.

Start here for any v3 deck, and add new v3 templates here first. Pattern notes: [`slide-templates-v3.md`](./slide-templates-v3.md).

## How to add a new reference

When you finish a presentation deck for Tle:

1. Add a section here with: URL, source path, theme, audience, what it demonstrates.
2. Sort by audience type (BNI first, then pitch, then internal, etc.).
3. Keep the section short — link, don't duplicate. The deck file itself is the canonical example.
