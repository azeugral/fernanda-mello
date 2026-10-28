"""Renderiza os fios de luz do hero para o celular (assets/video/fios-celular.mp4) com o mesmo shader
de assets/fios.js, quadro a quadro num Chromium headless, e codifica com o ffmpeg do imageio-ffmpeg.
O loop fecha sem emenda: a fase vai de 0 a 2π e o quadro 2π (igual ao 0) não entra.

Uso: python -I tools/gerar_fios.py [--teste]   (--teste só salva quadros em ../_ref/folhas)
"""
import base64
import subprocess
import sys
from io import BytesIO
from pathlib import Path

import imageio_ffmpeg
from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "assets" / "video"
FPS, SEGUNDOS = 24, 16
W, H = 720, 1280


def abrir(pw, w, h):
    b = pw.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": w, "height": h})
    pg.set_content(f'<body style="margin:0;background:#000"><canvas id="c" width="{w}" height="{h}"></canvas></body>')
    pg.add_script_tag(path=str(RAIZ / "assets" / "fios.js"))
    pg.evaluate("window.F = fiosGL(document.getElementById('c'), {preserveDrawingBuffer: true})")
    return b, pg


def quadro(pg, fase, cel):
    d = pg.evaluate(f"(F.desenhar({fase}, {cel}), document.getElementById('c').toDataURL('image/png'))")
    return base64.b64decode(d.split(",", 1)[1])


def main():
    with sync_playwright() as pw:
        if "--teste" in sys.argv:
            for nome, w, h, cel in [("desktop", 1440, 820, 0), ("celular", 390, 700, 1)]:
                b, pg = abrir(pw, w, h)
                for fase in (0.0, 2.0):
                    (RAIZ.parent / "_ref" / "folhas" / f"fios-{nome}-{fase:.0f}.png").write_bytes(quadro(pg, fase, cel))
                b.close()
            print("quadros de teste em _ref/folhas")
            return
        SAIDA.mkdir(parents=True, exist_ok=True)
        mp4 = SAIDA / "fios-celular.mp4"
        enc = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "image2pipe",
                                "-framerate", str(FPS), "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "slow",
                                "-crf", "25", "-x264-params", "aq-mode=3", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(mp4)],
                               stdin=subprocess.PIPE)
        b, pg = abrir(pw, W, H)
        total = FPS * SEGUNDOS
        for i in range(total):
            png = quadro(pg, i / total * 6.283185307179586, 1)
            enc.stdin.write(png)
            if i == 0:
                Image.open(BytesIO(png)).convert("RGB").save(RAIZ / "assets" / "img" / "fios-poster.webp", quality=82)
        b.close()
        enc.stdin.close()
        enc.wait()
        print(mp4.name, round(mp4.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
