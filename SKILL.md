---
name: kiki-presentation
description: "Build and deploy a web slide deck to madebytle.com/presentation/<slug> from any project. Triggers: ทำ presentation, ทำสไลด์, พรีเซน, make slides, build a deck. Asks audience, template version, theme, features."
---

# kiki-presentation — Web Presentation Builder

> Anywhere you're working, "make me a presentation" → a deployed web deck under `madebytle.com/presentation/<slug>`.

The current project provides *content*; the deck **always** lives in the MakeByTle.com Next.js repo. One React component per deck: Tailwind + Heroicons + Noto Sans Thai, a 1920×1080 canvas inside the shared [`DeckShell`](./canvas-shell.md), horizontal scroll-snap, keyboard nav, per-slide URLs. Opens on any device including a TV/projector.

## Inputs (confirm via `AskUserQuestion` — never plain-text questions)

| # | Input | Source |
|---|-------|--------|
| 1 | Slug | suggest from current dir name; Tle confirms |
| 2 | Audience | BNI / Pitch / Handover / Conference / Teaching / Custom — drives slide selection |
| 3 | Template version | v1 / v2 / v3 ("The Standard") — drives valid themes |
| 4 | Theme | always ask, even when defaulting ([`themes.md`](./themes.md)) |
| 5 | Optional features | ONE `multiSelect` question, ≤4 options ([`addons.md`](./addons.md)) |
| 6 | Title + tagline | from `CLAUDE.md` / `README.md`; confirm |
| 7 | Services / sections | project-dependent |
| 8 | Looking for · Trigger words | BNI only |
| 9 | Contact | Tle's standard (email/phone/web); confirm |

## File layout

```
/Users/tlej/Works (Local)/Vibe Docs/00 Madebytle Profile/madebytle/src/app/presentation/<slug>/
├── layout.tsx        # metadata (title, description, OG, robots noindex) + bg wrapper (bg-white; v3 bg-neutral-950)
├── page.tsx          # <Deck /> at /<slug> (slide 1)
├── slide-slugs.ts    # SLIDE_SLUGS, SLIDE_TITLES, BASE_PATH — NOT "use client" (server route imports it)
├── [slug]/page.tsx   # generateStaticParams + generateMetadata → <Deck initialSlide={index} />, notFound() on unknown
└── <slug>-deck.tsx   # "use client"; imports DeckShell; theme + primitives + slides
```

URLs: `https://madebytle.com/presentation/<slug>` and `…/<slug>/<slide-slug>` (real path segments, not `#hash` — people share and comment by slide). Dev: `http://localhost:3000/presentation/<slug>`.

## Workflow (checklist — walk every box)

### 1 · Scan (no questions yet)
- [ ] `pwd; ls; cat CLAUDE.md README.md; head -30 package.json` — suggest slug/title/tagline; don't ask for facts visible in the repo.

### 2 · Ask (batch; cap 4 questions per turn)
- [ ] **Audience** → structure:
  - BNI 5-min → 15 slides, [`bni-structure.md`](./bni-structure.md)
  - Pitch → Cover, Problem, Solution, Market, Demo, Traction, Business Model, Team, Ask, Closing
  - Handover / internal demo → Cover, Context, What We Built, Demo, Tech Stack, Results, Next Steps, Closing
  - Conference → Cover, Hook, 3–5 Sections, Closing/CTA
  - Teaching / Workshop → see below
  - Custom → ask for an outline
- [ ] **Version** (skip if Tle says "template The Standard" → v3):
  - **v1 — MakeByTle** [`slide-templates-v1.md`](./slide-templates-v1.md): clean single background; the proven default.
  - **v2 — Kevents** [`slide-templates-v2.md`](./slide-templates-v2.md): indigo→purple→pink gradient, glass, 3-tier backgrounds, signature motif, activity/divider archetypes. Kevents / community / event decks.
  - **v3 — The Standard · photo-led** [`slide-templates-v3.md`](./slide-templates-v3.md): full-bleed photo + scrim, white type, one accent per programme, real media (phones, thumbnails, cut-outs). Media / sponsorship / venue / portfolio decks. **Needs photographs** — ask where they are, read the v3 "Photos" section first. Not for teaching or text-heavy decks. Reference: `cinematic-demo`.
