# A cópia integral do Manuscrito Voynich

O original é o **Beinecke MS 408**, Yale University.
Catálogo: https://collections.library.yale.edu/catalog/2002046

PDF de 214 páginas:
https://collections.library.yale.edu/pdfs/2002046.pdf

Espelho:
https://archive.org/download/voynich_MS_408/voynich.pdf

Manteremos a cópia **integral em PDF sem modificar** como ativo de GitHub Release:
https://github.com/brasalabs6/voynich/releases/tag/ms408-yale-2002046-v1

A Release contém o PDF original e manifest.json (URL efetiva, SHA-256, bytes,
páginas). O fluxo que tenta gerar a Release é:
https://github.com/brasalabs6/voynich/actions/workflows/archive-manuscript.yml

A Release NÃO deve ser considerada existente até a execução do workflow ter
sido concluída com sucesso. Em caso de bloqueio por Yale e Archive.org,
anotar falha e pedir ao mantenedor o upload manual; NUNCA simular download.

**Por que GitHub Releases?** O PDF tem mais de 100 MB, ultrapassando o limite
de um arquivo Git. GitHub Releases aceita arquivos maiores e faz parte do
acervo do repositório. Não reduzir ou recomprimir o manuscrito para disfarçar
a limitação. O arquivo da Release é a cópia, e o código do Git é o método
reproduzível de aquisição/verificação.

Verificação independente: instalar pypdf; executar
python scripts/archive_manuscript.py; comparar manifest.json e sha256sum.
214 páginas de PDF não são 214 folhas físicas nem 214 fólios.

