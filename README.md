# Voynich Research Lab — BrasALabs

Laboratório aberto, reprodutível e de longo prazo dedicado ao **Manuscrito Voynich (Beinecke MS 408)**.

> **Estado científico (2026-11-14):** não há decifração comprovada e aceita. Nenhum resultado estatístico, correspondência visual ou sugestão de IA deve ser anunciado como tradução sem validação independente.

## Comece por aqui

1. [Protocolo científico](docs/PROTOCOL.md) e [plano de pesquisa](docs/ROADMAP.md).
2. [Fontes e direitos](data/SOURCES.md); [acervo fac-símile em PDF](manuscript/README.md).
3. [Hipóteses testáveis](hypotheses/INDEX.md) e [tarefas para agentes](agents/README.md).
4. [Ferramenta de análise](src/voynich_lab/) e [resultados](experiments/README.md).

## Reprodutibilidade

Requisitos: Python 3.11+; sem dependências externas para o núcleo de métricas.

```bash
python scripts/fetch_data.py --out data/raw
python -m voynich_lab.cli analyze --input data/raw/ZL3b-n.txt --output results/analysis_zl3b.json
python -m unittest discover -s tests -v
```

Para funcionar com `python -m voynich_lab.cli`, use `PYTHONPATH=src` ou `python -m pip install -e .`.

**Importante:** arquivos de origem obtidos de terceiros, modelos grandes e PDFs >100 MB não entram diretamente no Git. Veja [manuscript/README.md](manuscript/README.md) para arquivamento fracionado. O fluxo de arquivamento da íntegra também exige verificação de execução.

## Rigor e governança

- Análise confirmatória exige pré-registro e hipóteses falsificáveis antes de inspecionar resultados.
- Registrar também fracassos e hipóteses refutadas.
- Identificar transcrição, versão, divisão de treinamento/teste, semente aleatória, código e hash.
- Separar **rascunho por IA**, **evidência reproduzida**, **revisão independente** e **decifração aceita**.
- Nunca treinar e avaliar no mesmo conjunto sem separação ou correção explícita.
- Cada agente deve usar [AGENTS.md](AGENTS.md) e abrir PR; alterações de dados primários ou inferências sem evidência devem ser contestadas.

Material histórico: Yale Beinecke MS 408, https://collections.library.yale.edu/catalog/2002046
