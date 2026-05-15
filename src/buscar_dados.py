import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

MODELO = "paraphrase-multilingual-MiniLM-L12-v2"


def similaridade_cosseno(vetor_query, matriz):
    norma_query = np.linalg.norm(vetor_query)
    normas_docs = np.linalg.norm(matriz, axis=1)

    denominador = norma_query * normas_docs
    denominador = np.where(denominador == 0, 1e-10, denominador)

    return np.dot(matriz, vetor_query) / denominador


def buscar(query, noticias, embeddings, modelo, top_k=3):
    embedding_query = modelo.encode(query, convert_to_numpy=True)
    scores = similaridade_cosseno(embedding_query, embeddings)

    indices_top = np.argsort(scores)[::-1][:top_k]

    resultados = []
    for idx in indices_top:
        resultados.append({
            "id": noticias[idx]["id"],
            "titulo": noticias[idx]["titulo"],
            "fonte": noticias[idx]["fonte"],
            "data": noticias[idx]["data"],
            "score": float(scores[idx]),
            "trecho": noticias[idx]["texto_limpo"][:200] + "...",
        })

    return resultados


def exibir_resultados(query, resultados):
    print(f"\nQuery: \"{query}\"")
    print("-" * 60)
    for i, r in enumerate(resultados, 1):
        print(f"{i}. [{r['score']:.4f}] {r['titulo']}")
        print(f"   Fonte: {r['fonte']} | Data: {r['data']}")
        print(f"   {r['trecho']}")
        print()


if __name__ == "__main__":
    base = Path(__file__).parent.parent

    with open(base / "dados" / "dados_limpos.json", "r", encoding="utf-8") as f:
        noticias = json.load(f)

    embeddings = np.load(base / "dados" / "embeddings.npy")

    print(f"Carregando modelo...")
    modelo = SentenceTransformer(MODELO)

    queries = [
        "mudanças na taxa de juros",
        "mercado de trabalho e desemprego",
        "inflação e preços ao consumidor",
    ]

    for query in queries:
        resultados = buscar(query, noticias, embeddings, modelo, top_k=3)
        exibir_resultados(query, resultados)