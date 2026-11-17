"""Confere o projetos.json antes de publicar o site.

Uso:
    python validar.py                 # confere o projetos.json desta pasta
    python validar.py outro.json      # confere outro arquivo

Sai com código 0 quando está tudo certo e 1 quando encontra algum problema.
Usa só a biblioteca padrão do Python; não precisa instalar nada.
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CATEGORIAS = ("Dashboards", "Automações", "IA")  # as mesmas do script.js e do index.html

# campo: (tipo esperado, pode ficar vazio?)
CAMPOS = {
    "titulo": (str, False),
    "categoria": (str, False),
    "descricao": (str, False),
    "ferramentas": (list, False),
    "imagem": (str, True),
    "link": (str, True),
    "destaque": (bool, False),
    "emConstrucao": (bool, False),
}
NOMES_TIPO = {str: "texto entre aspas", list: "lista entre colchetes", bool: "true ou false"}


def conferir_projeto(p, nome, erros):
    if not isinstance(p, dict):
        erros.append(f"{nome}: cada projeto precisa estar entre chaves {{ }}.")
        return

    for campo in p:
        if campo not in CAMPOS:
            erros.append(f"{nome}: campo desconhecido \"{campo}\". Os campos válidos são: {', '.join(CAMPOS)}.")

    for campo, (tipo, pode_vazio) in CAMPOS.items():
        if campo not in p:
            erros.append(f"{nome}: falta o campo \"{campo}\".")
            continue
        valor = p[campo]
        if type(valor) is not tipo:  # type() para não aceitar 0/1 no lugar de true/false
            erros.append(f"{nome}: \"{campo}\" deve ser {NOMES_TIPO[tipo]}.")
            continue
        if not pode_vazio and tipo is str and not valor.strip():
            erros.append(f"{nome}: \"{campo}\" está vazio.")

    categoria = p.get("categoria")
    if isinstance(categoria, str) and categoria.strip() and categoria not in CATEGORIAS:
        erros.append(f"{nome}: categoria \"{categoria}\" não existe. Use exatamente: {', '.join(CATEGORIAS)}.")

    ferramentas = p.get("ferramentas")
    if isinstance(ferramentas, list):
        if not ferramentas:
            erros.append(f"{nome}: \"ferramentas\" está vazia.")
        elif not all(isinstance(f, str) and f.strip() for f in ferramentas):
            erros.append(f"{nome}: cada item de \"ferramentas\" deve ser um texto entre aspas.")

    imagem = p.get("imagem")
    if isinstance(imagem, str) and imagem:
        if not imagem.startswith("assets/img/"):
            erros.append(f"{nome}: a imagem deve ficar em assets/img/ (veio \"{imagem}\").")
        elif not (RAIZ / imagem).is_file():
            erros.append(f"{nome}: a imagem \"{imagem}\" não foi encontrada. Confira o nome e a extensão.")

    link = p.get("link")
    if isinstance(link, str) and link and not link.startswith("https://"):
        erros.append(f"{nome}: o link deve começar com https:// (veio \"{link}\").")


def validar(caminho):
    erros = []
    try:
        texto = caminho.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [f"Arquivo não encontrado: {caminho}"], 0

    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as e:
        linha = texto.splitlines()[e.lineno - 1] if e.lineno <= len(texto.splitlines()) else ""
        return [
            f"O arquivo não é um JSON válido (linha {e.lineno}, coluna {e.colno}): {e.msg}.\n"
            f"    {linha.strip()}\n"
            "    Costuma ser uma vírgula sobrando ou faltando, ou uma aspa esquecida, nesta linha ou na anterior."
        ], 0

    if not isinstance(dados, list) or not dados:
        return ["O arquivo deve ser uma lista de projetos entre colchetes [ ], com pelo menos um projeto."], 0

    titulos = {}
    for i, p in enumerate(dados, start=1):
        titulo = p.get("titulo") if isinstance(p, dict) else None
        nome = f"Projeto {i}" + (f" ({titulo})" if isinstance(titulo, str) and titulo.strip() else "")
        conferir_projeto(p, nome, erros)
        if isinstance(titulo, str) and titulo.strip():
            if titulo in titulos:
                erros.append(f"{nome}: título repetido (igual ao projeto {titulos[titulo]}).")
            titulos.setdefault(titulo, i)

    return erros, len(dados)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # acentos no terminal do Windows
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "projetos.json"
    erros, total = validar(caminho)
    if erros:
        print(f"{len(erros)} problema(s) em {caminho.name}:")
        for e in erros:
            print(f"  - {e}")
        sys.exit(1)
    print(f"{caminho.name} OK: {total} projetos conferidos.")


if __name__ == "__main__":
    main()
