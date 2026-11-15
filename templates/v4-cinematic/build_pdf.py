#!/usr/bin/env python3
"""Build qa/deck.pdf from per-slide screenshots (never Chrome --print-to-pdf).

Why: Chrome's print-to-PDF exports box-shadows / filters on rotated elements as
transparency groups. macOS Preview, Google Drive and LINE render those as solid
black rectangles around the phones. Screenshots are flat pixels, so every viewer
shows exactly what the browser shows.

Usage: python3 build_pdf.py [--scale 2] [--quality 88]
Needs: Google Chrome, img2pdf (pip install img2pdf), Pillow.
"""
import argparse, pathlib, re, subprocess, tempfile
import img2pdf
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
here = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--scale", type=float, default=2)
ap.add_argument("--quality", type=int, default=88)
args = ap.parse_args()

html = here / "index.html"
n = len(re.findall(r'<section class="slide', html.read_text()))
qa = here / "qa"; qa.mkdir(exist_ok=True)
jpgs = []
with tempfile.TemporaryDirectory() as tmp:
    for i in range(1, n + 1):
        png = pathlib.Path(tmp) / f"s-{i:02d}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--force-device-scale-factor={args.scale}", "--window-size=1280,720",
                        "--virtual-time-budget=4000", f"--screenshot={png}",
                        f"{html.as_uri()}?shot#{i}"], check=True, capture_output=True)
        img = Image.open(png).convert("RGB")
        img.resize((640, 360), Image.LANCZOS).save(qa / f"s-{i:02d}.png")  # thumbnails for the contact sheet
        jpg = pathlib.Path(tmp) / f"s-{i:02d}.jpg"
        img.save(jpg, quality=args.quality, optimize=True)
        jpgs.append(str(jpg))
        print(f"slide {i}/{n}", flush=True)
    (qa / "deck.pdf").write_bytes(img2pdf.convert(jpgs, layout_fun=img2pdf.get_layout_fun((960, 540))))
print("wrote", qa / "deck.pdf")
