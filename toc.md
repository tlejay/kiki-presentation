# Table of Contents (สารบัญ) — optional navigation add-on

A way to let viewers **jump** around a deck instead of only scrolling linearly. Most valuable for
long decks (15+ slides), teaching/training material, and reference decks people revisit. Short
pitch/BNI decks usually don't need it.

> **MANDATORY RULE — always ask first.**
> Never build a TOC silently, and never skip offering it. On **every** deck build, ask Tle via
> `AskUserQuestion` whether they want a TOC (canonical form below). Build it only if Tle says yes.
> This mirrors the "always ask theme" rule — the question is required, the feature is opt-in.

## The canonical AskUserQuestion (ask this every build)

```ts
{
  question: "ต้องการใส่สารบัญ (Table of Contents) ให้เด็คนี้ไหม?",
  header: "สารบัญ / TOC",
  multiSelect: false,
  options: [
    {
      label: "ใส่แบบเต็ม (หน้าสารบัญ + ปุ่มเมนูทุกสไลด์) (Recommended)",
      description: "มีสไลด์สารบัญที่กดกระโดดได้ + ปุ่ม 'สารบัญ' มุมซ้ายบนทุกสไลด์ เปิด overlay เมนูกระโดดได้ตลอดเวลา — เหมาะกับเด็คยาว/สอน/อ้างอิง",
    },
    {
      label: "ใส่เฉพาะหน้าสารบัญ",
      description: "มีสไลด์ Agenda ที่คลิกกระโดดได้ แต่ไม่มีปุ่มเมนู overlay ลอยทุกหน้า",
    },
    {
      label: "ไม่ใส่",
      description: "ข้ามไป — เหมาะกับเด็คสั้น เช่น pitch/BNI ที่เล่าเป็นเส้นตรงอยู่แล้ว",
    },
  ],
}
```

Recommend "เต็ม" for teaching/reference/15+ slide decks; recommend "ไม่ใส่" for ≤10-slide linear pitches.

## What "full TOC" is made of

1. **An Agenda / TOC slide** — a normal slide (usually slide 2–3) listing the sections/modules as
   **clickable** rows that jump to the right slide.
2. **A floating "สารบัญ" menu button** — pinned at the deck **root** (viewport, NOT inside a slide),
   top-left, on every slide.
3. **A slide-out overlay drawer** — opens from the menu button (and key `M`), lists every section
   grouped (e.g. by Day / Part), plus a "ทางลัด / quick links" block; each row jumps and closes the
   drawer. `Esc` closes.

All three reuse the existing deep-link machinery — jumping = `scrollToSlide(index)`.

## Data structure (single source of truth for jumps)

Keep one array near the top of the deck mapping each section to its **1-based slide number** (the
number on the `SlideShell`). Reuse it for the Agenda slide, the overlay, and any "recap" jumps.

```tsx
// 1-based slide numbers — must match the SlideShell number={N} of each target.
const SECTIONS = [
  { group: "Part 1", groupNote: "…", items: [
    { no: 1, title: "หัวข้อแรก", slide: 5 },
    { no: 2, title: "หัวข้อสอง", slide: 9 },
  ]},
  { group: "Part 2", groupNote: "…", items: [
    { no: 3, title: "หัวข้อสาม", slide: 13 },
  ]},
] as const;

const QUICK_LINKS = [
  { label: "ภาพรวม", slide: 2 },
  { label: "สรุป", slide: 30 },
];
```

> When you renumber slides, update these `slide` values. A quick guard: the largest `slide` must be
> ≤ `totalSlides`.

## State + jump helper (inside the deck component)

```tsx
const [tocOpen, setTocOpen] = useState(false);

// Jump to a 1-based slide number and close the drawer.
const goTo = useCallback((slideNumber: number) => {
  setTocOpen(false);
  scrollToSlide(slideNumber - 1); // scrollToSlide takes a 0-based index
}, [scrollToSlide]);
```

Extend the existing keyboard handler so `M` opens the drawer and `Esc` closes it. Guard the normal
arrow/space nav so it's ignored while the drawer is open:

```tsx
const onKey = (e: KeyboardEvent) => {
  if (e.key === "Escape") { setTocOpen(false); return; }
  if (tocOpen) return;                         // drawer open → ignore slide nav
  if (e.key === "m" || e.key === "M") { setTocOpen(true); return; }
  // ...existing ArrowRight / ArrowLeft / Space / Home / End handling...
};
// remember to add `tocOpen` to this effect's dependency array
```

## Menu button — pinned at the deck ROOT (every slide)

Place it as a sibling of the controls pill, **outside** the rotated canvas transform, so it stays
upright in landscape mode and never scales with the canvas. Top-left avoids the `SlideNumber` badge
(top-right). Use theme tokens for color.

```tsx
<button
  type="button"
  onClick={() => setTocOpen(true)}
  aria-label="เปิดสารบัญ"
  title="สารบัญ (กด M)"
  className={`absolute top-4 left-4 z-40 flex items-center gap-2 rounded-full bg-white/95 backdrop-blur border ${theme.border} shadow-lg pl-3 pr-4 py-2 ${theme.accent} hover:${theme.accentBg} transition-colors`}
>
  <Bars3Icon className="w-5 h-5" aria-hidden="true" />
  <span className="text-sm font-semibold">สารบัญ</span>
</button>
```

