#!/usr/bin/env python3
"""Download PILOT media from the live WordPress site and crop for the new layout."""

from __future__ import annotations

import io
import json
import re
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "images" / "raw"
OUT = ROOT / "images"
DOCS = ROOT / "docs"

USER_AGENT = "PILOT-redesign/1.0 (local asset migration)"

DOWNLOADS = {
    "logo.png": [
        "https://impilot.org/wp-content/uploads/2020/04/LOGO-PNG-_-FINAL-e1586859524329.png",
    ],
    "hero-assembly.jpg": [
        "https://impilot.org/wp-content/uploads/2024/03/Videos.png",
    ],
    "hero-recipients.jpg": [
        "https://impilot.org/wp-content/uploads/2021/09/Scholarship-Recep-PILOT.jpeg",
    ],
    "hero-giving.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/Giving.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/Giving-e1586823568540.jpg",
    ],
    "newsletter-cover.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/Newsletter-Clean.jpg",
    ],
    "trustee-ruqia.png": [
        "https://impilot.org/wp-content/uploads/2020/04/Raquia-Iqbal.png",
        "https://impilot.org/wp-content/uploads/2020/04/Raquia-Iqbal-150x150.png",
    ],
    "trustee-anil.png": [
        "https://impilot.org/wp-content/uploads/2020/04/Anil-Rego.png",
        "https://impilot.org/wp-content/uploads/2020/04/Anil-Rego-150x150.png",
    ],
    "trustee-ayeesha.png": [
        "https://impilot.org/wp-content/uploads/2020/05/Ayesha-New.png",
    ],
    "update-1.jpg": [
        "https://impilot.org/wp-content/uploads/2023/12/1.jpg",
        "https://impilot.org/wp-content/uploads/2023/12/1-1024x1024.jpg",
    ],
    "update-2.jpg": [
        "https://impilot.org/wp-content/uploads/2023/12/2.jpg",
        "https://impilot.org/wp-content/uploads/2023/12/2-1024x1024.jpg",
    ],
    "update-3.jpg": [
        "https://impilot.org/wp-content/uploads/2023/12/3.jpg",
        "https://impilot.org/wp-content/uploads/2023/12/3-1024x1024.jpg",
    ],
    "init-comp.jpg": [
        "https://impilot.org/wp-content/uploads/2023/03/IMpilot-Comp.jpg",
        "https://impilot.org/wp-content/uploads/2023/03/IMpilot-Comp-scaled-e1765672418880.jpg",
        "https://impilot.org/wp-content/uploads/2023/03/IMpilot-Comp-scaled-e1765672418880-897x1024.jpg",
    ],
    "init-i5.jpg": ["https://impilot.org/wp-content/uploads/2020/04/I5.jpg"],
    "init-sonny.jpg": ["https://impilot.org/wp-content/uploads/2020/04/Sonny-ra.jpg"],
    "init-i1.jpg": ["https://impilot.org/wp-content/uploads/2020/04/I1.jpg"],
    "init-leadership.png": ["https://impilot.org/wp-content/uploads/2024/10/Leadership-Principles.png"],
    "init-i2.jpg": ["https://impilot.org/wp-content/uploads/2020/04/I2.jpg"],
    "init-i3.jpg": ["https://impilot.org/wp-content/uploads/2020/04/I3.jpg"],
    "init-i7.jpg": ["https://impilot.org/wp-content/uploads/2020/04/I7.jpg"],
    "g-winners-2021-a.jpg": [
        "https://impilot.org/wp-content/uploads/2021/07/20210630_230401.jpg",
        "https://impilot.org/wp-content/uploads/2021/07/20210630_230401-1024x1024.jpg",
    ],
    "g-winners-2021-b.jpg": [
        "https://impilot.org/wp-content/uploads/2021/07/20210630_124918.jpg",
        "https://impilot.org/wp-content/uploads/2021/07/20210630_124918-1024x880.jpg",
    ],
    "g-awardees-2019.jpg": [
        "https://impilot.org/wp-content/uploads/2021/03/Pilot-Awardees-2019.jpg",
        "https://impilot.org/wp-content/uploads/2021/03/Pilot-Awardees-2019-260x123.jpg",
    ],
    "g-volleyball.jpg": [
        "https://impilot.org/wp-content/uploads/2021/03/State-Level-Volleyball-Winners.jpg",
        "https://impilot.org/wp-content/uploads/2021/03/State-Level-Volleyball-Winners-300x192.jpg",
    ],
    "g-winnetta-pune.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/MC-Henry-2.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/MC-Henry-2-260x146.jpg",
    ],
    "g-winnetta-newasa.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/MC-Henry-1.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/MC-Henry-1-260x146.jpg",
    ],
    "g-gift-argentina.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/1006180251a_HDR-rotated.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/1006180251a_HDR-rotated-576x1024.jpg",
    ],
    "g-4h-fareed.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/WITH-fareed-upload-scaled.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/WITH-fareed-upload-scaled-260x146.jpg",
    ],
    "g-archbishop.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/with-arch-bishop.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/with-arch-bishop-1024x576.jpg",
    ],
    "g-sda-principal.jpg": ["https://impilot.org/wp-content/uploads/2020/04/IMG_7180.jpg"],
    "g-sonny-students.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/Sonny.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/Sonny-1024x382.jpg",
    ],
    "g-st-marys-students.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/0122200114a-rotated.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/0122200114a-rotated-576x1024.jpg",
    ],
    "g-gommateshwara.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/0926180822a_HDR.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/0926180822a_HDR-1024x576.jpg",
    ],
    "g-assembly.jpg": ["https://impilot.org/wp-content/uploads/2020/04/CIMG1859.jpg"],
    "g-sda-bangalore.jpg": [
        "https://impilot.org/wp-content/uploads/2021/08/WhatsApp-Image-2021-08-05-at-7.36.33-PM.jpeg",
        "https://impilot.org/wp-content/uploads/2021/08/WhatsApp-Image-2021-08-05-at-7.36.33-PM-1024x1024.jpeg",
    ],
    "g-st-marys-winners.jpg": ["https://impilot.org/wp-content/uploads/2020/04/1005160141.jpg"],
    "g-flora.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/DSC_6966-scaled.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/DSC_6966-scaled-1024x687.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/DSC_6966-scaled-300x201.jpg",
    ],
    "g-ayeesha-marys.jpg": ["https://impilot.org/wp-content/uploads/2020/04/2018-03-13-PHOTO-00000006.jpg"],
    "g-awards-marys.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/DSC_22241-Upload.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/DSC_22241-Upload-1024x687.jpg",
    ],
    "g-dance.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/DSC_2258-Upload.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/DSC_2258-Upload-1024x687.jpg",
    ],
    "g-sp-address.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/1004190035b.jpg",
        "https://impilot.org/wp-content/uploads/2020/04/1004190035b-1024x576.jpg",
    ],
    "g-sp-sujitha-a.png": ["https://impilot.org/wp-content/uploads/2020/04/SP-Police12.png"],
    "g-sp-sujitha-b.png": ["https://impilot.org/wp-content/uploads/2020/04/SP-Police.png"],
    "g-smiling.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/WhatsApp-Image-2020-04-24-at-10.37.31-PM.jpeg",
        "https://impilot.org/wp-content/uploads/2020/04/WhatsApp-Image-2020-04-24-at-10.37.31-PM-1024x576.jpeg",
    ],
    "g-4h-activity.jpg": [
        "https://impilot.org/wp-content/uploads/2020/04/WhatsApp-Image-2020-04-24-at-10.39.13-PM.jpeg",
        "https://impilot.org/wp-content/uploads/2020/04/WhatsApp-Image-2020-04-24-at-10.39.13-PM-576x1024.jpeg",
    ],
    "g-disha.jpg": [
        "https://impilot.org/wp-content/uploads/2022/03/WhatsApp-Image-2022-03-12-at-3.14.58-PM.jpeg",
        "https://impilot.org/wp-content/uploads/2022/03/WhatsApp-Image-2022-03-12-at-3.14.58-PM-768x1024.jpeg",
    ],
    "g-2022-a.jpg": [
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-02-at-9.08.01-PM.jpeg",
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-02-at-9.08.01-PM-768x1024.jpeg",
    ],
    "g-2022-b.jpg": [
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-02-at-9.10.19-PM.jpeg",
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-02-at-9.10.19-PM-768x1024.jpeg",
    ],
    "g-2022-c.jpg": [
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-03-at-1.50.42-AM.jpeg",
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-03-at-1.50.42-AM-768x1024.jpeg",
    ],
    "g-2022-d.jpg": [
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-02-at-9.04.38-PM.jpeg",
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-02-at-9.04.38-PM-1024x768.jpeg",
    ],
    "g-2022-e.jpg": [
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-02-at-9.06.05-PM.jpeg",
        "https://impilot.org/wp-content/uploads/2022/11/WhatsApp-Image-2022-11-02-at-9.06.05-PM-768x1024.jpeg",
    ],
    "g-topper-2023.jpg": [
        "https://impilot.org/wp-content/uploads/2023/06/IMG-20230509-WA0075-1.jpg",
        "https://impilot.org/wp-content/uploads/2023/06/IMG-20230509-WA0075-1-514x1024.jpg",
    ],
    "g-topper-2024.jpg": [
        "https://impilot.org/wp-content/uploads/2024/08/WhatsApp-Image-2024-08-17-at-20.38.22.jpeg",
        "https://impilot.org/wp-content/uploads/2024/08/WhatsApp-Image-2024-08-17-at-20.38.22-682x1024.jpeg",
    ],
    "g-recipients-2024.jpg": [
        "https://impilot.org/wp-content/uploads/2024/12/WhatsApp-Image-2024-12-19-at-18.53.55.jpeg",
        "https://impilot.org/wp-content/uploads/2024/12/WhatsApp-Image-2024-12-19-at-18.53.55-1024x819.jpeg",
    ],
    "g-recent.jpg": [
        "https://impilot.org/wp-content/uploads/2026/04/WhatsApp-Image-2026-04-27-at-11.31.04-AM-rotated.jpeg",
    ],
    "g-awards-6109.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_6109.jpg"],
    "g-awards-5581.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_5581.jpg"],
    "g-awards-6101.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_6101.jpg"],
    "g-awards-6097.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_6097-rotated.jpg"],
    "g-awards-6088.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_6088-rotated.jpg"],
    "g-awards-6084.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_6084-rotated.jpg"],
    "g-awards-6078.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_6078-rotated.jpg"],
    "g-awards-5980.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_5980.jpg"],
    "g-awards-5903.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_5903.jpg"],
    "g-awards-5857.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_5857.jpg"],
    "g-awards-5848.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_5848.jpg"],
    "g-awards-5806.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_5806.jpg"],
    "g-awards-5700.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_5700.jpg"],
    "g-awards-5592.jpg": ["https://impilot.org/wp-content/uploads/2023/12/MJU_5592.jpg"],
}

