# RUN-20261114-002 — Currier A/B, covariáveis e posição de sufixos

**Data:** 2026-11-14. **Estado:** EXECUTADO / EXPLORATÓRIO / NÃO CONFIRMATÓRIO; **NÃO É DECIFRAÇÃO**.

## Proveniência verificável
- CI executado com sucesso: https://github.com/brasalabs6/voynich/actions/runs/43604521195
- Commit que gerou os dados: b3c8d02626e0b8b491cfaa741c81606e8414e4ba
- Artefato no CI: exploratory-statistics, com zl3b_confounds.json, it2a_confounds.json, zl3b_contrast.json, it2a_contrast.json e provenance.json.
- ZL3b-n.txt: 411671 bytes, SHA-256 bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
- IT2a-n.txt: 342104 bytes, SHA-256 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5
- Ambiente GitHub Actions Ubuntu + Python 3.11; bootstrap 999 reamostragens (seed 408); permutação 199.
- Reproduzir após instalar projeto e obter os dados locais com scripts/fetch_data.py:
  - python scripts/audit_confounds.py --input data/raw/ZL3b-n.txt --output results/tmp/zl3b_confounds.json
  - python scripts/bootstrap_line_effect.py --input data/raw/ZL3b-n.txt --output results/tmp/zl3b_contrast.json --repetitions 999
  - repetir para IT2a.

## Auditoria de identificabilidade

| Métrica | ZL3b | IT2a |
|---|---:|---:|
| Identificadores de página IVTFF | 227 | 225 |
| Etiquetadas Currier A | 114 | 114 |
| Etiquetadas Currier B | 83 | 82 |
| Estratos conjuntos mão+quire contendo A e B | **0** | **0** |
| Páginas em estratos comuns por mão apenas | 30 (2 A e 28 B) | 30 (2 A e 28 B) |
| Quires distintos no bootstrap | 14 | 14 |

**Implicação:** não é identificável uma diferença Currier A/B independente dos dois confundidores mão e quire neste desenho. Uma divergência estatística pode acompanhar ambos. Não inferir duas línguas.

## Estatística exploratória de posição

Estimativa por grupo = proporção de tokens EVA terminados em dy na posição FINAL da linha, menos proporção de tokens com esse sufixo nas posições INTERIORES. Somente registros de parágrafos (locus P) com três ou mais tokens; não traduzimos dy.

| Medida | ZL3b | IT2a |
|---|---:|---:|
| Loci Currier A elegíveis | 1504 | 1515 |
| Loci Currier B elegíveis | 2443 | 2437 |
| Efeito A | +0.05744566 | +0.05387708 |
| Efeito B | -0.06200112 | -0.07031011 |
| Contraste B menos A | **-0.11944678** | **-0.12418719** |
| IC bootstrap percentil 95%, resampling de páginas | [-0.14560845,-0.09640802] | [-0.14989563,-0.10191876] |
| IC bootstrap percentil 95%, resampling de quires | [-0.17926838,-0.09842756] | [-0.17589347,-0.10119728] |

Os dois ICs de quire permaneceram negativos após 999 sorteios, assim como
as duas transcrições. O IC mede variabilidade sob reamostragem do corpus,
**não identifica causa** nem valida idioma, cifra ou tradução.

Outras classes de locus misturadas induzem resultados diferentes: contagens
ZL P=4130, L=1029, C=84, R=142; IT P=4118, L=883, C=72, R=142. Somente
27 rótulos ZL e 29 IT tinham três ou mais tokens, tornando sua estimativa
instável; não combinar legendas e parágrafos sem estratificação.

## Limitações e próximos falsificadores

1. Resultado exploratório, não pré-registrado. A escolha do sufixo dy e
   política de fronteira podem inflar descoberta; sem correção múltipla.
2. O parser IVTFF não cobre todas as convenções; o ponto (.) e a vírgula (,) são tratados
   como separadores de palavras, dúvidas de EVA descartadas.
3. Em textos históricos, páginas e quires não são amostras aleatórias
   independentes. Bootstrap cluster não resolve confundimento Currier/mão/quire.
4. ZL e IT transcrevem o mesmo objeto: robustez de transcritor não é
   replicação independente.
5. Repetir com IVTT oficial, holdout por quire, efeitos por layout e mão,
   controles geradores/criptográficos, intervalos e revisão adversarial.

Issues: auditoria IVTFF #1; confundidores #2; geradores/cifra #3; hipótese
de posição #6. O código completo está em src/voynich_lab/confounds.py,
src/voynich_lab/contrast.py e scripts/audit_confounds.py,
scripts/bootstrap_line_effect.py. A versão auditável dos valores principais
foi copiada em results/snapshots/2026-11-14-confounds-bootstrap.json.
