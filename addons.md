# Optional add-ons

All opt-in. On every build ask **once** with a single `multiSelect` `AskUserQuestion` listing the ≤4 options relevant to the deck type (never one question per feature, never silently build them all). Build exactly what Tle ticks. Theme stays its own single-choice question.

```ts
{
  question: "เด็คนี้อยากได้ฟีเจอร์เสริมอะไรบ้าง? (เลือกได้หลายอัน)",
  header: "ฟีเจอร์เด็ค",
  multiSelect: true,
  options: [
    { label: "สารบัญเต็ม (TOC)", description: "หน้าสารบัญกดกระโดดได้ + ปุ่มเมนูทุกสไลด์ + drawer (กด M) — เหมาะเด็คยาว/สอน/อ้างอิง" },
    { label: "ปุ่มดาวน์โหลด PDF", description: "generate ไฟล์ PDF (1 สไลด์/หน้า) + ปุ่มดาวน์โหลด — เหมาะเด็คที่ต้องแจก/เก็บเป็นไฟล์" },
    { label: "Mockup จำลอง UI (แนะนำสำหรับเด็คสอน)", description: "ภาพจำลองหน้าจอเครื่องมือ (tag ภาพประกอบ) ในสไลด์สอนเครื่องมือ ให้ผู้เรียนเห็นภาพ" },
    { label: "Progress marker บน controller", description: "แบ่ง section/วัน บนแถบ dots ของ controller ให้รู้ตำแหน่ง เช่น เห็นว่าใกล้ถึงช่วงท้าย" },
  ],
}
```

Option sets: **Teaching / Workshop** → สารบัญ · PDF · Mockup (pre-recommend) · Progress marker. **BNI / Pitch / Conference** → สารบัญ · PDF · Live messages (+ one more if relevant). Mockups are documented in the gallery → "Illustrative mockups"; the other four are below.

---

## Progress markers (section ticks on the dot row)

For a long deck split into named sections (Day 1 / Day 2, Part 1 / Part 2, Week 6 / Week 8) the presenter wants a glanceable "how far in am I". This is deck **chrome** — a `DeckShell` prop, no slide change, **no PDF regen**:

```tsx
// 0-based index of each section's first slide
const SECTIONS = [
  { start: 0, label: "ที่มา" },
  { start: 5, label: "ผู้ซื้อ" },
  { start: 18, label: "กติกาแต้ม" },
] as const;

<DeckShell … sections={SECTIONS}>
```

The shell draws a thin tick + `text-[9px]` label before the first dot of each section after the first (chrome, so exempt from the 5-size scale). Keep ticks subtle — a notch, not a wall. Reference: `korat-points` (frozen copy of the same markup).

---

## PDF download (static, Playwright)

A **pre-generated static PDF**, one landscape page per slide, plus a download button. Chosen over `window.print()` because the deck is a transform-scaled canvas — the print dialog mangles it; screenshotting each slide gives clean uniform pages.

**Generate** — after the deck is final, with `pnpm dev` running (from the madebytle repo root):

```js
// _pdf.mjs
import { chromium } from "playwright";
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1920, height: 1200 }, deviceScaleFactor: 2 });
const p = await ctx.newPage();
await p.goto("http://localhost:3000/presentation/<slug>", { waitUntil: "networkidle" });
await p.waitForTimeout(1500);
// hide floating chrome so it doesn't bleed into the page
await p.addStyleTag({ content: `.absolute.top-4.left-4{display:none!important}.absolute.bottom-4{display:none!important}` });
await p.evaluate(() => { document.querySelector('[data-slide]').parentElement.style.scrollBehavior = 'auto'; });
const total = await p.evaluate(() => document.querySelectorAll('[data-slide]').length);
for (let i = 0; i < total; i++) {
  await p.evaluate((i) => { document.querySelector('[data-slide]').parentElement.scrollLeft = 1920 * i; }, i);
  await p.waitForTimeout(260);
  await p.screenshot({ path: `/tmp/pdf/s${String(i+1).padStart(3,"0")}.jpg`, type: "jpeg", quality: 82,
    clip: { x: 0, y: 0, width: 1920, height: 1080 } }); // clip = slide only (pill is below 1080)
}
await b.close();
```

```bash
magick /tmp/pdf/s*.jpg -quality 82 public/presentation/<slug>/<Name>.pdf   # 1 slide = 1 page
```

Viewport `1920×1200` + `deviceScaleFactor: 2` renders the canvas at scale 1, so the clip `{0,0,1920,1080}` is exactly one slide (the pill sits in the strip below y=1080). ImageMagick JPEG→PDF works even when PDF *reading* is policy-blocked.

