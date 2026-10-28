# Fernanda Mello Beauty · Lash Designer

Site da Fernanda Mello ([@fernandamellobeauty](https://www.instagram.com/fernandamellobeauty/)), lash designer e designer de sobrancelhas em Carapicuíba (Colinas do Anhanguera), SP.

Publicado em https://azeugral.github.io/fernanda-mello/ (com `noindex` até a aprovação).

## Páginas

- `index.html`: hero com o logo oficial e fios de luz, frase dela, os 8 estilos de cílios com valores de aplicação e manutenção (7/14/21 dias), manutenção x nova aplicação, sobrancelhas, 12 trabalhos, sobre, política de agendamento e formulário que monta a mensagem para o WhatsApp (11) 91677-7797.
- `trabalhos.html`: 30 fotos em grade 4:5 com filtro por estilo e foto ampliada.
- `404.html`

## Identidade

Tirada do catálogo dela no Canva (capa com o monograma FM) e do Instagram:
preto `#0a0708`, champanhe/dourado `#d9b58f` do monograma, rosa `#e2477f` do "BEAUTY" e violeta dos fios de luz.
Cormorant Garamond nos títulos e Jost no texto. Fotos dos estilos em cápsula, como no catálogo.
O logo é a arte original recortada da capa (`tools/logo.py`), não foi redigitado.
O fundo do hero é um shader (`assets/fios.js`) ao vivo no desktop e um MP4 em loop no celular (`tools/gerar_fios.py`).

## Ferramentas

```
python -I tools/logo.py        # logo.png, logo-fm.png e favicons a partir de ../_ref/canva/canva-01-p1.jpg
python -I tools/paginas.py     # monta trabalhos.html e 404.html com o topo/rodapé do index
python -I tools/processar.py   # recorta as fotos de ../_ref (ig e canva) e injeta as grades
python -I tools/gerar_fios.py  # MP4 do hero para o celular (--teste salva só quadros)
python -I tools/og.py          # prévia de link (og.jpg)
```

Ao mudar CSS, JS ou vídeo, subir o `?v=` nas páginas.

## CONFIRMAR antes do domínio

- [ ] **Unhas**: o pedido falou em nail designer, mas o perfil e o catálogo são de lash designer (cílios e sobrancelhas). O post "Nail & Lash Designer" mostra a **Fantay** fazendo unhas no mesmo espaço; o site cita isso numa frase do "Sobre". Ela quer uma seção de unhas (com serviços e valores da Fantay) ou é só a menção?
- [ ] **Fotos dos estilos Classic e Sirena**: vieram do catálogo do Canva (baixa resolução). As outras são do Instagram, escolhidas pela legenda. Confirmar se cada foto mostra mesmo o estilo do cartão.
- [ ] **Spikes Fox**: post de 22/09 diz "disponível no catálogo", mas o catálogo do Canva não tem esse estilo nem valor.
- [ ] **Valores**: copiados do catálogo do Canva (out/2026). Conferir se continuam valendo.
- [ ] **Endereço**: só "Colinas do Anhanguera, Carapicuíba". Quer rua/número e mapa, ou só o bairro (endereço enviado no agendamento)?
- [ ] **Dias e horários** de atendimento (um post fala de "domingo de atendimento").
- [ ] **Instagram**: o catálogo traz @fernandamello_beautystyle e @fernandamello__beauty; o site usa o perfil atual, @fernandamellobeauty.
- [ ] **Sinal de R$ 50**: forma de pagamento (Pix?) para citar no site.
- [ ] Uso das fotos das clientes (todas marcadas nos posts dela).
- [ ] Domínio (sugestão: fernandamellobeauty.com.br) e remover o `noindex`.

Site por [L R G Z](https://lrgz.com.br).
