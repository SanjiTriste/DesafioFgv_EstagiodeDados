import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

MODELO = "paraphrase-multilingual-MiniLM-L12-v2"


def carregar_dados(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def gerar_embeddings(noticias):
    print(f"Carregando modelo...")
    modelo = SentenceTransformer(MODELO)

    textos = [f"{n['titulo']}. {n['texto_limpo']}" for n in noticias]

    print(f"Gerando embeddings para {len(textos)} notícias...")
    embeddings = modelo.encode(textos, show_progress_bar=True, convert_to_numpy=True)

    return embeddings, modelo


if __name__ == "__main__":
    base = Path(__file__).parent.parent

    noticias = carregar_dados(str(base / "dados" / "dados_limpos.json"))
    embeddings, _ = gerar_embeddings(noticias)

    np.save(str(base / "dados" / "embeddings.npy"), embeddings)
    print(f"Embeddings salvos.")