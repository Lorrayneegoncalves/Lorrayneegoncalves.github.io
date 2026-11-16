/* Monta os cards e os filtros a partir de projetos.json. */
(function () {
  "use strict";

  var LIMITE = 6;                 // cards visíveis antes do "Ver mais"
  var CATEGORIAS = ["Dashboards", "Automações", "IA"];

  var grade = document.getElementById("grade-projetos");
  var status = document.getElementById("status-projetos");
  var botaoMais = document.getElementById("ver-mais");
  var modelo = document.getElementById("modelo-card");
  var botoesFiltro = document.querySelectorAll(".filtro");

  var projetos = [];
  var filtroAtual = "Todos";
  var expandido = false;

  // Destaques primeiro; dentro de cada grupo, mantém a ordem do JSON.
  function ordenar(lista) {
    return lista
      .map(function (p, i) { return { p: p, i: i }; })
      .sort(function (a, b) {
        return (b.p.destaque === true) - (a.p.destaque === true) || a.i - b.i;
      })
      .map(function (x) { return x.p; });
  }

  function criarCard(p) {
    var card = modelo.content.firstElementChild.cloneNode(true);

    var areaImagem = card.querySelector(".card__imagem");
    if (p.imagem) {
      var img = document.createElement("img");
      img.src = p.imagem;
      img.alt = "Tela do projeto " + p.titulo;
      img.loading = "lazy";
      img.decoding = "async";
      img.width = 1200;
      img.height = 750;
      img.addEventListener("error", function () { areaImagem.replaceChildren(reservado()); });
      areaImagem.appendChild(img);
    } else {
      areaImagem.appendChild(reservado());
    }

    card.querySelector(".card__categoria").textContent = p.categoria;
    card.querySelector(".selo").hidden = !p.emConstrucao;
    card.querySelector(".card__titulo").textContent = p.titulo;
    card.querySelector(".card__descricao").textContent = p.descricao;

    var lista = card.querySelector(".card__ferramentas");
    (p.ferramentas || []).forEach(function (f) {
      var li = document.createElement("li");
      li.textContent = f;
      lista.appendChild(li);
    });

    var link = card.querySelector(".card__link");
    if (p.link) {
      link.href = p.link;
      link.setAttribute("aria-label", "Ver repositório do projeto " + p.titulo + " no GitHub");
    } else {
      link.remove();
    }
    return card;
  }

  function reservado() {
    var div = document.createElement("div");
    div.className = "card__reservado";
    div.textContent = "Imagem em breve";
    return div;
  }

  function render() {
    var filtrados = projetos.filter(function (p) {
      return filtroAtual === "Todos" || p.categoria === filtroAtual;
    });
    var visiveis = expandido ? filtrados : filtrados.slice(0, LIMITE);

    grade.replaceChildren.apply(grade, visiveis.map(criarCard));
    status.textContent = filtrados.length ? "" : "Nenhum projeto nesta categoria ainda.";

    botaoMais.hidden = filtrados.length <= LIMITE;
    botaoMais.textContent = expandido ? "Ver menos" : "Ver mais";
    botaoMais.setAttribute("aria-expanded", String(expandido));
  }

  function filtrar(categoria) {
    filtroAtual = categoria;
    expandido = false;
    botoesFiltro.forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.filtro === categoria));
    });
    render();
  }

  function contar() {
    CATEGORIAS.forEach(function (c) {
      var n = projetos.filter(function (p) { return p.categoria === c; }).length;
      var alvo = document.querySelector('[data-contagem="' + c + '"]');
      if (alvo) alvo.textContent = n + (n === 1 ? " projeto" : " projetos");
    });
  }

  botoesFiltro.forEach(function (b) {
    b.addEventListener("click", function () { filtrar(b.dataset.filtro); });
  });

  // Índice da abertura: filtra e deixa o link rolar até a seção de projetos.
  document.querySelectorAll(".indice [data-filtro]").forEach(function (a) {
    a.addEventListener("click", function () { filtrar(a.dataset.filtro); });
  });

  botaoMais.addEventListener("click", function () {
    var estavaExpandido = expandido;
    expandido = !expandido;
    render();
    if (estavaExpandido) {
      document.getElementById("projetos").scrollIntoView({ block: "start" });
    }
  });

  fetch("projetos.json", { cache: "no-cache" })
    .then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    })
    .then(function (dados) {
      projetos = ordenar(dados);
      contar();
      render();
    })
    .catch(function () {
      status.textContent = "Não foi possível carregar os projetos. Veja todos no GitHub: github.com/Lorrayneegoncalves";
    });
})();
