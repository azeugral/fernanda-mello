"""Recorta o logo oficial (capa do catálogo do Canva, _ref/canva/canva-01-p1.jpg) em PNG transparente.
O logo é dourado/rosa sobre preto: a transparência sai do brilho de cada pixel e a cor é
"despremultiplicada" do preto, então o PNG assenta em qualquer fundo escuro sem caixa.
Gera: logo.png (monograma + nome + BEAUTY), logo-fm.png (só o monograma), favicons e apple-touch-icon.

Uso: python -I tools/logo.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ.parent / "_ref" / "canva" / "canva-01-p1.jpg"
IMG = RAIZ / "assets" / "img"
PRETO = 16  # o fundo da arte não é preto puro; abaixo disso vira transparente


def recortar(caixa, limpar=()):
    im = np.asarray(Image.open(FONTE).convert("RGB").crop(caixa)).astype(np.float32)
    for x0, y0, x1, y1 in limpar:  # apaga restos do fundo (fios e arcos) que encostam no recorte
        im[y0:y1, x0:x1] = 0
    m = im.max(axis=2)
    a = np.clip((m - PRETO) / (235 - PRETO), 0, 1)
    a = np.where(a < .05, 0, a)
    cor = np.clip(im / np.maximum(a[..., None], 1e-3), 0, 255)
    cor = np.where(a[..., None] > 0, cor, 0)
    rgba = np.dstack([cor, a * 255]).astype(np.uint8)
    out = Image.fromarray(rgba, "RGBA")
    return out.crop(out.getbbox())


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    logo = recortar((240, 330, 1020, 776), limpar=[(0, 0, 200, 150), (762, 60, 780, 320), (0, 390, 60, 446), (730, 360, 780, 446), (690, 0, 780, 50)])
    fm = recortar((440, 330, 820, 610), limpar=[(0, 0, 40, 120)])
    for nome, im in [("logo.png", logo), ("logo-fm.png", fm)]:
        im.save(IMG / nome, optimize=True)
        print(nome, im.size)
    # favicon: FM dourado num quadrado preto; no iOS sem cantos (o sistema arredonda)
    for nome, lado, raio in [("favicon-32.png", 32, 6), ("favicon-192.png", 192, 36), ("apple-touch-icon.png", 180, 0)]:
        base = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
        m = Image.new("L", (lado, lado), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, lado - 1, lado - 1], raio, fill=255)
        base.paste((12, 9, 10, 255), (0, 0), m)
        f = fm.copy(); f.thumbnail((int(lado * .78), int(lado * .7)), Image.LANCZOS)
        base.alpha_composite(f, ((lado - f.width) // 2, (lado - f.height) // 2))
        base.save(RAIZ / nome)
    Image.open(RAIZ / "favicon-32.png").save(RAIZ / "favicon.ico", sizes=[(32, 32), (16, 16)])


if __name__ == "__main__":
    main()
