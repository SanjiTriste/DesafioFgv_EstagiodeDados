# Desafio FGV — Pipeline de Notícias com Embeddings

Este projeto implementa uma pipeline de processamento de notícias utilizando Processamento de Linguagem Natural (NLP) e embeddings semânticos para permitir buscas por similaridade textual.

A arquitetura foi desenhada para separar as responsabilidades de coleta, tratamento e processamento, mantendo a lógica de serviços dentro de um módulo dedicado e o fluxo de execução principal de forma isolada.

---

## Estrutura do Diretório

```text
DesafioFGV_Estagio/
├── dados/
│   ├── noticias_brutas.json     # Base de dados original
│   ├── dados_limpos.json        # Dados após processamento e limpeza
│   └── embeddings.npy           # Vetores de representação semântica
├── src/
│   ├── service/
│   │   ├── buscar_dados.py      # Módulo de carga de dados
│   │   ├── limpar_dados.py      # Módulo de tratamento de texto e Regex
│   │   └── embeddings.py        # Módulo de geração de vetores
│   └── pipeline.py              # Script principal de execução
├── requirements.txt             # Dependências do projeto
├── .gitignore                   # Arquivos ignorados pelo controle de versão
└── README.md                    # Documentação do projeto

---

## Detalhamento das Etapas

### 1. Limpeza de Dados
Os dados brutos continham ruídos de extração, como tags HTML, entidades de texto e metadados de sistema. 
- Implementação de expressões regulares (Regex) para higienização do texto.
- Aplicação de filtro de densidade: notícias com extensão inferior a 10 palavras foram descartadas para garantir a relevância dos dados processados.

### 2. Geração de Embeddings
A conversão de texto para vetores numéricos utiliza a biblioteca sentence-transformers.
- Modelo: paraphrase-multilingual-MiniLM-L12-v2.
- Critérios de escolha: O modelo oferece suporte ao idioma português, apresenta baixo custo computacional e permite execução eficiente em ambiente de CPU, dispensando o uso de aceleradores gráficos (GPU).

### 3. Sistema de Busca
A recuperação de informações é baseada no cálculo de similaridade de cosseno. O sistema compara o vetor da consulta do usuário com a base de embeddings gerada, retornando os documentos com maior proximidade semântica.

---

## Validação de Resultados

A eficiência da pipeline foi testada com consultas temáticas, apresentando os seguintes resultados de primeira posição:

- Termo: "mudanças na taxa de juros" -> Resultado: Notícia relacionada à Selic.
- Termo: "mercado de trabalho e desemprego" -> Resultado: Notícia sobre índices de desocupação.
- Termo: "inflação e preços ao consumidor" -> Resultado: Notícia referente ao IPCA.

---

## Planejamento de Evoluções

### Melhorias em Modelagem e Métricas
- Avaliação de modelos especializados na língua portuguesa (BERTimbau e ptT5).
- Implementação e comparação de novas métricas de distância, como Euclidiana e divergência KL.

### Escalabilidade e Arquitetura
- Migração do armazenamento local (.npy) para sistemas de indexação vetorial (FAISS ou ChromaDB).
- Integração da pipeline com frameworks de orquestração como LangChain para suporte a aplicações mais complexas e fluxos agênticos.