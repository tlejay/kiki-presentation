# kiki-presentation

A [Claude Code](https://docs.anthropic.com/claude/docs/claude-code) skill that builds web-based presentation decks from any project directory and deploys them as Next.js pages under `madebytle.com/presentation/<slug>`.

Built by [Tle](https://madebytle.com) — a PM-turned-product-builder who vibe codes everything with Claude Code.

## What it does

1. **Scans the current project** (`CLAUDE.md`, `README.md`, `package.json`) for slug, title, tagline.
2. **Asks via `AskUserQuestion`**: audience, template version (v1 MakeByTle / v2 Kevents / v3 The Standard), theme (8 presets or custom), optional features (one multi-select), remaining content.
3. **Writes a React deck** into the MakeByTle.com Next.js app: slides from the chosen gallery inside the shared `DeckShell` chrome (`src/app/presentation/_shared/deck-shell.tsx`), per-slide deep-link routes.
4. **Audits** (safe area, typography greps, tsc / lint / build), optionally generates a PDF, then **deploys** with `vercel deploy --prod --yes` and verifies the live URL.

Triggers: "ทำ presentation" / "ทำสไลด์" / "พรีเซน" / "make slides" / "build a deck".

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Entry point — inputs, file layout, the 8-step checklist workflow |
| `canvas-shell.md` | What `DeckShell` provides, its props, locked numbers (1920×1080, 96px strip, y ≤ 920) |
| `checklist.md` | Design rules + "deck complete?" gate |
| `slide-templates-v1.md` | Gallery v1 — MakeByTle style (T01–T15) + layout principles |
| `slide-templates-v2.md` | Gallery v2 — Kevents brand (K01–K24, SignatureMotif, 3-tier backgrounds) |
| `slide-templates-v3.md` | Gallery v3 — The Standard (C01–C10, full-bleed photo + scrim, cut-outs) |
| `scripts/cutout.swift` | Lifts the main subject out of a photo into a transparent PNG (Apple Vision, macOS 14+) |
| `themes.md` | Theme presets 1–8 + custom synthesis |
| `typography.md` | 5-size type scale and font rules |
| `addons.md` | Optional features: progress markers, PDF, TOC, live audience messages |
| `illustrated-decks.md` | Picture-led client decks (`/kiki-gpt` illustrations, status tags, copy rules) |
| `bni-structure.md` | 15-slide BNI 5-minute structure |

## Conventions

- All decks live under `madebytle/src/app/presentation/<slug>/`; chrome is shared via `DeckShell`, slides are per-deck (`SlideShell`, `Kicker`/`CapsLabel`, `SlideNumber`, `theme`).
- Themes follow a strict token shape (`bg`, `text`, `accent`, `frameOutline`, …) — see `themes.md`.
- **Templates evolve, decks freeze** — galleries and `DeckShell` are upgraded in place; shipped decks are never rewritten.

## Reference decks

| Deck | URL / source | Theme · version | Why look at it |
|------|--------------|-----------------|----------------|
| **bni-5min** | madebytle.com/presentation/bni-5min · `src/app/presentation/bni-5min/` | MakeByTle · v1 | 15-slide BNI structure, T01–T12 applied, Thai-aware kicker spacing, contact cards with `mailto:`/`tel:`. Also the live-messages reference (`comment-ticker.tsx`). Frozen — carries its own chrome |
| **korat-points** · BENCHMARK | madebytle.com/presentation/korat-points · `src/app/presentation/korat-points/` | Korat City Show · v1 | 16 generated illustrations across 21 slides, `illustrated-split` layouts, `Tag` status pills (ล็อกแล้ว / ข้อเสนอ / รอเคาะ), phone + dashboard mockups labelled "ภาพประกอบ · ตัวเลขสมมติ", light/dark `tone`, section markers, PDF, no invented prices. **Tle (1 ต.ค. 2569): "นี่ถือเป็นสไลด์ที่ดีที่สุดที่เราทำมา"** — start here for any client deck. Frozen chrome |
| **cinematic-demo** | `/presentation/cinematic-demo` · `src/app/presentation/cinematic-demo/` | The Standard · v3 | All ten v3 templates C01–C10 in order; `host.png` made with `scripts/cutout.swift`; sample content, every number illustrative. **First deck on `DeckShell`** — add new v3 templates here first |
| **hare-and-tortoise** | `/presentation/hare-and-tortoise` · `src/app/presentation/hare-and-tortoise/` | The Standard · v3 | 5-slide fable on v3; smallest working `DeckShell` deck — the template for a new deck's skeleton |

When you finish a deck for Tle, add a row: URL, source, theme · version, what it demonstrates, Tle's verdict if he gave one. Link, don't duplicate — the deck file is the canonical example.

## Install

```bash
git clone https://github.com/tlejay/kiki-presentation.git ~/.claude/skills/kiki-presentation
```

Invoke with `/kiki-presentation` or by asking Claude to build a presentation in any project.

## License

MIT — see [LICENSE](./LICENSE).
