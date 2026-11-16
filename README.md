# Portfólio · Lorrayne Gonçalves

Site de portfólio publicado no GitHub Pages: https://lorrayneegoncalves.github.io

Feito com HTML, CSS e JavaScript puros, sem framework e sem etapa de build. Os cards de projeto e os filtros são montados a partir do arquivo `projetos.json`.

## Estrutura

```
index.html          # página única: topo, abertura, projetos, sobre, contato, rodapé
styles.css          # cores, tipografia e layout (inclui as regras para celular)
script.js           # lê projetos.json, monta os cards, os filtros, o índice e o "Ver mais"
projetos.json       # lista de projetos (é o único arquivo que muda para incluir um projeto)
assets/
  favicon.svg
  img/              # imagens dos cards
MODELO_README_PROJETO.md   # modelo de README para os repositórios de projeto
```

## Como adicionar um projeto

1. **Imagem (opcional).** Salve um print do projeto em `assets/img/`, de preferência em JPG, com proporção 16:10 (por exemplo, 1200 × 750) e menos de 200 KB. O card mostra a parte de cima da imagem. Sem imagem, o card mostra um espaço reservado.

2. **Novo item no `projetos.json`.** Copie um item existente e altere os campos. Atenção à vírgula entre os itens.

   ```json
   {
     "titulo": "Nome do projeto",
     "categoria": "Automações",
     "descricao": "Uma ou duas frases: o problema e o que a solução faz.",
     "ferramentas": ["Python", "Pandas", "Power Automate"],
     "imagem": "assets/img/nome-do-projeto.jpg",
     "link": "https://github.com/Lorrayneegoncalves/nome-do-repositorio",
     "destaque": false,
     "emConstrucao": false
   }
   ```

   | Campo | O que colocar |
   |---|---|
   | `titulo` | Nome curto do projeto. |
   | `categoria` | Exatamente `Dashboards`, `Automações` ou `IA` (com acento e maiúsculas). É o que define o filtro e a contagem do índice. |
   | `descricao` | Uma ou duas frases. Sem números que não estejam no README do projeto. |
   | `ferramentas` | Lista de ferramentas, entre aspas e separadas por vírgula. |
   | `imagem` | Caminho da imagem em `assets/img/`, ou `""` para usar o espaço reservado. |
   | `link` | Endereço do repositório no GitHub. |
   | `destaque` | `true` para aparecer antes dos outros; `false` caso contrário. |
   | `emConstrucao` | `true` para mostrar o selo "Em construção". |

3. **Confira localmente.** O site lê o JSON com `fetch`, então não funciona abrindo o `index.html` direto do disco. Na pasta do repositório, rode:

   ```bash
   python -m http.server 8000
   ```

   e abra http://localhost:8000. Se os cards não aparecerem, provavelmente há um erro no JSON (vírgula sobrando ou faltando). Dá para validar colando o conteúdo em https://jsonlint.com.

4. **Publique.**

   ```bash
   git add projetos.json assets/img
   git commit -m "Adiciona projeto Nome do projeto"
   git push
   ```

   O GitHub Pages atualiza o site em um ou dois minutos.

## Regras da página

- A grade mostra 6 projetos (destaques primeiro, depois a ordem do JSON). Com mais de 6 no filtro escolhido, aparece o botão "Ver mais".
- O índice da abertura conta os projetos de cada categoria automaticamente.
- Cores: fundo `#F2F2EF`, superfícies `#FBFBF9`, texto `#1F2326`, texto secundário `#5C6166`, linhas `#D8D8D2`, destaque `#8A5A62`. Títulos em Space Grotesk e texto em Inter (Google Fonts).

## Modelo de README para os projetos

O arquivo [`MODELO_README_PROJETO.md`](MODELO_README_PROJETO.md) tem a estrutura sugerida para o README de cada repositório: problema, solução, ferramentas, prints e resultado.