PDFS = {
    "newsletter-2019-2020.pdf": "https://impilot.org/wp-content/uploads/2020/04/Newsletter.pdf",
    "newsletter-2021.pdf": "https://impilot.org/wp-content/uploads/2021/04/PILOT-Newsletter-Latest-2021.pdf",
    "pilot-financials.pdf": "https://impilot.org/wp-content/uploads/2022/08/PILOT-Financials.pdf",
    "sample-essay.pdf": "https://impilot.org/wp-content/uploads/2020/05/MY-GRANDMOTHER-Essay.pdf",
    "update-organized.pdf": "https://impilot.org/wp-content/uploads/2025/12/organized-1.pdf",
    "letter-to-pilot.pdf": "https://impilot.org/wp-content/uploads/2026/05/letter-to-pilot.pdf",
}

CROPS = {
    "logo.png": ("contain", 280, 280),
    "hero-assembly.jpg": ("cover", 1920, 1080, (0.5, 0.42)),
    "hero-recipients.jpg": ("cover", 1400, 1000, (0.5, 0.38)),
    "hero-giving.jpg": ("cover", 1600, 1000, (0.5, 0.4)),
    "newsletter-cover.jpg": ("cover", 720, 1000, (0.5, 0.45)),
    "trustee-ruqia.png": ("cover", 480, 480, (0.5, 0.28)),
    "trustee-anil.png": ("cover", 480, 480, (0.5, 0.28)),
    "trustee-ayeesha.png": ("cover", 480, 480, (0.5, 0.28)),
    "update-1.jpg": ("cover", 900, 900, (0.5, 0.45)),
    "update-2.jpg": ("cover", 900, 900, (0.5, 0.45)),
    "update-3.jpg": ("cover", 900, 900, (0.5, 0.45)),
    "init-comp.jpg": ("cover", 900, 1200, (0.5, 0.35)),
    "init-i5.jpg": ("cover", 1200, 800, (0.5, 0.4)),
    "init-sonny.jpg": ("cover", 1200, 800, (0.5, 0.35)),
    "init-i1.jpg": ("cover", 1000, 1200, (0.5, 0.35)),
    "init-leadership.png": ("contain", 1400, 900),
    "init-i2.jpg": ("cover", 1200, 800, (0.5, 0.4)),
    "init-i3.jpg": ("cover", 1200, 800, (0.5, 0.4)),
    "init-i7.jpg": ("cover", 1200, 800, (0.5, 0.4)),
}


