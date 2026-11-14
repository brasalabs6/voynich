# RUN-20261114-001 — Baseline exploratório ZL3b versus IT2a

**Estado:** EXECUTADO e CI passou; **NÃO CONFIRMATÓRIO** e **NÃO É DECIFRAÇÃO**.
Pipeline: https://github.com/brasalabs6/voynich/actions/runs/43603783560
Código testado: b92a38ab2b6059a559f4ef424a0d4693418e6dab
Data UTC: 2026-11-14. Python 3.11. Randomização 199 iterações, sementes 408/409.
Artifact da execução: exploratory-statistics (na Actions; expira).

## Proveniência

- ZL3b-n.txt, 411671 bytes; SHA-256:
  bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
- IT2a-n.txt, 342104 bytes; SHA-256:
  7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5
- Dados obtidos pelo pipeline de https://www.voynich.nu/data
- Regra: excluir fragmentos EVA ambíguos; dividir ponto e vírgula como espaço
  incerto (na realidade a decisão atual divide em vírgula e ponto).
  Corrigir interpretação nesta frase: tanto vírgula quanto ponto são
  tratados como quebra de palavra; não é a política oficial IVTT.

## Resultados efetivamente computados

| Medida | ZL3b | IT2a |
|---|---:|---:|
| Loci | 5385 | 5215 |
| Páginas/lados IVTFF | 227 | 225 |
| Tokens EVA conservadores | 37608 | 37759 |
| Fragmentos excluídos | 1418 | 160 |
| Types EVA | 7457 | 8026 |
| Entropia por caractere EVA (bits) | 3.862595 | 3.861128 |
| H001 JS sufixo-2 A/B (bits) | 0.10442809 | 0.10481095 |
| H001 p Monte Carlo, permutação de página | 0.005 | 0.005 |
| H002 diferença final - meio para sufixo dy | -0.02584689 | -0.03086627 |
| H002 p Monte Carlo, permutação por locus | 0.005 | 0.005 |

H001: essa associação entre classes A/B não demonstra duas línguas, pois
mãos, seção, quire e comprimento podem confundir. Unidade permutada: página
IVTFF. H002: **efeito negativo**, isto é, nesta definição o sufixo dy fica
menos frequente nos finais do que no interior, comparado com a diferença
observada. Isso NÃO se traduz em significado semântico.

Com 199 permutações, p=0.005 é o limite inferior resolúvel, não deve ser
anunciado como evidência mais precisa. Nenhum intervalo de confiança
hierárquico ou correção de multiplicidade foi concluído.

## Auditoria de versão importante

Primeira execução https://github.com/brasalabs6/voynich/actions/runs/43603340638
usava regex de fólio comum e omitia fRos: 5225 loci ZL e 37116 tokens.
A correção acrescentou **160 loci da página das Rosetas**, +492 tokens e
passou a 5385 loci, 227 páginas/lados. O teste de regressão test_rosettes.py
impede reincidência. A execução anterior não é válida como versão completa.

## Próximos falsificadores

1. Repetir H001 com bloqueio de mão/quire e apenas estratos sobrepostos.
2. Repetir H002 excluindo labels/círculos, linhas curtas e incertezas.
3. Aumentar permutações, estimar IC hierárquico, corrigir escolhas múltiplas.
4. Reproduzir contagens com IVTT oficial e outros leitores; exigir cobertura.

