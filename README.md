# Identificador e Classificador de Subgrafos de Rede

**Juliana Lombard Souza**

Este algoritmo foi desenvolvido para analisar redes de linhas (como redes viárias, hidrográficas, etc.) representadas por um shapefile. Ele identifica as partes da rede que estão desconectadas umas das outras, classifica cada parte como um "subgrafo" e gera um novo arquivo shapefile e um mapa visual para facilitar a análise.

## Funcionalidades

*   Carrega uma rede de um arquivo shapefile de linhas.
*   Realiza a limpeza e correção de geometrias inválidas ou nulas.
*   Constrói um modelo de grafo da rede usando a biblioteca `networkx`.
*   Identifica o componente principal (a maior parte contínua da rede).
*   Identifica e classifica todos os outros componentes desconectados como subgrafos.
*   Adiciona uma nova coluna `subgrafo` ao arquivo de dados, onde:
    *   `0` representa a rede principal.
    *   `1`, `2`, `3`, ... representam os subgrafos desconectados (hierarquizados pelo tamanho da rede).
*   Salva o resultado em um novo shapefile na pasta `output`.
*   Gera e salva um mapa colorido (`.png`) que visualiza cada subgrafo com uma cor diferente.
*   Exibe um resumo no console com a quantidade de trechos em cada subgrafo.

## Pré-requisitos

Antes de executar o script, certifique-se de ter o Python 3.x e as seguintes bibliotecas instaladas. Você pode instalá-las usando o `pip`:

```bash
pip install geopandas networkx matplotlib
```

> **Nota:** A biblioteca `pathlib` já vem incluída na instalação padrão do Python.

## Como Usar

Siga os passos abaixo para configurar e executar o script em sua máquina.

### 1. Estrutura do Projeto

Organize seus arquivos da seguinte forma. O script espera encontrar o arquivo de dados na pasta `data` e criará a pasta `output` automaticamente, se ela não existir.

```
meu_projeto_rede/
├── data/
│   └── rede_teste_lin.shp  # <-- Coloque seu arquivo shapefile aqui
├── output/
│   └── (será criada automaticamente pelo script)
└── scripts/
    └── subgrafos.py  # <-- O seu script Python
```

### 2. Preparar os Dados

1.  Coloque seu arquivo shapefile da rede (ex: `rede_teste_lin.shp`) e todos os arquivos associados (`.shx`, `.dbf`, etc.) dentro da pasta `data`.
2.  Verifique se o nome do arquivo no script corresponde ao seu arquivo. A linha a ser alterada está no início do script:

    ```python
    # IMPORTANTE: Certifique-se de que todos os arquivos do shapefile (.shp, .shx, .dbf, etc.)
    # estão na pasta 'data'.
    rede_shp = DATA_DIR / "rede_teste_lin.shp" # renomeie aqui
    ```

### 3. Executar o Script

Abra o terminal ou prompt de comando, navegue até a pasta `scripts` e execute o script com o seguinte comando:

```bash
python subgrafos.py
```

### 4. Verificar os Resultados

Após a execução, verifique a pasta `output`. Você encontrará:

*   `rede_teste_subgrafos_lin.shp`: Uma cópia do seu shapefile original, mas com uma nova coluna chamada `subgrafo` contendo a classificação.
*   `mapa_subgrafos.png`: Uma imagem do mapa onde cada subgrafo está pintado com uma cor diferente, facilitando a identificação visual.
*   **Resumo no Terminal:** O script também imprimirá no terminal um resumo da classificação, mostrando quantos trechos de linha existem em cada subgrafo.

---

## 🔬 O que são Subgrafos?

Um subgrafo é definido como um grafo que é um subconjunto de outro grafo, compartilhando alguns ou todos os seus vértices e arestas.

Este script automatiza a tarefa de encontrar subgrafos em seus dados, o que é extremamente útil para:

*   Identificar erros de digitalização (onde uma rua deveria se conectar, mas não o faz).
*   Analisar a fragmentação de redes de infraestrutura.
*   Separar sistemas que são fisicamente independentes.

A coluna `subgrafo` criada pelo script permite que você realize análises posteriores, como filtrar ou estilizar cada parte da rede de forma independente em um SIG (Sistema de Informação Geográfica).

## Licença/Citação

MIT License 

Citation: SOUZA, J.L. (2026) Identificador e Classificador de Subgrafos de Rede [Data set]. Zenodo. https://doi.org/10.5281/zenodo.19133714