Also add a compact icon-only TOC button **inside** the controls pill (before the landscape toggle,
using `ListBulletIcon`) so it's reachable from the bottom bar too.

## Overlay drawer — slides in from the right

Rendered at the deck root (sibling of the menu button), gated on `tocOpen`. A dimmed backdrop
(click to close) + a right-side panel listing grouped sections and quick links. `z-50` so it sits
above the controls pill. Use slide-/`text-` sizes from chrome scale (this is deck chrome, like the
controls pill — `text-sm`/`text-base`/`text-lg` are allowed here, not slide content).

```tsx
{tocOpen && (
  <div className="absolute inset-0 z-50 flex">
    {/* backdrop */}
    <button
      type="button"
      aria-label="ปิดสารบัญ"
      onClick={() => setTocOpen(false)}
      className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm"
    />
    {/* panel */}
    <div className="relative ml-auto h-full w-full max-w-2xl bg-white shadow-2xl flex flex-col">
      <div className="flex items-center justify-between px-8 py-6 border-b border-slate-100">
        <div>
          <p className={`text-[11px] tracking-[0.3em] uppercase ${theme.kicker} font-semibold`}>
            สารบัญ · Agenda
          </p>
          <p className="text-2xl font-bold text-slate-900 mt-1">{deckTitle}</p>
        </div>
        <button type="button" onClick={() => setTocOpen(false)} aria-label="ปิด"
          className="w-11 h-11 rounded-full hover:bg-slate-100 flex items-center justify-center text-slate-500">
          <XMarkIcon className="w-6 h-6" aria-hidden="true" />
        </button>
      </div>
      <div className="flex-1 overflow-y-auto px-8 py-6">
        {SECTIONS.map((g) => (
          <div key={g.group} className="mb-8">
            <p className={`text-lg font-bold ${theme.accent} mb-3`}>{g.group}</p>
            <div className="space-y-1.5">
              {g.items.map((m) => (
                <button key={m.no} type="button" onClick={() => goTo(m.slide)}
                  className="w-full flex items-center gap-4 rounded-xl px-4 py-3 text-left hover:bg-slate-50 group">
                  <span className="w-9 h-9 shrink-0 rounded-lg bg-slate-50 border border-slate-200 text-sm font-bold flex items-center justify-center tabular-nums">
                    {m.no}
                  </span>
                  <span className="flex-1 text-lg text-slate-800 leading-snug">{m.title}</span>
                </button>
              ))}
            </div>
          </div>
        ))}
        {/* quick links */}
        <div className="border-t border-slate-100 pt-5 grid grid-cols-2 gap-2">
          {QUICK_LINKS.map((q) => (
            <button key={q.label} type="button" onClick={() => goTo(q.slide)}
              className="rounded-xl border border-slate-200 px-4 py-3 text-left text-base text-slate-700 hover:border-slate-300 transition-colors">
              {q.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  </div>
)}
```

## The Agenda / TOC slide (clickable in-deck)

A normal `SlideShell` placed early (slide 2–3). Render `SECTIONS` as clickable cards/rows that call
`goTo(m.slide)`. Keep it within the 5-size typography system (this is slide content, not chrome —
use `text-2xl` for rows, not `text-lg`). Add a hint like "กดที่หัวข้อเพื่อกระโดดไปได้เลย".

## Gotchas

- **Stays upright in landscape**: the menu button + overlay live at the deck root, outside the
  `rotate(90deg)` canvas transform. Never put them inside a `SlideShell`.
- **z-index order**: overlay `z-50` (above controls), menu button `z-40`.
- **Renumber discipline**: `SECTIONS[*].slide` and `QUICK_LINKS[*].slide` are 1-based and must track
  the `SlideShell number={N}` of their targets. Re-check them after inserting/removing slides.
- **Chrome vs content text sizes**: the overlay drawer and menu button are deck *chrome* (like the
  controls pill) — `text-sm`/`text-base`/`text-lg` are fine there. The Agenda *slide* is content —
  stay on the 5-size scale (`text-2xl` etc.).
- **A11y**: every jump button needs readable text or `aria-label`; the menu/close buttons need
  `aria-label`.

## Checklist (when TOC is enabled)

- [ ] Asked via `AskUserQuestion` first and Tle opted in
- [ ] `SECTIONS` (+ optional `QUICK_LINKS`) defined with correct 1-based slide numbers
- [ ] `goTo(slideNumber)` helper closes the drawer and calls `scrollToSlide(slideNumber - 1)`
- [ ] Floating "สารบัญ" button at deck root, top-left, `z-40`, on every slide
- [ ] Icon-only TOC button also inside the controls pill
- [ ] Overlay drawer `z-50`, grouped sections + quick links, backdrop closes, `Esc` closes, `M` opens
- [ ] An in-deck Agenda slide with clickable rows (for "full" option)
- [ ] Largest referenced `slide` ≤ `totalSlides`; deep-links still land correctly
