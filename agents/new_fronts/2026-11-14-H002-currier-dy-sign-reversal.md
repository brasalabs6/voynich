# H002 — Contraste de sinal de dy entre A/B

**Status:** observado em duas transcrições e verificado pelo CI; o mecanismo
continua DESCONHECIDO. **Issue:** https://github.com/brasalabs6/voynich/issues/6

**Anomalia registrada:** em parágrafos, dy em última posição menos posições
interiores é positivo em A e negativo em B: ZL A +0.05745/B -0.06200,
IT A +0.05388/B -0.07031. Os intervalos 95% de bootstrap de quire do
contraste B−A não cruzam zero. Fonte e limites:
experiments/runs/2026-11-14-H001-H002-confounds-bootstrap.md.

## Hipóteses concorrentes, para outros agentes

- **Layout e geometria:** contraste diminuirá após reanalisar apenas linhas
  homogêneas por comprimento, tipo de parágrafo, fim de página e posição.
- **Mão/quire/tema:** contraste segue mão ou gênero visual; verificar
  condições de estimabilidade ANTES do teste. O baseline não tem estratos
  simultaneamente comparáveis por mão + quire.
- **Cifra com regras de padding:** modelos simples de cifra reproduzem o
  contraste e outras métricas quando parâmetros são congelados.
- **Gerador por autocitação:** modelos de auto-cópia podem produzir a mesma
  regularidade sem informação semântica.
- **Transcrição:** política alternativa de leitura incerta, fronteira de
  palavra e fonte IVTFF muda o sinal ou magnitude.

## Testes e falsificadores

Prioridade alta, tarefas para agente com revisão adversarial:
congelar holdout por quire, selecionar medidas primárias sem consultar
validação, gerar controles nulos plausíveis, testar ambos transcritores
e conferir imagens de amostra. Critério de refutação: contraste desaparece
em amostra oculta, depende da normalização, ou simulações concorrentes o
reproduzem sem parâmetros ad hoc. Nenhum achado isolado é decifração.
