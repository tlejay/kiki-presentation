"""Generate deck.md from index.html so the brief never drifts from the slides."""
import re, html
from pathlib import Path
src = Path(__file__).with_name('index.html').read_text()
head = Path(__file__).with_name('deck-head.md').read_text()
tail = Path(__file__).with_name('deck-qa.md').read_text()
def text(fr):
    fr = re.sub(r'<br\s*/?>', ' / ', fr); fr = re.sub(r'<[^>]+>', '', fr)
    return re.sub(r'\s+', ' ', html.unescape(fr)).strip()
out = [head]
for n, m in enumerate(re.finditer(r'<section class="slide([^"]*)"([^>]*)>(.*?)</section>', src, re.S), 1):
    cls, attrs, body = m.groups()
    title = re.search(r'data-title="([^"]+)"', attrs).group(1)
    time = re.search(r'data-time="([^"]+)"', attrs).group(1)
    w = re.search(r'data-who="([^"]+)"', attrs)  # optional per-slide speaker
    who = w.group(1) if w else '-'
    h1 = text(re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1))
    kick = re.search(r'class="kick">(.*?)</div>', body)
    lead = re.search(r'class="lead[^"]*"[^>]*>(.*?)</p>', body, re.S)
    bgs = re.findall(r'class="bg[^"]*" style="background-image:url\(img/([^)]+)\)', body)
    shots = sorted(set(re.findall(r'scr/([\w-]+\.png)', body)))
    prods = re.findall(r'prod/([\w.-]+)', body)
    note = re.search(r'<aside class="note">(.*?)</aside>', body, re.S).group(1).strip()
    out.append(f"\n## {n:02d} · {title}\n")
    out.append(f"- **ผู้พูด / เวลา:** {who} · {time}")
    if kick: out.append(f"- **คำนำ:** {text(kick.group(1))}")
    out.append(f"- **หัวเรื่อง (Key message):** {h1}")
    if lead: out.append(f"- **ข้อความรอง:** {text(lead.group(1))}")
    if bgs: out.append(f"- **ภาพพื้นหลัง:** `img/{bgs[0]}`")
    if shots: out.append(f"- **หน้าจอจริง:** " + ', '.join(f'`{s}`' for s in shots))
    if prods: out.append(f"- **ภาพสินค้าจริง:** " + ', '.join(f'`{p}`' for p in prods))
    out.append("\n**บทพูด**\n")
    out += ['> ' + l.strip() for l in note.splitlines() if l.strip()]
out.append('\n' + tail)
Path(__file__).with_name('deck.md').write_text('\n'.join(out) + '\n')
print('deck.md written')
