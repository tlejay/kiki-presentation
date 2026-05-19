# Reference Decks

Working decks built with this skill. Open these when you need a concrete example of templates applied end-to-end.

## bni-5min — เติ้ล AI (BNI presentation)

- **URL**: https://madebytle.com/presentation/bni-5min
- **Source**: `/Users/tlej/Works (Local)/Vibe Docs/00 Made by Tle/madebytle/src/app/presentation/bni-5min/`
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

## How to add a new reference

When you finish a presentation deck for Tle:

1. Add a section here with: URL, source path, theme, audience, what it demonstrates.
2. Sort by audience type (BNI first, then pitch, then internal, etc.).
3. Keep the section short — link, don't duplicate. The deck file itself is the canonical example.
