(() => {
  const ALBUM = [
    {
      src: "assets/img/tela-ieducar-gestao.jpg",
      url: "i-educar · gestão",
      title: "Gestão escolar · painel da secretaria",
      desc: "Visão consolidada da rede a partir do cadastro único: alunos, escolas, turmas e indicadores operacionais.",
      pros: [
        "Um número oficial para toda a secretaria",
        "Acompanhamento diário sem consolidar escola por escola",
        "Base pronta para Censo, documentos e satélites",
      ],
    },
    {
      src: "assets/img/tela-matricula.jpg",
      url: "i-educar · matrícula",
      title: "Matrícula e cadastro do aluno",
      desc: "Registro da pessoa e da matrícula com vínculo a turma, etapa e situação escolar.",
      pros: [
        "Histórico contínuo do aluno na rede",
        "Menos retrabalho em transferência e renovação",
        "Dados consistentes para documentos e Educacenso",
      ],
    },
    {
      src: "assets/img/tela-idiario.jpg",
      url: "i-diario · microssistema",
      title: "i-Diário · microssistema conectado ao i-Educar",
      desc: "Produto do professor acoplado ao SGE: diário, chamada, notas e planejamento na mesma base de alunos e turmas.",
      pros: [
        "Microssistema próprio, não uma tela isolada",
        "Lançamento na sala com reflexo na secretaria",
        "Apoia busca ativa, boletim e acompanhamento pedagógico",
      ],
    },
    {
      src: "assets/img/tela-fila.jpg",
      url: "pré-matrícula",
      title: "Pré-matrícula · fila e vagas",
      desc: "Organização da demanda por vaga com protocolos, status e critérios da rede.",
      pros: [
        "Transparência para famílias e gestores",
        "Apoio à lista de espera pública",
        "Planejamento de oferta com demanda real",
      ],
    },
    {
      src: "assets/img/tela-censo.jpg",
      url: "educacenso",
      title: "Educacenso · validação e exportação",
      desc: "Preparação do arquivo para o INEP com conferência por escola.",
      pros: [
        "Menos força-tarefa manual no prazo do Censo",
        "Validação antes do envio reduz retrabalho",
        "Usa a base já operada no dia a dia",
      ],
    },
    {
      src: "assets/img/tela-transporte.jpg",
      url: "transporte v2",
      title: "Transporte escolar v2",
      desc: "Rotas com mapa, frota, passageiros e operação de viagens ligadas ao aluno matriculado.",
      pros: [
        "Ocupação e rotas alinhadas à matrícula",
        "Visibilidade para a família e para a SME",
        "Base para gastos e conformidade",
      ],
    },
    {
      src: "assets/img/tela-relatorios.jpg",
      url: "advanced reports",
      title: "Relatórios e documentos",
      desc: "Emissão de boletins e documentos em PDF/Excel, com validação pública por QR Code.",
      pros: [
        "Documentos oficiais no dia a dia sem Java",
        "Autenticidade verificável pelo cidadão",
        "Menus temáticos para secretaria e pedagógico",
      ],
    },
    {
      src: "assets/img/tela-servlitcys.jpg",
      url: "servlitcys",
      title: "SERVLITCYS · analytics municipal",
      desc: "Consultoria e mapa Horizonte cruzando i-Educar com FUNDEB, Censo e SAEB.",
      pros: [
        "Decisão com dado territorial e financeiro",
        "Leitura integrada da rede e do contexto público",
        "Apoio a diagnóstico e priorização",
      ],
    },
    {
      src: "assets/img/tela-moodle.jpg",
      url: "moodle · capacitação",
      title: "Moodle · treinamento híbrido",
      desc: "Ambiente LMS para trilhas de capacitação do ecossistema, combinando online e apoio presencial.",
      pros: [
        "Escala o treinamento por perfil (SME, escola, professor)",
        "Padroniza implantação em vários municípios",
        "Registra progresso e certificação da rede",
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

  // Keep disabled test links from navigating
  document.querySelectorAll("a.btn-disabled").forEach((a) => {
    a.addEventListener("click", (e) => e.preventDefault());
  });
})();
