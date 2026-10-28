"""Recorta as fotos de ../_ref (Instagram e catálogo do Canva) em 4:5 e salva em WebP (640 e 1080 px).
Também injeta a grade de trabalhos no index.html e no trabalhos.html, entre os marcadores
<!--GRADE--> ... <!--/GRADE--> (e <!--GRADE-RESUMO--> no index).

Cada foto: (saída, origem, foco_y, categoria, legenda). A origem é "NNN-K" do Instagram
(_ref/ig/NNN-K.jpg) ou "cv-NN" do catálogo (_ref/canva/canva-NN-*.jpg). foco_y vai de 0 (topo) a 1 (base).

Uso: python -I tools/processar.py
"""
import glob
import html
import re
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
REF = RAIZ.parent / "_ref"
SAIDA = RAIZ / "assets" / "p"
LARGURAS = (640, 1080)

CATEGORIAS = {"fox": "Efeito Fox", "egipcio": "Volume Egípcio", "brasileiro": "Volume Brasileiro",
              "volumoso": "Volumoso", "anime": "Efeito Anime", "sobrancelha": "Sobrancelhas"}

# trabalhos (a ordem é a da grade; as 12 primeiras vão para o resumo do index)
TRABALHOS = [
    ("t-fox-01", "006-1", .35, "fox", "Fox com curvatura marcante"),
    ("t-egi-01", "004-1", .3, "egipcio", "Volume Egípcio e design de sobrancelhas"),
    ("t-bra-01", "008-2", .4, "brasileiro", "Volume Brasileiro e design de sobrancelhas"),
    ("t-vol-01", "026-1", .4, "volumoso", "Volumoso Black 8D"),
    ("t-fox-02", "009-1", .4, "fox", "Fox Marrom, curvatura L"),
    ("t-egi-02", "034-3", .4, "egipcio", "Volume Egípcio"),
    ("t-bra-02", "021-2", .4, "brasileiro", "Volume Brasileiro"),
    ("t-ani-01", "015-1", .45, "anime", "Efeito Anime"),
    ("t-fox-03", "028-1", .4, "fox", "Fox"),
    ("t-bra-03", "030-1", .4, "brasileiro", "Volume Brasileiro"),
    ("t-vol-02", "036-1", .4, "volumoso", "Volumoso 6D"),
    ("t-sob-01", "039-2", .4, "sobrancelha", "Design de sobrancelhas e Volumoso 6D"),
    ("t-egi-03", "005-2", .4, "egipcio", "Volume Egípcio"),
    ("t-fox-04", "035-1", .4, "fox", "Fox delicado"),
    ("t-bra-04", "029-1", .4, "brasileiro", "Volume Brasileiro com glow"),
    ("t-egi-04", "027-1", .4, "egipcio", "Volume Egípcio"),
    ("t-bra-05", "017-1", .4, "brasileiro", "Volume Brasileiro"),
    ("t-fox-05", "037-1", .4, "fox", "Fox para noiva"),
    ("t-vol-03", "013-1", .4, "volumoso", "Volume com destaque"),
    ("t-bra-06", "031-1", .4, "brasileiro", "Volume Brasileiro com manutenção em dia"),
    ("t-egi-05", "014-1", .4, "egipcio", "Volume Egípcio"),
    ("t-bra-07", "032-1", .4, "brasileiro", "Volume Brasileiro"),
    ("t-sob-02", "024-1", .5, "sobrancelha", "Design de sobrancelhas"),
    ("t-fox-06", "023-1", .4, "fox", "Fox e design de sobrancelhas"),
    ("t-egi-06", "010-1", .35, "egipcio", "Egípcio Marrom"),
    ("t-bra-08", "033-1", .4, "brasileiro", "Volume Brasileiro bem cheio"),
    ("t-vol-04", "039-1", .4, "volumoso", "Volume 6D"),
    ("t-bra-09", "038-1", .4, "brasileiro", "Brasileiro delicado"),
    ("t-sob-03", "026-2", .4, "sobrancelha", "Design de sobrancelhas e Volumoso Black"),
    ("t-vol-05", "041-2", .4, "volumoso", "Cílios marrom"),
]

# fotos das seções (estilos, sobrancelhas, sobre, estúdio)
FIXAS = [
    ("e-classic", "cv-12", .5), ("e-egipcio", "034-2", .45), ("e-brasileiro", "022-2", .5), ("e-sirena", "cv-13", .5),
    ("e-fox", "006-2", .4), ("e-marrom", "007-1", .5), ("e-black", "036-2", .45), ("e-anime", "015-1", .45),
    ("s-1", "cv-24", .5), ("s-2", "cv-25", .5), ("s-3", "cv-26", .5),
    ("fernanda", "cv-02", .3), ("fernanda-2", "cv-03", .35), ("bast-1", "cv-27", .4), ("bast-2", "cv-28", .45),
    ("manutencao", "cv-21", 0),
]


def origem(cod):
    if cod.startswith("cv-"):
        return Path(glob.glob(str(REF / "canva" / f"canva-{cod[3:]}-*.jpg"))[0])
    return REF / "ig" / f"{cod}.jpg"


GIRAR = {"007-1": 180}  # fotos tiradas com a cliente deitada, de ponta-cabeça


def recortar(cod, foco, razao=(4, 5)):
    im = ImageOps.exif_transpose(Image.open(origem(cod))).convert("RGB").rotate(GIRAR.get(cod, 0))
    w, h = im.size
    rw, rh = razao
    if w / h > rw / rh:
        nw = round(h * rw / rh); x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = round(w * rh / rw); y = round((h - nh) * foco)
    return im.crop((0, y, w, y + nh))


def salvar(nome, im, larguras=LARGURAS):
    feitos = []
    for lw in larguras:
        alvo = im if im.width <= lw else im.resize((lw, round(im.height * lw / im.width)), Image.LANCZOS)
        alvo.save(SAIDA / f"{nome}-{lw}.webp", quality=80, method=6)
        feitos.append((lw, alvo.size))
    return feitos


def figura(nome, cat, legenda, cls="trab"):
    leg = html.escape(legenda)
    return (f'<figure class="{cls} revela" data-cat="{cat}"><button type="button" class="trab__abre" aria-label="Ampliar: {leg}">'
            f'<img src="assets/p/{nome}-640.webp" srcset="assets/p/{nome}-640.webp 640w, assets/p/{nome}-1080.webp 1080w" '
            f'sizes="(max-width:700px) 50vw, 25vw" width="640" height="800" alt="{leg}" loading="lazy" decoding="async"></button>'
            f'<figcaption>{leg}<span>{CATEGORIAS[cat]}</span></figcaption></figure>')


def injetar(arquivo, marca, conteudo):
    p = RAIZ / arquivo
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    t2 = re.sub(rf"(<!--{marca}-->).*?(<!--/{marca}-->)", lambda m: m.group(1) + "\n" + conteudo + "\n" + m.group(2), t, flags=re.S)
    p.write_text(t2, encoding="utf-8")


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, cod, foco, *_ in TRABALHOS + FIXAS:
        razao = (615, 410) if nome == "manutencao" else (4, 5)
        salvar(nome, recortar(cod, foco, razao))
    grade = "\n".join(figura(n, c, l) for n, _, _, c, l in TRABALHOS)
    resumo = "\n".join(figura(n, c, l) for n, _, _, c, l in TRABALHOS[:12])
    injetar("trabalhos.html", "GRADE", grade)
    injetar("index.html", "GRADE-RESUMO", resumo)
    print(len(TRABALHOS), "trabalhos,", len(FIXAS), "fixas")


if __name__ == "__main__":
    main()
