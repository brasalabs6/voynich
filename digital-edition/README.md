# Edição Digital Crítica do Manuscrito Voynich

## Decisão editorial

O site não tenta recriar o original por desenho generativo. A autoridade da
edição é a fotografia de Yale com o máximo de detalhe possível via IIIF.
Qualquer extração de texto, vetorização, fonte digital ou "folha limpa" é
uma **camada derivada identificável**, que pode ser corrigida ou removida.

A primeira implementação está em web/ e foi publicada pelo projeto
Vercel voynich-codex, vinculado ao repositório brasalabs6/voynich.

### Quatro camadas independentes

1. ORIGINAL: 213 canvases IIIF de Yale, capa, folhas e detalhes; atribuição,
   ordem e dimensões; cada serviço de zoom aponta à imagem institucional.
2. TRANSCRIÇÃO: leituras EVA/IVTFF humanas, com versão, autor, posição,
   variantes e zonas de incerteza. Não é a mesma coisa que o original.
3. ATLAS DE GLIFOS: recortes indexados por fólio/linha/caixa de pixels,
   categorias propostas, concordância entre revisores e variantes de mão.
4. FONTE E RECONSTRUÇÃO: vetores e OpenType com proveniência por glifo,
   apresentados como hipótese paleográfica experimental, nunca como fac-símile.

## Fluxo para uma réplica rigorosa

- Primeiro manter link direto para o original e criar índice do documento.
- Depois alinhar cada fólio IIIF ao identificador correto da transcrição
  (a ordem de 213 imagens NÃO corresponde automaticamente a todos os 227
  identificadores EVA, em especial foldouts, detalhes e fRos).
- Transcrever linha por linha com método duplo cego, marcando dúvida e
  distância entre transcritores. Usar fotografias para verificação.
- Criar catálogo de espécimes de glifos com quadriláteros localizados nas
  imagens, preservando ligaduras/traços de cada mão.
- Só então criar contornos vetoriais e fonte específica da mão, comparando
  reconstrucões por sobreposição e distância visual.
- Validar reprodução contra páginas não usadas na criação da fonte.

## Estado atual

Feito: acervo original completo em PDF (GitHub Release), índice IIIF
verificado com 213 imagens, leitor com zoom, navegação, importação local IVTFF,
notas, pipeline automático, estrutura editorial e protocolo para pesquisa.

Não feito: transcrição manual independente de cada linha, bounding boxes
de todos os glifos, revisão dupla, fonte própria historicamente validada,
renderização vetorial completa de todas as páginas. Não inventar esse
progresso.

Consulte GLYPHS_AND_FONT.md, TRANSCRIPTION.md e web/README.md.

