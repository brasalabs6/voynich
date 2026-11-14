# Frente emergente: colinearidade Currier × mão × quire

**Issue:** https://github.com/brasalabs6/voynich/issues/2
**Status:** PREPARADO; teste estratificado PENDENTE.
**Motivação observada:** diferença de sufixos A/B nas duas transcrições:
Jensen-Shannon ~0.104 bits, permutação por página p=0.005 em 199 sorteios.
O resultado depende dos rótulos de origem e não controla mão ou assunto.

**Pergunta falsificável:** diferença A/B é identificável quando a mão e
quire são mantidos fixos, nos estratos de sobreposição real?

**Plano:** tabela cruzada de etiquetas por mão, caderno e ilustração;
diagrama de contiguidade; permutação por bloco e regressão regularizada
com efeito hierárquico; só inferir se houver suporte nos estratos.
Confrontar ZL/IT, seções e políticas de tokens incertos.

**Critério de refutação:** ausência de sobreposição, colinearidade perfeita,
ou efeito sem robustez em holdout. Ausência de identificabilidade não é
prova de igualdade entre A/B.

**Prioridade:** P0. **Dependências:** B001; IVTT e mapeamento cadernos.
**Saída:** notebooks/scripts, matrizes, incerteza, testes e resultado nulo.

