# Illustrated decks — the "picture on almost every slide" pattern

> **Benchmark:** `korat-points` (1 ต.ค. 2569). Tle: *"นี่ถือเป็นสไลด์ที่ดีที่สุดที่เราทำมา"*
> Source: `madebytle/src/app/presentation/korat-points/korat-points-deck.tsx` — read it before building a deck of this kind. Adapt, don't re-derive.

Tle's standing preference, said mid-build: **"อัดรูปเยอะ ๆ หน่อย คนชอบดูรูปมากกว่าชอบอ่านข้อความ"**
Default to this pattern for any deck shown to clients, partners or a non-technical audience. A text-only slide is the exception and needs a reason (a rules table, a UI mockup).

What made the benchmark work, in order of impact:

1. A generated illustration on ~3 of every 4 slides (16 images for 21 slides); the rest are UI mockups or one dense table.
2. Text cut to what fits beside a picture — one idea per card, 1–2 lines each.
3. A status tag on every number or rule, so the audience can tell decided from proposed.
4. One brand palette shared by slides *and* illustrations.
5. Plain, concrete Thai copy with no filler.

---

## 1. Plan images before writing slides

Draft the slide outline, then list one image per slide **before** writing JSX. Ordering images after the layout exists means rebuilding the layout (it happened: 11 slides were rewritten).

- **Count:** aim for an image on every slide that is not a mockup or a table.
- **Size:** always `exactly 1024 x 1024 pixels, a perfect SQUARE`. Every layout below places a square. Do not order 16:9 and crop.
- **Background baked in:** ask for a solid flat background equal to the surface the image sits on, so there is no visible box and no transparency keying:
  - light slides → the theme's soft surface (`#F4F7FB` in Korat City Show), shown in a `rounded-3xl` frame
  - dark cover/closing → the dark slide color itself (`#002760`), outline color switched to white
- **Palette:** pass the theme's hex values as `Palette STRICTLY`, plus one skin tone and one hair color — the brand palette has neither, and without them people come out blue.
- **People:** state ethnicity explicitly when Tle asks (e.g. `All people are Thai / Southeast Asian with black hair`).
- **No text in images:** `every sign, screen, paper, sticker and label must be a blank shape`. All wording lives in HTML.
- **Counts as digits:** `EXACTLY three coins`, `ONE gift box`.

### Run generation in the background

Images take ~2 minutes each and the ChatGPT pane handles one at a time. Spawn **one** background `general-purpose` agent with the full list and the `kiki-gpt` procedure, then write the deck while it works. Brief it to:

- send one prompt at a time, confirm the pane enters `working`, wait for done
- check every result with `magick identify` and by looking at it (no text, square, flat background, people as specified); max 2 retries
- copy accepted files to `madebytle/public/presentation/<slug>/<name>.png`
- say `Generate ONE NEW illustration` from the second prompt on, or Codex may reuse the previous image
- pick a file name that does not already exist in `~gpt-generated-images/` (an old `…-cover.png` was nearly overwritten)

Need more images later? `SendMessage` the same agent with the extra list instead of spawning a second one — two agents would fight over the single pane. Tell Tle the wait: ≈2 min × images.

When the agent reports, **look at the images yourself** (a `magick … +append` contact sheet is enough) before deploying.

---

## 2. Layout: picture + short text

`Art` primitive — one place for the image markup:

```tsx
const IMG = "/presentation/<slug>";
function Art({ name, alt, className = "" }: { name: string; alt: string; className?: string }) {
  return (
    <Image src={`${IMG}/${name}.png`} alt={alt} width={1024} height={1024}
      className={`w-full h-auto rounded-3xl ${className}`} />
  );
}
```

### T15 · `illustrated-split` — the workhorse

Square art in `col-span-4` (≈510 canvas-px), content in `col-span-8`, columns stretched to the same height.

```tsx
<SlideShell number={N} total={totalSlides} label="…">
  <SlideNumber current={N} total={totalSlides} />
  <Kicker>{kicker}</Kicker>
  <H1>{heading}</H1>
  <div className="mt-10 grid grid-cols-12 gap-8 items-stretch">
    <div className="col-span-4"><Art name="…" alt="ภาพประกอบ: …" /></div>
    <div className="col-span-8 flex flex-col gap-4">
      {rows.map((r) => (
        <div key={r.title} className={`flex-1 flex items-center gap-6 px-7 py-5 rounded-2xl border ${theme.card}`}>
          {/* icon · title (bold) · one-line desc */}
        </div>
      ))}
    </div>
  </div>
</SlideShell>
```

Rules learned the hard way:

