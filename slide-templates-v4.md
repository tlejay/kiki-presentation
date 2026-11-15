# Gallery v4 — Cinematic Launch (standalone HTML)

Photo-led stage deck for **launches, client proposals and confidential talks**. Unlike v1–v3 it is **not** a madebytle.com React page: it is one self-contained `index.html` + `deck.css` that lives **inside the client project** (fonts, photos and screens bundled, works offline on the venue laptop, never public).

Reference decks (Tle approved both — "ทำออกมาดีมาก"):
- `138 Yellobe/docs/proposal/presentation.html` — client proposal, yellow accent
- `30 Happiness MLM/mlm-thehappiness/.presentation-work/claude/` — platform launch, two speakers, sky/orange accents (Nov 2569). Built after Codex shipped two rounds Tle rejected as "a user manual, not a launch".

Starter kit: [`templates/v4-cinematic/`](./templates/v4-cinematic/) — copy the whole folder into the project (`deck.css`, `index.html` with one slide per pattern, `build_md.py`, `build_pdf.py`, fonts).

## When to pick v4

| Pick v4 | Pick v1–v3 |
|---|---|
| Must stay private (client data, unreleased product, NDA) | Fine to publish on madebytle.com |
| Stage / projector talk, Tle or client presents | Shared as a link, people read it alone |
| Real product screens are the evidence | Mostly concepts or illustrations |
| Needs a PDF backup + speaker notes + `deck.md` brief | Web-only |

## The look (what made Tle say yes)

1. **One photo series for the whole deck.** Generate every background through `/kiki-gpt` as ONE series: same lens, same grade (deep navy shadows, one ambient brand colour, small warm practical lights), real local people/settings, **left 45–55% left dark and empty for type**, 16:9, no text. Generate the cover first, check it, then queue the rest with "match the look of <cover path>". Every slide gets **its own** photo. Reusing a photo (even flipped) is a flaw, except cover ↔ closing as bookends.
2. **Every photo carries a meaning**: a growing city network for scale, team leaders around a phone for "used for real", hands and receipts for accountability, a seller photographing a product for "open your shop". A generic pretty photo is a reject.
3. **One message per slide, with one highlighted phrase** (`.hl` strip in the accent colour). The headline is the slide, and the lead is at most 2 lines.
4. **Real screens are the evidence.** Real captures (390×844 @2x) go in the CSS phone frame `.dv`, desktop captures in `.bw`. To make a detail readable from the back row, use a **magnifier** `.zm` that crops a region of the same real screen. Never draw a fake UI. Footer says `หน้าจอจริง ข้อมูลสาธิต`.
5. **Accent = chapter.** Take accents from the logo. One per speaker or section (`.slide.mk` switches `--accent`), so the audience feels the hand-off.
6. **Rhythm, not template.** Alternate: full-bleed statement → giant number → 3-promise evidence row → phone flow → phone + magnifier → browser frames → process flow → product gallery → checklist CTA. Never use the same layout on 3 slides in a row.

## Patterns (all in the starter `index.html`)

| # | Pattern | Key classes |
|---|---|---|
| P1 | Cover: photo + `scrim l`, two tilted phones, speaker lockup | `.dv.l4/.r7`, `.who` |
| P2 | Full-bleed statement | `.bg` + `.scrim l` + `h1.l` |
| P3 | Giant proof number (only a fact Tle confirmed) | `.huge sup` |
| P4 | Three promises, each with a magnified real-screen crop | `.pr`, `.zm` |
| P5 | Flow: text left, 3 phones with `ขั้นที่ N` captions | `.col .dv .cap` |
| P6 | Phone + magnifier + numbered tags | `.dv`, `.zm`, `.tag` |
| P7 | Browser frames (back office, reports) | `.bw` (crop with `.zm` inside to hide sensitive panels) |
| P8 | Process / money flow over a photo, last node in accent | `.flow` |
| P9 | Real product gallery | `.gal` |
| P10 | CTA checklist | `.chk` |

`.zm` crop maths: screen is 780px wide; to show region (x, y) at scale k → `--sw: 780k px; --x: x·k px; --y: y·k px`, box size = region × k.

## Thai typography (hard rules, both from Tle's feedback)

- **Headline line-height ≥ 1.6** (`h1`, `h1.l`). Below that, upper vowels and tone marks (ซื้อ, ขึ้น, ทุก) collide with the highlight strip on the next line. `h1.xl` 1.16 is only for one-line or Latin titles. A Thai multi-line headline uses `.l`, not `.xl`.
- **No wide letter-spacing on Thai.** Spaced-out Thai kickers are unreadable. Thai kickers use `letter-spacing .03em`. Wide uppercase tracking only goes on Latin-only kickers (`.kick.en`).
- IBM Plex Sans Thai bundled as woff2 (no network at the venue).
- QA by eye at **110 dpi zoom on every slide with a highlight strip**, not just the contact sheet. The collision is invisible at thumbnail size; Tle spotted it on a phone screenshot.

## Evidence discipline

- Keep an evidence register in `deck.md`: ✅ what Tle confirmed, ✅ what the code or screens show, ❌ what must not be said (uptime, capacity, approval times, dates, income promises).
- Put the boundary inside the speaker note of the slide where it matters, e.g. `(ไม่อ้างตัวเลข…)`.
- Never invent numbers. Demo data only, and crop out anything that shows seeded people or fake revenue.

## Viewer & outputs

- Keys: `←/→` · `F` fullscreen · `N` speaker notes · `G` overview grid · URL `#n` deep link · swipe on touch.
- PDF backup: **`python3 build_pdf.py`**: screenshots every slide (`index.html?shot#n`, 2×) and joins them with `img2pdf` → `qa/deck.pdf` (~8 MB for 24 slides) + `qa/s-NN.png` thumbnails. Regenerate after every content change.
  - **Never use Chrome `--print-to-pdf` / `window.print()`.** It exports box-shadows/filters on rotated phones as transparency groups, which macOS Preview, Google Drive and LINE draw as **solid black boxes around the phones** (Tle hit this many times; Happiness deck, Nov 2569). It also made a 54 MB file. Screenshots are flat pixels, so every viewer shows what Chrome shows.
  - `?shot` hides the HUD and turns off the slide fade. Without it, the capture catches a half-dark slide.
  - Verify with macOS Quick Look, not Chrome: `qlmanage -t -s 1600 -o /tmp qa/deck.pdf`. Chrome's own PDF viewer hides the bug.
- `deck.md` = `python3 build_md.py` (head + per-slide brief/notes from the HTML + Q&A tail). Never hand-edit the per-slide part. Add `data-who="…"` per slide for the speaker column.
- Speaker notes live in `<aside class="note">` per slide. Timing goes in `data-time`. Two speakers × 15 min ≈ 12 slides each.

## Build order

1. Outline: story → one message per slide → which real screen or fact proves it. Get Tle's OK.
2. Cover photo through `/kiki-gpt` → check → queue the rest of the series in one message (≈1.5 min/photo).
3. Build the slides from the starter while photos render.
4. `build_pdf.py` → contact sheet → zoom check each slide (faces covered by phones? text over faces? strips colliding?) → fix → repeat.
5. `deck.md`, then report to Tle with the contact sheet image.