- [ ] **Theme** — offer only presets valid for the version: v1 → MakeByTle · Premium Dark · Gradient AI · Editorial Minimal (or Custom; Korat City Show for Korat decks); v2 → Kevents only; v3 → The Standard only — ask instead which **accent** each programme gets (coral / amber / magenta / lilac / client palette). Never pair a v1 theme with v2 (cover/divider silently fall back to plain content).
- [ ] **Features** — one `multiSelect` question, pick the ≤4 relevant options: Teaching → สารบัญ · PDF · Mockup (pre-recommend) · Progress marker; BNI / Pitch / Conference → สารบัญ · PDF · Live messages (+1). Build exactly what is ticked. Canonical form + build notes in [`addons.md`](./addons.md).
- [ ] **Content** the repo doesn't provide (title, sections, contact…).

**Teaching / Workshop decks (Tle's standing rule):** size for the teaching time — a full day (≈09:00–16:00) needs **25–30 slides per day**; multi-day → size each day and sum (two days ≈ 50–60). Confirm depth via `AskUserQuestion` first. More slides ≠ repetition: for every tool walk **pain → landscape → tool → connect**: (1) show the learner's current pain (a day-in-the-life), (2) survey the category (e.g. team chat: LINE / Messenger / Slack / Discord / MS Teams) and why you picked one, (3) one slide per capability with an **illustrative HTML mockup** tagged `ภาพประกอบ` (never describe a UI in words), per-use-case slides, an SME hack, a mini-recap, (4) a wrap-up per section/day showing how the pieces form one system. Open each section with a category-overview slide and a pain slide before the first tool slide. Mockup templates: gallery → "Illustrative mockups" (reference `aviationx-deck.tsx`).

### 3 · Plan the pictures (client / partner / non-technical decks)
- [ ] Tle: "อัดรูปเยอะ ๆ คนชอบดูรูปมากกว่าชอบอ่านข้อความ". Unless it is a pure mockup-based teaching deck, plan **one generated illustration per slide** (`/kiki-gpt`, square 1024, background baked in) right after the outline, before any JSX, and start generation in a background agent. Read [`illustrated-decks.md`](./illustrated-decks.md). Benchmark: `korat-points`. Never ship a client deck that is mostly text.

### 4 · Build
- [ ] Read the chosen gallery (primitives + every slide pattern) and [`typography.md`](./typography.md). Templates are read-only during a build.
- [ ] Write `slide-slugs.ts` (order must match the `SlideShell`s), `[slug]/page.tsx`, `page.tsx`, `layout.tsx`.
- [ ] `<slug>-deck.tsx`: `import DeckShell, { BASE_W, BASE_H } from "../_shared/deck-shell"`, copy `theme` + `SlideShell`/`Kicker`/`SlideNumber` from the gallery, then only slides inside `<DeckShell slugs basePath initialSlide sections? chrome? extraTopLeft?>`. Details and locked numbers: [`canvas-shell.md`](./canvas-shell.md). Never re-implement stage / pill / keyboard code.
- [ ] Every slide: `<SlideNumber current={N} total={totalSlides} />`, default `align="top"` (only Cover / LCD / Closing `center`), content ends at y ≤ 920.

### 5 · Audit (before reporting)
- [ ] `pnpm dev` in the madebytle repo, open `http://localhost:3000/presentation/<slug>`.
- [ ] Safe-area audit (chrome-devtools `evaluate_script` or Playwright) — screenshots alone miss content hidden under the pill:

```js
async () => {
  const slides = document.querySelectorAll('[data-slide]');
  const rail = slides[0].parentElement;
  const scale = slides[0].getBoundingClientRect().width / 1920;
  const cRect = document.querySelector('.absolute.bottom-4')?.getBoundingClientRect();
  const safetyZoneCanvasPx = ((window.innerHeight - (cRect?.top ?? window.innerHeight)) / scale);
  const failures = [];
  for (let i = 0; i < slides.length; i++) {
    rail.scrollTo({ left: 1920 * i, behavior: 'auto' });
    await new Promise(r => setTimeout(r, 200));
    const rect = slides[i].getBoundingClientRect();
    let maxBottom = 0, offender = null;
    slides[i].querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      if (el.tagName === 'IMG' && el.className.includes('-z-10')) return; // full-canvas backgrounds
      if (el.closest('[data-bleed],[data-fill]')) return;                  // v3 decorative layers
      const b = (r.bottom - rect.top) / scale;
      if (b > maxBottom) { maxBottom = b; offender = el.tagName + '.' + (el.className||'').split(' ').slice(0,2).join('.'); }
    });
    if (maxBottom > 1080 - safetyZoneCanvasPx) failures.push({ slide: i+1, bottomY: Math.round(maxBottom), offender: offender?.slice(0, 60) });
  }
  return { scale, safetyZoneCanvasPx: Math.round(safetyZoneCanvasPx), failures };
}
```

  Fix every failure. Usual culprits: fixed-height media `h-[480px]+` (→ `h-[400px]` or `aspect-[X/Y]`), `aspect-[4/3]` in `col-span-7+` (→ `aspect-[16/9]`), long Thai text in narrow cards (widen, `break-words`), tall-padded lists with multi-line text.
- [ ] Visual checks per slide: top-anchored unless hero · no disconnected bands · content fills ≥ ~75% of the 920px budget · 2-col heights balanced · no card overflow (`auto-rows-fr`) · Thai font renders · no kicker/heading overlap · no horizontal scrollbars.
- [ ] The three greps (only mockup chrome may match):

```bash
DECK=src/app/presentation/<slug>/<slug>-deck.tsx
grep -nE 'text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)[^"]*text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)' "$DECK"  # duplicate size classes
grep -nE '(md|lg|sm):(text-|grid-cols-|col-span-)' "$DECK"   # responsive prefixes inside slides
grep -nE 'text-xs|text-\[1[0-3]px\]|text-\[9px\]' "$DECK"    # tiny prose
```
- [ ] `npx tsc --noEmit` · `pnpm lint` · `pnpm build` (all `[slug]` routes prerender).
- [ ] Walk [`checklist.md`](./checklist.md) line by line; fix every flag.

### 6 · PDF (only if ticked)
- [ ] Generate per [`addons.md`](./addons.md) → "PDF". **A PDF is a snapshot — regenerate after every slide-content change, before every deploy** ("edit → regen → deploy" is one step). Chrome edits (pill, markers) need no regen.

### 7 · Ship
- [ ] Commit in the madebytle repo (deck files only).
- [ ] **`git push` does NOT publish madebytle.com** — the Vercel project is not linked to Git; pushing builds nothing and a new deck 404s. Always:

```bash
cd "/Users/tlej/Works (Local)/Vibe Docs/00 Madebytle Profile/madebytle"
vercel deploy --prod --yes
curl -s -o /dev/null -w "%{http_code}" https://madebytle.com/presentation/<slug>   # must be 200
```
  `vercel deploy` printing READY is not proof prod changed — the curl is.

### 8 · Report (Thai, short)
- [ ] URL (dev + prod) · files created · every `// TODO: confirm with Tle` guess · what was deployed. Deploy it, don't just suggest it.

## Standing rules

- **Templates evolve, decks freeze.** Galleries are the source of truth; when Tle asks to "upgrade the template", edit the gallery file (and `DeckShell` for chrome) — existing `<slug>-deck.tsx` files are frozen snapshots and stay untouched. Never modify a gallery as part of building a deck.
- Design rules (font, icons, colours, typography, layout, safe area, a11y) are enforced by [`checklist.md`](./checklist.md).

## Reference files

| File | When |
|------|------|
| [`canvas-shell.md`](./canvas-shell.md) | Step 4 — what `DeckShell` provides, props, locked numbers |
| [`checklist.md`](./checklist.md) | Step 5 — design rules + "deck complete?" gate |
| [`typography.md`](./typography.md) | before sizing any text — 5-size scale |
| [`themes.md`](./themes.md) | Step 2 theme — presets per version |
| [`slide-templates-v1.md`](./slide-templates-v1.md) · [`v2`](./slide-templates-v2.md) · [`v3`](./slide-templates-v3.md) | Step 4 — the chosen gallery (v3 also covers photo sourcing + `scripts/cutout.swift`) |
| [`addons.md`](./addons.md) | Step 2 features / Step 6 — TOC, PDF, progress markers, live messages |
| [`illustrated-decks.md`](./illustrated-decks.md) | Step 3 — picture-led client decks (`korat-points` pattern) |
| [`bni-structure.md`](./bni-structure.md) | audience = BNI |
| [`README.md`](./README.md) | reference decks + Tle's verdicts |

## Never

- ❌ Deploy a slide-content change on a deck that has a PDF without regenerating the PDF.
- ❌ Modify a gallery / template file while building a deck.
- ❌ Use emoji anywhere (icons, headings, labels, card text, mockups) — Heroicons or plain text; typographic arrows `→ ← ↔` are fine.
- ❌ Invent personal-branding content — mark guesses `// TODO: confirm with Tle`.
- ❌ Invent a price, percentage or date Tle has not given — state the principle and tag it `รอเคาะ`.
- ❌ Present a proposal as agreed — tag it `ข้อเสนอ`.