- **`items-stretch` + `flex-1` on the rows.** With `items-start` the text column ends ~100px above the image and the slide looks unfinished.
- **Height budget:** heading block ≈130 + `mt-10` 40 + image 510 = content ends ≈776. That leaves room for **one** single-line bar underneath (`mt-6`, ≈82px). A heading + lead + image + bar does not fit — drop the bar or fold its sentence into the lead.
- **Variants:** art on the right for lists that read left-to-right (timeline, numbered decisions); `grid-cols-3` with art as one of three equal columns for a two-way comparison; art + a 2×2 card grid for four parallel items.
- **Cover / closing:** dark slide, `col-span-7` text + `col-span-5` art, two small sparkle motifs.
- The image keeps its aspect before it loads because `width`/`height` are set — the safe-area audit is valid even while images are still generating.

### Replace a sentence with a shape when it compares numbers

"100,000 บาท ที่ 0.25 หรือ 200,000 บาท ที่ 0.50" became two bars with the amount beside each. Put `whitespace-nowrap shrink-0` on the amount label or it wraps.

---

## 3. Status tags — say what is decided

Any slide that shows a rule, number or term carries a tag. This is what let the audience trust the deck: nothing proposed was dressed up as agreed.

```tsx
type Status = "locked" | "proposal" | "open";
function Tag({ status }: { status: Status }) {
  const map = {
    locked:   { label: "ล็อกแล้ว", cls: theme.accentBg },
    proposal: { label: "ข้อเสนอ",  cls: theme.yellowBg },
    open:     { label: "รอเคาะ",   cls: `bg-white border-2 ${theme.border} ${theme.text}` },
  } as const;
  const t = map[status];
  return <span className={`inline-block shrink-0 rounded-full px-4 py-1 text-2xl font-semibold whitespace-nowrap ${t.cls}`}>{t.label}</span>;
}
```

- Tag a whole slide by putting it beside the H1 (`flex items-center gap-5`).
- Mockups get `ภาพประกอบ · ตัวเลขสมมติ` in the frame header whenever they show numbers.
- Prices and percentages Tle has not given: write "ตามใบเสนอราคา" / "สัดส่วนตกลงร่วมกัน" with a `รอเคาะ` tag. **Never invent a price.** Ask once; "ยังไม่ใส่" is a valid answer.

---

## 4. Copy — no slop

Tle asked explicitly: *"ระวังข้อความที่เป็น slop"*.

- Headline = the claim of the slide in plain words, not a topic label. "ส่งสลิปในแชต แต้มเข้าโดยไม่ต้องรอคนตรวจ", not "ระบบตรวจสอบสลิปอัจฉริยะ".
- Concrete nouns and numbers from the source material. No "ยกระดับ / ครบวงจร / ไร้รอยต่อ / ขับเคลื่อน".
- One idea per card. If a card needs a third line, cut it or split the slide.
- Say the awkward thing plainly when it is true ("เวลา 1 เดือนกับงาน 4 ส่วนตึงมาก").
- Thai words for the audience; keep English only for names they already use (LINE, Voucher, QR).
- Verify outside facts before putting them on a slide (a LINE platform claim was checked against LINE's docs first).

---

## 5. Build notes specific to this pattern

- **Custom brand theme:** put the brand hex values in the `theme` object only (`bg-[#104C92]` etc.) and nowhere else in the deck. Add dark-slide tokens (`darkBg`, `darkText`, `darkMuted`, `darkKicker`, `darkFrameOutline`) and give `SlideShell`, `Kicker`, `SlideNumber` a `tone="light" | "dark"` prop. See "Preset 7 — Korat City Show" in `themes.md`.
- **Do not redraw a client's logo.** If the brand file says the wordmark needs the owner's asset, use the palette only and tell Tle.
- **Audit without chrome-devtools:** Playwright resolves from `/Users/tlej/node_modules/playwright/index.mjs`. A script at 1920×1200 viewport that scrolls the rail, measures the lowest element per slide (must be ≤ 920) and screenshots each slide replaces the chrome-devtools audit. Tile the screenshots 2×2 with `magick` to review four slides per look.
- **Port 3000 is usually taken** by another project — run `next dev -p 3137`.
- **Final check on the production build:** `pnpm build`, `next start -p 3137`, re-run the audit, then capture the PDF from that server. A long-running background dev server gets killed at its time limit.
- **Mockup chips:** render the enabled and disabled states as two separate elements, not one element with a class ternary — the design-lint hook reads both class sets on one line as "gray text on a colored background".
- After deploy, add the deck link and update steps to the client project's `docs/presentation/README.md`.