**Button** — pass to `DeckShell`'s `extraTopLeft` (it renders inside `absolute top-4 left-4 z-40 flex items-center gap-2`, so a TOC button can sit beside it). Use the theme accent (`text-amber-600 hover:bg-amber-500` for MakeByTle):

```tsx
<a
  href="/presentation/<slug>/<Name>.pdf"
  download="<Name>.pdf"
  aria-label="ดาวน์โหลดเป็น PDF"
  title="ดาวน์โหลด PDF"
  className="flex items-center gap-2 rounded-full bg-white/95 backdrop-blur border border-gray-200 shadow-lg pl-3 pr-4 py-2 text-amber-600 hover:bg-amber-500 hover:text-white transition-colors"
>
  <ArrowDownTrayIcon className="w-5 h-5" aria-hidden="true" />
  <span className="text-sm font-semibold">PDF</span>
</a>
```

**The PDF is a snapshot — regenerate on every slide-content change, before each deploy.** Tell Tle; treat "edit deck → regen PDF → deploy" as one step. Chrome edits (pill, markers) need no regen.

---

## Table of Contents (สารบัญ)

Lets viewers **jump** instead of scrolling linearly. Worth it for 15+ slide, teaching and reference decks; short linear pitch/BNI decks usually don't need it. "Full" = all three pieces; "Agenda only" = piece 1.

1. **Agenda slide** (slide 2–3) — a normal `SlideShell` listing sections as clickable rows. It is slide *content*: stay on the 5-size scale (`text-2xl` rows, not `text-lg`). Add a hint "กดที่หัวข้อเพื่อกระโดดไปได้เลย".
2. **Floating "สารบัญ" button** — via `extraTopLeft` (viewport-pinned, outside the rotated canvas, so it stays upright in landscape). Top-left avoids the `SlideNumber` badge (top-right).
3. **Slide-out drawer** — sibling of `<DeckShell>`, gated on `tocOpen`: dimmed backdrop (click closes) + right panel with grouped sections and quick links, `z-50` (above the pill at `z-40`). `M` opens, `Esc` closes. Drawer and button are *chrome*: `text-sm`/`text-base`/`text-lg` are fine there.

**Data — one source of truth for jumps**, 1-based slide numbers matching `SlideShell number={N}`; largest `slide` must be ≤ `totalSlides`. Re-check after inserting/removing slides.

```tsx
const SECTIONS = [
  { group: "Part 1", groupNote: "…", items: [
    { no: 1, title: "หัวข้อแรก", slide: 5 },
    { no: 2, title: "หัวข้อสอง", slide: 9 },
  ]},
] as const;
const QUICK_LINKS = [{ label: "ภาพรวม", slide: 2 }, { label: "สรุป", slide: 30 }];
```

**Jump + keys** — `DeckShell` owns the rail and the nav handler, so the TOC drives the rail directly and shadows the shell's keys while open (capture-phase listener runs before the shell's bubble-phase one):

```tsx
const [tocOpen, setTocOpen] = useState(false);
const goTo = useCallback((slideNumber: number) => {
  setTocOpen(false);
  const rail = document.querySelector("[data-slide]")?.parentElement;
  rail?.scrollTo({ left: (slideNumber - 1) * BASE_W, behavior: "smooth" }); // canvas coords, like the shell
}, []);

useEffect(() => {
  const onKey = (e: KeyboardEvent) => {
    if (e.key === "Escape") { setTocOpen(false); return; }
    if (tocOpen) { e.stopPropagation(); return; }           // drawer open → shell nav/zoom keys don't fire; Tab/Enter move inside the drawer
    if (e.key === "m" || e.key === "M") setTocOpen(true);
  };
  window.addEventListener("keydown", onKey, true);           // capture phase
  return () => window.removeEventListener("keydown", onKey, true);
}, [tocOpen]);
```

Button + drawer markup:

