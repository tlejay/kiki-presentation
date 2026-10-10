# kiki-presentation

A [Claude Code](https://docs.anthropic.com/claude/docs/claude-code) skill that builds web-based presentation decks from any project directory, then deploys them as Next.js pages under `madebytle.com/presentation/<project-slug>`.

Built by [Tle](https://madebytle.com) — a PM-turned-product-builder who vibe codes everything with Claude Code.

## What it does

When invoked, the skill:

1. **Scans the current project** for context — reads `CLAUDE.md`, `package.json`, `README.md`, recent git history, source files.
2. **Asks the user** via `AskUserQuestion`:
   - Who is the audience?
   - Which visual theme to apply (10 presets or generate on-the-fly)?
   - What content angle? (pitch, retrospective, walkthrough, etc.)
3. **Generates a React deck** following the chosen template gallery — `slide-templates-v1.md` (MakeByTle style), `slide-templates-v2.md` (Kevents brand) or `slide-templates-v3.md` (The Standard, photo-led), picked in SKILL.md Step 3a.
4. **Writes the deck into the MakeByTle.com Next.js app** at the right route.
5. **Verifies locally** by running the dev server and listing the new route.

## When to use

Trigger this skill when the user says any of:

- "ทำ presentation" / "ทำสไลด์" / "พรีเซน"
- "make a presentation" / "create slides" / "build a deck"

The skill works from inside any project directory — it auto-detects the project name and slug.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill entry point and workflow |
| `slide-templates-v1.md` | React template gallery — v1, MakeByTle style (clean, single background) |
| `slide-templates-v2.md` | React template gallery — v2, Kevents brand (gradient, glass, 3-tier backgrounds + signature motif) |
| `slide-templates-v3.md` | React template gallery — v3, The Standard (full-bleed photo + scrim, white type, brand chrome, phone/thumbnail/cut-out media) |
| `scripts/cutout.swift` | Lifts the main subject out of a photo into a transparent PNG (Apple Vision, macOS 14+) — for v3 cut-out slides |
| `themes.md` | Visual theme presets (incl. Kevents for v2, The Standard for v3) + custom theme synthesis |
| `typography.md` | Type-pairing rules and Tailwind tokens |
| `checklist.md` | Pre-deploy quality checklist |
| `toc.md` | Table-of-Contents add-on (Agenda slide + floating menu + jump overlay) — always offered via AskUserQuestion |
| `live-messages.md` | Status messages the skill prints during execution |
| `bni-structure.md` | Alternate 5-minute BNI presentation structure |
| `examples.md` | Sample slugs and parameter examples |

## Project conventions

- All decks live under `madebytle.com/src/app/presentation/<slug>/`
- Each deck uses the shared `<SlideShell>` / `<SlideKicker>` primitives from the main site
- Themes follow a strict token shape (`bg`, `fg`, `accent`, `frameOutline`, etc.) — see `themes.md`
- Presenter notes are placed inside `<aside data-presenter-note>` blocks so they don't render in the audience view

## Install

This is a Claude Code [user-level skill](https://docs.anthropic.com/claude/docs/claude-code/skills). To install:

```bash
git clone https://github.com/tlejay/kiki-presentation.git ~/.claude/skills/kiki-presentation
```

Then invoke from Claude Code with `/kiki-presentation` or by asking Claude to build a presentation in any project.

## License

MIT — see [LICENSE](./LICENSE).
