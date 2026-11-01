"""Convierte a WebP las imágenes (JPG/PNG/GIF) que usa el sitio y actualiza las páginas.

    python tools/optimize_images.py site              # en el lugar (así corre en GitHub Actions)
    python tools/optimize_images.py site --out dist   # deja una copia optimizada en dist/ y no toca site/

Sólo se tocan las imágenes que alguna página (.html) o estilo (.css) usa; el resto queda como está.
Las imágenes se achican a 1600 px de ancho como máximo. Si el WebP no resulta más liviano que el
original, se deja el original. No hace falta correrlo a mano: el flujo de GitHub lo ejecuta en cada
publicación, de modo que en el repositorio se pueden seguir subiendo fotos JPG/PNG comunes.
"""
import argparse
import os
import shutil
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Falta Pillow: pip install pillow")

MAX_WIDTH = 1600
QUALITY = 80
EXTS = (".jpg", ".jpeg", ".png", ".gif")
# Estas quedan en su formato: las redes sociales y algunos lectores no muestran bien WebP
# en las vistas previas de los enlaces (og:image).
KEEP = {"assets/photo.jpg", "assets/favicon.svg"}


def read(path):
    with open(path, encoding="utf8", errors="ignore") as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--out")
    args = ap.parse_args()

    root = args.site
    if args.out:
        shutil.rmtree(args.out, ignore_errors=True)
        shutil.copytree(root, args.out)
        root = args.out
    root = os.path.abspath(root)

    texts = []
    for base, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith((".html", ".css")):
                texts.append(os.path.join(base, f))
    corpus = "\n".join(read(t) for t in texts)

    renamed = {}
    saved = 0
    for base, _, files in os.walk(os.path.join(root, "assets")):
        for f in files:
            if not f.lower().endswith(EXTS):
                continue
            full = os.path.join(base, f)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if rel in KEEP or "/" + rel not in corpus:
                continue
            dest = os.path.splitext(full)[0] + ".webp"
            if os.path.exists(dest):
                continue
            try:
                with Image.open(full) as im:
                    if getattr(im, "is_animated", False):
                        continue
                    im = ImageOps.exif_transpose(im)
                    if im.width > MAX_WIDTH:
                        im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)
                    if im.mode not in ("RGB", "RGBA"):
                        im = im.convert("RGBA" if "transparency" in im.info or im.mode in ("LA", "PA") else "RGB")
                    im.save(dest, "WEBP", quality=QUALITY, method=6)
            except Exception as e:
                print(f"  omitida {rel}: {e}")
                continue
            if os.path.getsize(dest) >= os.path.getsize(full):
                os.remove(dest)
                continue
            saved += os.path.getsize(full) - os.path.getsize(dest)
            os.remove(full)
            renamed["/" + rel] = "/" + os.path.splitext(rel)[0] + ".webp"

    for t in texts:
        s = read(t)
        new = s
        for old, webp in renamed.items():
            new = new.replace(old, webp)
        if new != s:
            with open(t, "w", encoding="utf8", newline="") as fh:
                fh.write(new)
    print(f"{len(renamed)} imágenes pasadas a WebP, {saved / 1024 / 1024:.1f} MB menos")


main()
