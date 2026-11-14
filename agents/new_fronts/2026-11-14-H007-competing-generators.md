# Frente emergente: discriminação conjunta de mecanismos concorrentes

**Issue:** https://github.com/brasalabs6/voynich/issues/3
**Status:** NÃO TESTADO. Motivo: artigos revisados apresentam tanto gerador
por autocitação quanto cifra homofônica com propriedades parecidas com
a escrita Voynich. Ajustar uma métrica isolada não discrimina mecanismos.

**Experimento proposto:** comparar (a) gerador auto-citação de Timm/Schinner,
(b) Naibbe/cifra manual reversível, (c) Markov e (d) permutação por página,
sob mesmo orçamento de ajuste. Congelar treino por quire e testar distribuição
multivariada: frequência/rank, comprimento de palavra, autocorrelação
espacial, padrões de início/fim, diferenças A/B e variação de mão.

**Critério de aceite:** >=4 métricas pré-registradas, seeds e parâmetros
fixos antes do holdout, curva de tradeoffs, resultados negativos salvos.

**Falha:** não reproduzir vetor conjunto em páginas ocultas ou depender
de parametrização ad hoc. Mesmo sucesso não prova o mecanismo histórico.

