# Protocolo científico de longa duração — versão 1.0

## Objetivo e epistemologia

MS 408 permanece sem decifração consensual. Competem hipóteses de língua
natural, cifra homofônica/verbosa, texto gerado, escrita mista e sistemas de
abreviação. O laboratório busca **previsões verificáveis**, não narrativas
sedutoras. Um p-valor baixo NÃO decifra nenhuma palavra.

## Pipeline obrigatório

1. Adquirir fontes primárias e derivadas, registrar licença, DOI/URL, data
   UTC, SHA-256, extensão, versão e código de localização física.
2. Distinguir: OBSERVED (imagem verificável), TRANSCRIBED (leitura humana),
   MEASURED (computação reproduzida), INFERRED (dependente de modelo),
   SPECULATIVE, REFUTED e EXTERNALLY_REPLICATED.
3. Formular hipótese falsificável, previsão numérica e falsificadores ANTES
   de análise confirmatória. A descoberta exploratória deve ser rotulada.
4. Definir controle negativo plausível (não apenas embaralhamento ingênuo),
   hipótese nula, efeito esperado, família de testes, poder e tamanho.
5. Congelar holdout por fólio/caderno; ajustar apenas em treino. Nunca usar
   o mesmo folio para treino e validação; avaliar vazamento por vizinhança.
6. Registrar commit, dependências, seeds, hash de entrada, comando e output;
   conservar também tentativas sem efeito e resultados contraditórios.
7. Replicar em transcrição alternativa, políticas de leitura incerta,
   divisão por gênero, mão, caderno e versão, apontando confundidores.
8. Revisão adversarial independente: refazer código, auditar estatística,
   verificar leitura em imagens e tentar refutar a conclusão.

## Estatística

- Para inferência A/B usar permutações em nível de página ou quire,
  não de token; estratificar por escriba/posição/gênero se identificável.
- Reportar tamanho de efeito, IC por bootstrap hierárquico e amostras nulas.
- Controlar seleção múltipla por Holm/BH e declarar escolhas pós-hoc.
- Analisar independência entre registros, folios próximos e transcritores.
- Modelos de língua/cifra/gerador devem receber o MESMO orçamento de
  treinamento e teste oculto, com ablações e baselines fortes.

## O que seria evidência de decifração

Um mecanismo de leitura com regras estáveis, aplicado cegamente a páginas
novas, produz texto coerente, explicações morfológicas/linguísticas
historicamente plausíveis e correspondência visual verificável, acima de
controles aleatórios e sem exceções inventadas para cada exemplo. Requer
revisão por linguistas, paleógrafos e historiadores externos.
Sem isso, é HYPOTHESIS, nunca SOLUTION.

## Governança

Ideias novas: agents/new_fronts; execução: experiments/runs; hipóteses:
hypotheses/HNNN.md; revisões em PR/Issues; DOI e backups externos como
trabalho futuro. Autores de dados e imagens devem ser creditados.

