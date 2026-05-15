import json
import re
import html
from pathlib import Path


def limpar_texto(texto):
    texto = re.sub(r"<!--.*?-->", " ", texto, flags=re.DOTALL)

    texto = re.sub(r"PUBLICADO EM:\s*[\d\-: ]+", " ", texto, flags=re.IGNORECASE)
    texto = re.sub(r"UPDATED:\s*[\d\-:T Z]+", " ", texto, flags=re.IGNORECASE)
    texto = re.sub(r"TIMESTAMP:\s*\d+", " ", texto, flags=re.IGNORECASE)
    texto = re.sub(r"SOURCE(?:_ID)?:\s*[\w_]+", " ", texto, flags=re.IGNORECASE)
    texto = re.sub(r"last_modified:\s*[\d\-: ]+", " ", texto, flags=re.IGNORECASE)
    texto = re.sub(r"ts=\d+", " ", texto, flags=re.IGNORECASE)
    texto = re.sub(r"article_id=\d+\s*author=\w+", " ", texto, flags=re.IGNORECASE)
    texto = re.sub(r"nav:\s*[\w\s>]+", " ", texto, flags=re.IGNORECASE)
    texto = re.sub(r"Atualizado em[\s\d\-:]+", " ", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\bUTC\b", " ", texto)
    texto = re.sub(r"\|\s*", "", texto)

    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = html.unescape(texto)

    texto = re.sub(r"\n+", " ", texto)
    texto = re.sub(r"\s{2,}", " ", texto)

    return texto.strip()


def processar_noticias(caminho_entrada, caminho_saida):
    with open(caminho_entrada, "r", encoding="utf-8") as f:
        noticias = json.load(f)

    resultado = []
    descartadas = []

    for noticia in noticias:
        texto_limpo = limpar_texto(noticia["texto"])

        if len(texto_limpo.split()) < 10:
            descartadas.append(noticia["id"])
            continue

        resultado.append({
            "id": noticia["id"],
            "titulo": noticia["titulo"].strip(),
            "texto_limpo": texto_limpo,
            "data": noticia["data"],
            "fonte": noticia["fonte"],
        })

    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"{len(resultado)} notícias processadas.")
    if descartadas:
        print(f"descartadas por conteúdo curto: {descartadas}")

    return resultado


if __name__ == "__main__":
    base = Path(__file__).parent.parent
    processar_noticias(
        caminho_entrada=str(base / "dados" / "noticias_brutas.json"),
        caminho_saida=str(base / "dados" / "dados_limpos.json"),
    )