def fetch(url: str) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=45) as res:
            if res.status != 200:
                return None
            return res.read()
    except Exception as exc:
        print(f"  fail {url} ({exc})")
        return None


def save_raw(name: str, urls: list[str]) -> Path | None:
    dest = RAW / name
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    for url in urls:
        print(f"GET {name} <- {url}")
        data = fetch(url)
        if not data:
            continue
        dest.write_bytes(data)
        return dest
    return None


def cover_crop(im: Image.Image, w: int, h: int, focus=(0.5, 0.5)) -> Image.Image:
    im = ImageOps.exif_transpose(im)
    src_w, src_h = im.size
    target = w / h
    current = src_w / src_h
    if current > target:
        new_w = int(src_h * target)
        left = max(0, min(src_w - new_w, int(src_w * focus[0] - new_w / 2)))
        im = im.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target)
        top = max(0, min(src_h - new_h, int(src_h * focus[1] - new_h / 2)))
        im = im.crop((0, top, src_w, top + new_h))
    return im.resize((w, h), Image.Resampling.LANCZOS)


def contain_fit(im: Image.Image, w: int, h: int) -> Image.Image:
    im = ImageOps.exif_transpose(im)
    im.thumbnail((w, h), Image.Resampling.LANCZOS)
    return im


def process_image(name: str, raw_path: Path) -> None:
    spec = CROPS.get(name)
    out_path = OUT / name
    im = Image.open(raw_path)
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if name.endswith(".png") else "RGB")

    if spec:
        mode = spec[0]
        if mode == "cover":
            _, w, h, *rest = spec
            focus = rest[0] if rest else (0.5, 0.45)
            im = cover_crop(im, w, h, focus)
        else:
            _, w, h = spec
            im = contain_fit(im, w, h)
    else:
        # Gallery defaults: crop to 4:5 portrait or 3:2 landscape, max 1200 on long edge
        w, h = im.size
        if w >= h:
            im = cover_crop(im, 1200, 800, (0.5, 0.4))
        else:
            im = cover_crop(im, 800, 1000, (0.5, 0.38))

    if name.endswith(".png"):
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        im.save(out_path, "PNG", optimize=True)
    else:
        if im.mode == "RGBA":
            bg = Image.new("RGB", im.size, (246, 239, 227))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        elif im.mode != "RGB":
            im = im.convert("RGB")
        im.save(out_path, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"CROP {name} -> {im.size}")


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    failed = []
    for name, urls in DOWNLOADS.items():
        path = save_raw(name, urls)
        if not path:
            failed.append(name)
            continue
        try:
            process_image(name, path)
        except Exception as exc:
            print(f"PROCESS FAIL {name}: {exc}")
            failed.append(name)

    for name, url in PDFS.items():
        dest = DOCS / name
        if dest.exists() and dest.stat().st_size > 0:
            continue
        print(f"GET {name}")
        data = fetch(url)
        if data:
            dest.write_bytes(data)
        else:
            failed.append(name)

    # Favicon from logo
    logo = OUT / "logo.png"
    if logo.exists():
        im = Image.open(logo)
        im = ImageOps.exif_transpose(im).convert("RGBA")
        im.thumbnail((64, 64), Image.Resampling.LANCZOS)
        im.save(OUT / "favicon.png", "PNG")

    print(json.dumps({"failed": failed}, indent=2))


if __name__ == "__main__":
    main()
