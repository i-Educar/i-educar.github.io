(() => {
  const ALBUM = [
    {
      src: "assets/img/tela-ieducar-gestao.jpg",
      url: "painel da secretaria",
      title: "Passo da operação 1 · Painel da secretaria",
      desc: "Ponto de partida da decisão operacional: indicadores da rede a partir do cadastro único — sem pedir planilha escola por escola.",
      pros: [
        "Um número oficial para apresentar ao gabinete e ao conselho",
        "Acompanhamento contínuo da rede, não só no fechamento do mês",
        "Base pronta para Censo, documentos e módulos satélite",
      ],
    },
    {
      src: "assets/img/tela-matricula.jpg",
      url: "matrícula",
      title: "Passo da operação 1 · Matrícula oficial",
      desc: "Base de toda a cadeia decisória: pessoa e matrícula oficiais alimentam diário, fila, Censo, transporte e documentos.",
      pros: [
        "Histórico do aluno permanece na rede, não em pasta solta",
        "Menos retrabalho em renovação e transferência",
        "Dados consistentes para documentos e Educacenso",
      ],
    },
    {
      src: "assets/img/tela-idiario.jpg",
      url: "i-diario",
      title: "Passo da operação 2 · i-Diário",
      desc: "Depois do núcleo: o professor lança na sala e a SME já lê frequência e notas — sem cadastro paralelo.",
      pros: [
        "Acaba a digitação duplicada de frequência e notas",
        "Fecha período com menos atraso",
        "Apoia busca ativa e emissão de boletim",
      ],
    },
    {
      src: "assets/img/tela-fila.jpg",
      url: "pré-matrícula",
      title: "Passo da operação 3 · Pré-matrícula",
      desc: "Com a base estável, a família entra na fila com critério público — a SME planeja oferta com demanda real.",
      pros: [
        "Transparência para famílias e para a gestão",
        "Apoio às regras de lista de espera pública",
        "Planejamento de oferta com demanda real",
      ],
    },
    {
      src: "assets/img/tela-censo.jpg",
      url: "educacenso",
      title: "Passo da operação 4 · Educacenso",
      desc: "O Censo aproveita o cadastro do ano. Na decisão do gestor: menos risco político e menos correção no prazo final.",
      pros: [
        "Reduz risco de erro no prazo do Censo",
        "Validação por escola antes do envio",
        "Aproveita o trabalho diário da rede",
      ],
    },
    {
      src: "assets/img/tela-transporte.jpg",
      url: "transporte",
      title: "Passo da operação 5 · Transporte",
      desc: "Módulo sob demanda: rotas e frota ligadas à matrícula oficial — entra quando a logística é prioridade da gestão.",
      pros: [
        "Ocupação alinhada ao aluno matriculado",
        "Visibilidade para a família e para a gestão",
        "Base para controle de gastos e conformidade",
      ],
    },
    {
      src: "assets/img/tela-relatorios.jpg",
      url: "documentos",
      title: "Passo da operação 5 · Documentos",
      desc: "Emissão oficial a partir da mesma base — atendimento ao cidadão sem processo manual demorado.",
      pros: [
        "Emissão sem depender de processo manual demorado",
        "Autenticidade verificável pela família",
        "Padronização dos documentos da rede",
      ],
    },
    {
      src: "assets/img/tela-servlitcys.jpg",
      url: "servlitcys",
      title: "Passo da operação 6 · SERVLITCYS",
      desc: "Camada de leitura para gabinete e conselhos: cruza a base local com FUNDEB, Censo e território.",
      pros: [
        "Apoia priorização e diagnóstico da rede",
        "Une dado operacional e contexto público",
        "Linguagem de painel para reunião de gestão",
      ],
    },
    {
      src: "assets/img/tela-moodle.jpg",
      url: "moodle",
      title: "Passo 4 da decisão · Moodle",
      desc: "Capacitação entra depois de definir o pacote e o fluxo — para a equipe operar com padrão antes de escalar.",
      pros: [
        "Padroniza o treinamento em vários municípios",
        "Registra progresso e certificação da equipe",
        "Reduz dependência de uma única turma presencial",
      ],
    },
  ];

  const nodes = document.querySelectorAll(".reveal");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) {
    nodes.forEach((el) => el.classList.add("is-visible"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -6% 0px" }
    );
    nodes.forEach((el) => io.observe(el));
  }

  const lightbox = document.getElementById("lightbox");
  const lbImage = document.getElementById("lb-image");
  const lbTitle = document.getElementById("lb-title");
  const lbDesc = document.getElementById("lb-desc");
  const lbPros = document.getElementById("lb-pros");
  const lbIndex = document.getElementById("lb-index");
  const lbUrl = document.getElementById("lb-url");
  const lbClose = document.getElementById("lb-close");
  const lbPrev = document.getElementById("lb-prev");
  const lbNext = document.getElementById("lb-next");
  let current = 0;
  let lastFocus = null;

  function render(index) {
    current = (index + ALBUM.length) % ALBUM.length;
    const item = ALBUM[current];
    lbImage.src = item.src;
    lbImage.alt = item.title;
    lbTitle.textContent = item.title;
    lbDesc.textContent = item.desc;
    lbUrl.textContent = item.url;
    lbIndex.textContent = `${current + 1} / ${ALBUM.length}`;
    lbPros.innerHTML = "";
    item.pros.forEach((pro) => {
      const li = document.createElement("li");
      li.textContent = pro;
      lbPros.appendChild(li);
    });
  }

  function openAlbum(index) {
    lastFocus = document.activeElement;
    render(index);
    lightbox.hidden = false;
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("album-open");
    lbClose.focus();
  }

  function closeAlbum() {
    lightbox.classList.remove("is-open");
    lightbox.hidden = true;
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("album-open");
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  document.querySelectorAll("[data-album-index]").forEach((btn) => {
    btn.addEventListener("click", () => openAlbum(Number(btn.dataset.albumIndex) || 0));
  });
  document.querySelectorAll("[data-open-album]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      openAlbum(Number(btn.dataset.openAlbum) || 0);
    });
  });

  lbClose.addEventListener("click", closeAlbum);
  lbPrev.addEventListener("click", () => render(current - 1));
  lbNext.addEventListener("click", () => render(current + 1));
  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) closeAlbum();
  });
  document.addEventListener("keydown", (e) => {
    if (!lightbox.classList.contains("is-open")) return;
    if (e.key === "Escape") closeAlbum();
    if (e.key === "ArrowLeft") render(current - 1);
    if (e.key === "ArrowRight") render(current + 1);
  });

  document.querySelectorAll("a.btn-disabled").forEach((a) => {
    a.addEventListener("click", (e) => e.preventDefault());
  });
})();
