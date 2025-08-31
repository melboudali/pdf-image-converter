#!/usr/bin/env python3
from pathlib import Path
from typing import Tuple
from pdf2image import convert_from_path
from PIL import Image, ImageChops

# ====== Settings ======
INPUT_DIR = Path("./pdfs")
OUTPUT_DIR = Path("./images")
DPI = 400  # try 300–400 for sharper output
EXTENSION = "png"  # "png" or "jpg"
FORMAT = "PNG"  # "PNG" or "JPEG"
TRIM_BORDERS = True
BORDER_COLOR: Tuple[int, int, int] = (0, 0, 0)  # black
TRIM_TOLERANCE = 10  # 0-255; higher = more aggressive border trimming
# ======================


def ensure_dirs():
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"Input folder not found: {INPUT_DIR.resolve()}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def trim_border(
    img: Image.Image, bg_rgb: Tuple[int, int, int] = (0, 0, 0), tolerance: int = 10
) -> Image.Image:
    """
    Auto-crops uniform borders close to bg_rgb.
    Uses a tolerance so near-black edges are removed but content remains.
    """
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    # Build a solid background image, compute difference
    bg = Image.new("RGB", img.size, color=bg_rgb)
    diff = ImageChops.difference(img.convert("RGB"), bg)

    # Convert to grayscale and threshold to isolate non-border content
    gray = diff.convert("L")
    # Map pixels: > tolerance -> 255, else 0
    bw = gray.point(lambda p: 255 if p > tolerance else 0)

    bbox = bw.getbbox()
    if bbox:
        return img.crop(bbox)
    return img  # nothing to trim


def convert_pdf_to_pngs(pdf_path: Path):
    print(f"Converting: {pdf_path}")
    try:
        images = convert_from_path(str(pdf_path), dpi=DPI)
    except Exception as e:
        print(f"  ERROR reading {pdf_path.name}: {e}")
        return

    base = pdf_path.stem
    for i, img in enumerate(images, start=1):
        if TRIM_BORDERS:
            img = trim_border(img, bg_rgb=BORDER_COLOR, tolerance=TRIM_TOLERANCE)

        # Ensure RGB (avoids weird transparency issues in some viewers)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        out_file = OUTPUT_DIR / f"{base}_page_{i}.{EXTENSION}"
        try:
            img.save(out_file, FORMAT)
            print(f"  Saved: {out_file}")
        except Exception as e:
            print(f"  ERROR saving page {i} of {pdf_path.name}: {e}")


def main():
    ensure_dirs()
    pdfs = [
        p for p in INPUT_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"
    ]
    if not pdfs:
        print(f"No PDFs found in {INPUT_DIR.resolve()}")
        return

    for pdf in pdfs:
        convert_pdf_to_pngs(pdf)


if __name__ == "__main__":
    main()
