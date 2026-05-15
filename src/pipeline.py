import json
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from limpar_dados import processar_noticias
from embeddings import gerar_embeddings, carregar_dados
from buscar_dados import buscar, exibir_resultados, MODELO
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).parent
DADOS_BRUTOS = BASE / "dados" / "noticias_brutas.json"
DADOS_LIMPOS = BASE / "dados" / "dados_limpos.json"
EMBEDDINGS_PATH = BASE / "dados" / "embeddings.npy"

QUERIES = [
    "mudanças na taxa de juros",
    "mercado de trabalho e desemprego",
    "inflação e preços ao consumidor",
]


def main():
    print("=" * 60)
    print("ETAPA 1 — Limpeza")
    print("=" * 60)
    noticias = processar_noticias(str(DADOS_BRUTOS), str(DADOS_LIMPOS))

    print("\n" + "=" * 60)
    print("ETAPA 2 — Embeddings")
    print("=" * 60)
    embeddings, modelo = gerar_embeddings(noticias)
    np.save(str(EMBEDDINGS_PATH), embeddings)
    print("Embeddings salvos.")

    print("\n" + "=" * 60)
    print("ETAPA 3 — Busca")
    print("=" * 60)
    for query in QUERIES:
        resultados = buscar(query, noticias, embeddings, modelo, top_k=3)
        exibir_resultados(query, resultados)


if __name__ == "__main__":
    main()