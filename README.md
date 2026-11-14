# Voynich Research Lab — BrasALabs

Laboratório científico aberto, reproduzível e de longo prazo dedicado ao **Manuscrito Voynich (Beinecke MS 408)**.

> **Status (14 nov 2026): não há decifração comprovada.** Uma regularidade
> estatística, correspondência visual ou narrativa plausível não representa
> uma tradução. Cada conclusão precisa ser falsificável e reproduzível.

## Edição digital interativa (novo)

**[Abrir o site Voynich Codex](https://voynich-codex-two.vercel.app/)** · [Código do leitor](web/) · [Protocolo editorial](digital-edition/) · [Projeto de glifos e fonte](digital-edition/GLYPHS_AND_FONT.md).

A primeira versão oferece o acervo original de **213 canvases IIIF de Yale** em alta resolução com zoom, índice por fólio e notas exportáveis. Transcrições IVTFF podem ser importadas localmente sem redistribuição automática da obra moderna de terceiros. A nova fonte Voynich exige amostras reais, vetorização com rastreabilidade e revisão humana; ainda não foi construída. As 213 imagens do acervo não equivalem a 214 páginas do PDF nem aos identificadores das transcrições.

## Acesso ao manuscrito e estudos

- **[PDF integral na GitHub Release](https://github.com/brasalabs6/voynich/releases/tag/ms408-yale-2002046-v1)**. PDF institucional Yale de 214 páginas e 118.428.581 bytes, preservado sem recompressão, com [hash SHA-256 e fonte](manuscript/SHA256.md). A Release contorna o limite de 100 MB por arquivo Git. Não é o número de fólios físicos.
- **[Fontes e transcrições](data/SOURCES.md)**, incluindo ZL3b e IT2a em EVA/IVTFF; são obtidas localmente, sem redistribuir automaticamente textos de terceiros.
- **[Protocolo científico](docs/PROTOCOL.md)**, [roteiro de 24h e continuidade](docs/ROADMAP.md) e [bibliografia crítica](docs/LITERATURE.md).
- **[14 hipóteses falsificáveis](hypotheses/INDEX.md)**, [novas frentes para agentes](agents/new_fronts/INDEX.md), [backlog e handoff](agents/README.md), [issues](https://github.com/brasalabs6/voynich/issues).
- **[Experimentos e relatórios](experiments/runs/)** e [snapshots numéricos com proveniência](results/snapshots/); [CI reproduzível](https://github.com/brasalabs6/voynich/actions).

## Evidências iniciais em 14 nov 2026

1. **Auditoria do parser:** fRos, página especial das Rosetas, estava ausente na primeira execução; correção adicionou 160 registros, elevando a 5.385 loci ZL3b. Implementação e teste de regressão publicados.
2. **Currier A/B:** distância de Jensen-Shannon de sufixos EVA em torno de 0,104 bits, porém **zero estratos comparáveis para (mão, quire)**; esse desenho não identifica línguas distintas.
3. **Posição do sufixo EVA dy:** em parágrafos, efeito do fim de linha positivo em A e negativo em B em ambas as transcrições; contraste B−A ~−0,12. Reamostragem por página e quire com 999 repetições manteve sinal negativo; não se atribui causa, língua ou tradução.
4. **[Experimento executado e auditável](experiments/runs/2026-11-14-H001-H002-confounds-bootstrap.md)**. [GitHub Actions passou](https://github.com/brasalabs6/voynich/actions/runs/43604521195).

## Reprodução do laboratório

Python 3.11+ e conexão para obter transcrições das fontes originais:

    python -m pip install -e .
    python -m unittest discover -s tests -v
    python scripts/fetch_data.py --out data/raw
    voynich-lab analyze --input data/raw/ZL3b-n.txt --output results/tmp/zl3b.json
    python scripts/audit_confounds.py --input data/raw/ZL3b-n.txt --output results/tmp/zl3b_confounds.json
    python scripts/bootstrap_line_effect.py --input data/raw/ZL3b-n.txt --output results/tmp/zl3b_contrast.json --repetitions 999

O CI roda em push, pull request, manualmente e semanalmente. O script de
arquivamento do PDF verifica páginas e hash e publica o arquivo como asset
de Release. **Automações não equivalem a pesquisa contínua autônoma:**
novas ideias requerem trabalho e validação verificáveis a cada rodada.

## Para outros pesquisadores ou agentes

Leia [AGENTS.md](AGENTS.md) e [CONTRIBUTING.md](CONTRIBUTING.md).
Registrar cada hipótese emergente em agents/new_fronts com previsão,
controles, critério de rejeição, orçamento e delegação. Guardar código,
entradas com SHA-256, seeds, resultados negativos, métricas, erros e
revisão adversarial. Evitar vazamentos de holdout e confundir EVA com
texto traduzido. Scripts e documentação originais: MIT; manuscrito e
transcrições de terceiros: direitos próprios, veja data/SOURCES.md.

Instituição: [Yale Beinecke MS 408](https://collections.library.yale.edu/catalog/2002046).