```tsx
// extraTopLeft
<button type="button" onClick={() => setTocOpen(true)} aria-label="เปิดสารบัญ" title="สารบัญ (กด M)"
  className={`flex items-center gap-2 rounded-full bg-white/95 backdrop-blur border ${theme.border} shadow-lg pl-3 pr-4 py-2 ${theme.accent} hover:${theme.accentBg} transition-colors`}>
  <Bars3Icon className="w-5 h-5" aria-hidden="true" />
  <span className="text-sm font-semibold">สารบัญ</span>
</button>

// sibling of <DeckShell>
{tocOpen && (
  <div className="fixed inset-0 z-50 flex">
    <button type="button" aria-label="ปิดสารบัญ" onClick={() => setTocOpen(false)} className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" />
    <div className="relative ml-auto h-full w-full max-w-2xl bg-white shadow-2xl flex flex-col">
      <div className="flex items-center justify-between px-8 py-6 border-b border-slate-100">
        <div>
          <p className={`text-[11px] tracking-[0.3em] uppercase ${theme.kicker} font-semibold`}>สารบัญ · Agenda</p>
          <p className="text-2xl font-bold text-slate-900 mt-1">{deckTitle}</p>
        </div>
        <button type="button" onClick={() => setTocOpen(false)} aria-label="ปิด" className="w-11 h-11 rounded-full hover:bg-slate-100 flex items-center justify-center text-slate-500">
          <XMarkIcon className="w-6 h-6" aria-hidden="true" />
        </button>
      </div>
      <div className="flex-1 overflow-y-auto px-8 py-6">
        {SECTIONS.map((g) => (
          <div key={g.group} className="mb-8">
            <p className={`text-lg font-bold ${theme.accent} mb-3`}>{g.group}</p>
            <div className="space-y-1.5">
              {g.items.map((m) => (
                <button key={m.no} type="button" onClick={() => goTo(m.slide)} className="w-full flex items-center gap-4 rounded-xl px-4 py-3 text-left hover:bg-slate-50">
                  <span className="w-9 h-9 shrink-0 rounded-lg bg-slate-50 border border-slate-200 text-sm font-bold flex items-center justify-center tabular-nums">{m.no}</span>
                  <span className="flex-1 text-lg text-slate-800 leading-snug">{m.title}</span>
                </button>
              ))}
            </div>
          </div>
        ))}
        <div className="border-t border-slate-100 pt-5 grid grid-cols-2 gap-2">
          {QUICK_LINKS.map((q) => (
            <button key={q.label} type="button" onClick={() => goTo(q.slide)} className="rounded-xl border border-slate-200 px-4 py-3 text-left text-base text-slate-700 hover:border-slate-300 transition-colors">{q.label}</button>
          ))}
        </div>
      </div>
    </div>
  </div>
)}
```

Every jump button needs readable text or `aria-label`. Never put the button or drawer inside a `SlideShell`.

---

## Live audience messages (cover QR + bottom-left ticker)

Two surfaces for a live room: a **QR badge on the cover** (scan → comment form) and a **bottom-left ticker** on every other slide that shows the small QR when idle and flips to live messages (up to `MAX_VISIBLE = 3`, each fading after `VISIBLE_DURATION_MS = 12_000` with a 600ms fade) as they arrive. Keywords: "live messages", "comment ticker", "audience interaction", "ส่งข้อความขึ้นจอ".

**Reference implementation** (frozen, keep as the canonical pattern): `bni-5min/comment-ticker.tsx`, `bni-5min/comment-qr.ts`, `bni-5min/comment/`.

```
audience phone  /<slug>/comment  ──insert──►  Supabase Postgres  <slug>_comments
                                                   │ realtime INSERT (postgres_changes)
                                                   ▼
                                      <CommentTicker>  bottom-left of every slide
```

- **Table**: `id uuid pk default gen_random_uuid()`, `name text`, `message text`, `created_at timestamptz default now()`; realtime publication on; RLS = insert + select for the anon role on this table only.
- **Form page** `/<slug>/comment`: `'use client'`, name (≤30, optional) + message (≤200, required), server action validates and inserts; **rate-limit per IP** (e.g. one message / 30s) — a hostile attendee can otherwise spam the wall mid-talk. No login.
- **QR**: rendered server-side with the `qrcode` package (`type: "svg"`, `errorCorrectionLevel: "M"`, `margin: 1`, dark `#111827` on transparent) and passed to the deck as an SVG string.
- **Files**: `comment-qr.ts` (exports `LIVE_MESSAGES_ENABLED = false`, `COMMENT_URL`, `getCommentQrSvg()`), `comment-ticker.tsx`, `comment/page.tsx`, `comment/comment-form.tsx`. `page.tsx` and `[slug]/page.tsx` call `getCommentQrSvg()` only when the flag is on and pass `commentQrSvg` + `commentUrl` to the deck.
- **Env**: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` (anon key used for both the insert and the realtime subscription).
- **Ticker**: viewport-pinned (sibling of `<DeckShell>`, never inside the canvas — must stay upright in landscape), `aria-live="polite"`, `pointer-events-none`; clears timeouts and `removeChannel` on unmount; the idle/active faces flip with a small `rotateX`. Hide it on the cover (the cover already has the big QR) — with `DeckShell` the deck doesn't see `active`, so derive it from the synced URL (`location.pathname` ends with the cover slug) or reuse the frozen `bni-5min` deck pattern.
- Don't ship with `LIVE_MESSAGES_ENABLED = true` until table + RLS + rate limiter exist. The flag is the off-switch; the core deck never depends on this feature.
