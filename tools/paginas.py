"""Monta trabalhos.html e 404.html com o mesmo <head>, topo e rodapé do index.html.
Depois rode tools/processar.py, que injeta a grade de fotos em trabalhos.html.

Uso: python -I tools/paginas.py
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
idx = (RAIZ / "index.html").read_text(encoding="utf-8")
head = idx.split("<body>")[0]
topo = re.search(r"<!--TOPO-->.*?<!--/TOPO-->", idx, re.S).group(0)
rodape = re.search(r"<!--RODAPE-->.*?<!--/RODAPE-->", idx, re.S).group(0)
caixa = re.search(r'<div class="foto-grande".*?</div>\n', idx, re.S).group(0)
scripts = '<script src="assets/site.js?v=20261028"></script>'


def head_de(titulo, descricao):
    h = re.sub(r"<title>.*?</title>", f"<title>{titulo}</title>", head)
    h = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{descricao}">', h)
    h = re.sub(r'<link rel="preload" as="image"[^>]*>\n', "", h)
    return re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", h, flags=re.S)


CATS = [("todos", "Todos"), ("fox", "Efeito Fox"), ("egipcio", "Volume Egípcio"), ("brasileiro", "Volume Brasileiro"),
        ("volumoso", "Volumoso"), ("anime", "Efeito Anime"), ("sobrancelha", "Sobrancelhas")]
filtros = "\n".join(f'      <button type="button" data-cat="{c}" aria-pressed="{str(c == "todos").lower()}">{n}</button>' for c, n in CATS)

trabalhos = f"""{head_de("Trabalhos · Fernanda Mello Beauty", "Resultados de extensão de cílios e design de sobrancelhas da Fernanda Mello, lash designer em Carapicuíba.")}<body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
{topo}

<main id="conteudo">
<section class="pagina-topo">
  <div class="caixa">
    <p class="chapeu entra" style="--d:0">Trabalhos</p>
    <h1 class="entra" style="--d:1">Olhares feitos aqui</h1>
    <p class="entra" style="--d:2">Clientes reais, fotografadas no estúdio logo depois do atendimento. Filtre pelo estilo que você quer ver.</p>
  </div>
</section>
<section class="secao" style="padding-top:20px">
  <div class="caixa">
    <div class="filtros" role="group" aria-label="Filtrar por estilo">
{filtros}
    </div>
    <div class="grade">
<!--GRADE-->
<!--/GRADE-->
    </div>
    <p class="centro"><a class="btn" href="./#agendar">Agendar o meu horário</a></p>
  </div>
</section>
</main>

{rodape}

{caixa}
{scripts}
</body>
</html>
"""

nao = f"""{head_de("Página não encontrada · Fernanda Mello Beauty", "Página não encontrada.")}<body>
{topo}
<main id="conteudo">
<section class="pagina-topo" style="min-height:70svh;display:flex;align-items:center">
  <div class="caixa">
    <p class="chapeu">Erro 404</p>
    <h1>Esta página não existe</h1>
    <p>O endereço pode ter mudado. Os estilos, valores e o agendamento estão na página inicial.</p>
    <p style="margin-top:32px"><a class="btn" href="./">Voltar ao início</a></p>
  </div>
</section>
</main>
{rodape}
{scripts}
</body>
</html>
"""

(RAIZ / "trabalhos.html").write_text(trabalhos, encoding="utf-8")
(RAIZ / "404.html").write_text(nao, encoding="utf-8")
print("trabalhos.html e 404.html")
