## O que cada etapa faz

**Etapa 1 — Limpeza**

Os textos das notícias vieram brutos: tags HTML, entidades HTML, timestamps e metadados jogados no meio do texto. Usei regex pra remover tudo isso e deixar só o conteúdo de fato. Notícias com menos de 10 palavras depois da limpeza foram descartadas.

**Etapa 2 — Embeddings**

Usei a biblioteca sentence-transformers com o modelo paraphrase-multilingual-MiniLM-L12-v2 pra transformar cada notícia em um vetor numérico. Escolhi esse modelo porque ele suporta português e é leve o suficiente pra rodar sem GPU.

**Etapa 3 — Busca**

A busca funciona calculando a similaridade cosseno entre o vetor da query e os vetores de todas as notícias. As mais similares são retornadas como resultado.

## Resultados

Os resultados das três queries de validação fazem sentido:

- "mudanças na taxa de juros" trouxe a notícia da Selic como primeira
- "mercado de trabalho e desemprego" trouxe a notícia de queda do desemprego como primeira
- "inflação e preços ao consumidor" trouxe o IPCA como primeiro resultado

## Futuras melhorias

- Teste com novos modelos de embeddings mais apropriados para o português, como BERTimbau ou ptT5.
- Experimentação de outras métricas de similaridade (distância euclidiana, divergência KL) comparando acerto no retrieval e tempo de resposta.
- Migração do pipeline para SDK com extensão agêntica como LangChain para permitir integração com LLMs e orquestração agêntica.