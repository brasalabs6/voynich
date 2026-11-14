# Site: Voynich Codex (primeira versão)

Origem: web/index.html, web/style.css, web/app.js.
Índice documental: web/data/folios.json, gerado com
scripts/build_digital_edition.py de Yale IIIF e versionado via CI.

O projeto está hospedado na Vercel, conectado a main, pasta raiz web.
Site público: https://voynich-codex-two.vercel.app/

### Teste local

    python -m http.server 8000 -d web

Acesse http://localhost:8000. O site requer acesso de rede à Yale para
imagens de alta resolução e ao OpenSeadragon CDN para zoom em mosaicos.
Se o visualizador de mosaicos falhar, oferece imagem original de fallback.

### Funcionalidades atuais

- Lista as 213 digitalizações de Yale, incluindo capas e fólios.
- Pesquisa nomes, navega com setas e permite zoom IIIF em alta resolução.
- Preserva URL da fonte e deixa abrí-la diretamente.
- Importa arquivo IVTFF original localmente e mostra registros associados
  ao fólio. A importação preserva as leituras incertas literalmente;
  EVA não é tradução ou representação vetorial precisa.
- Notas locais por fólio, com exportação JSON e hash do manifesto original.
- Guia de trabalho para futuro atlas de glifos e fonte paleográfica.

### Limitações ainda abertas

- Nem toda unidade EVA corresponde à uma imagem IIIF de mesmo nome,
  especialmente as Rosetas e foldouts; faltam alinhamentos verificáveis.
- O índice registra a ordem/etiquetas de Yale; NÃO ajusta contagem de
  fólios para corresponder a 214 páginas PDF ou 227 locais IVTFF.
- Ainda não há uma fonte própria nem transcrição manual completa e
  validada. O site não gera arte falsa para preencher lacunas.

A investigação científica continua em docs/PROTOCOL.md e
digital-edition/GLYPHS_AND_FONT.md.

