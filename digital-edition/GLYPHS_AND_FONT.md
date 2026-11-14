# Como construir uma fonte Voynich sem falsear o manuscrito

## Natureza do problema

EVA é transliteração com convenções de ligadura; não se deve tratar cada
letra latina EVA como um sinal físico único. Algumas sequências como ch,
sh, cth, ckh, cph, cfh envolvem unidades e conexões debatidas. Variações
entre escreventes, tamanhos, posicionamento e marcas de correção importam.

Fontes EVA criadas anteriormente são trabalhos de terceiros e podem
impor restrições: NÃO copiar arquivos de fontes nem seus contornos no
repositório sem autorização clara. Usar espécimes reais de Yale com créditos
e regras de reutilização documentadas.

## Banco de espécimes com cadeia de custódia

Cada entrada precisa:
- ID imutável: GLYPH-SPECIMEN-NNNN.
- URL exata do serviço IIIF e canvas, fólio, número da linha e contexto.
- Caixa delimitadora x,y,w,h em pixels da imagem original.
- SHA-256 do recorte produzido; dimensões; data, versão e script.
- Categoria de glifo PROPOSTA, não verdade; alternativas e incertezas.
- Escriba/mão quando identificável; fonte da classificação.
- Identidades dos revisores e consenso; decisões e desacordos arquivados.
- Arquivos SVG derivados versionados, com link para o recorte fotográfico.

Processamento: scripts/glyph_extract.py aceita anotações com coordenadas e
baixa recortes diretos dos serviços IIIF da Yale (sem inventar glifos).
Conjuntos aprovados por dois revisores são pré-requisito para produção.

## Tipografia

- Guardar contorno SVG de cada variante, preservando a forma observada;
  distinguir traços da pena de manchas, desgaste e textura do suporte.
- Planejar unidades internas por categorias de glifos, não limitar-se ao
  teclado QWERTY nem forçar ligações EVA 1:1.
- Usar OpenType GSUB para ligaduras e alternantes contextuais; mapear
  teclas de entrada apenas como interface. Guardar alfabetos/catálogos
  separados das regras hipotéticas de transliteração.
- Criar famílias para mãos distintas se for necessário; jamais afirmar
  que uma fonte digital substitui as múltiplas grafias históricas.
- Empregar escala e métrica ligadas ao fac-símile: linha base, tamanho,
  espaçamento e deslocamento devem ser testados fólio a fólio.
- Comparar renderização digital com pixels originais usando métricas
  de distância/contorno e avaliação cega de especialistas.

## Níveis de fidelidade

A: fac-símile da fotografia de Yale, sem alteração (fonte de verdade).
B: caracteres vetoriais desenhados a partir de recortes verificados.
C: reconstrução editorial de palavras, com variantes e correções explícitas.
D: interpretações semânticas e traduções hipotéticas. D nunca se torna A.

Jamais usar geração por IA para restaurar conteúdo ilegível sem marcar
visivelmente como simulação, preservando a foto original disponível.

