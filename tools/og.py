"""Prévia de link (og.jpg, 1200x630): os fios de luz do hero com o logo oficial no centro.
O essencial fica no quadrado central, porque o WhatsApp corta a miniatura em quadrado.

Uso: python -I tools/og.py
"""
import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
logo = base64.b64encode((RAIZ / "assets" / "img" / "logo.png").read_bytes()).decode()
HTML = f"""<body style="margin:0;background:#000;width:1200px;height:630px;position:relative;overflow:hidden">
<canvas id="c" width="2400" height="1260" style="position:absolute;inset:0;width:1200px;height:630px"></canvas>
<img src="data:image/png;base64,{logo}" style="position:absolute;left:50%;top:50%;width:400px;transform:translate(-50%,-54%)">
</body>"""

with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(HTML)
    pg.add_script_tag(path=str(RAIZ / "assets" / "fios.js"))
    pg.evaluate("fiosGL(document.getElementById('c'), {preserveDrawingBuffer:true}).desenhar(1.2, 0)")
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(RAIZ / "og.jpg"), type="jpeg", quality=86)
    b.close()
print("og.jpg")
