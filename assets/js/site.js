(() => {
  const ALBUM = [
    {
      src: "assets/img/tela-ieducar-gestao.jpg",
      title: "Gestão escolar · painel da secretaria",
      desc: "Visão consolidada da rede: alunos, escolas, turmas e indicadores em tempo real a partir do cadastro único.",
      pros: [
        "Um número oficial para toda a secretaria — sem planilhas paralelas",
        "Acompanhamento diário da rede sem consolidar escola por escola",
        "Base pronta para Censo, relatórios e integrações satélite",
      ],
    },
    {
      src: "assets/img/tela-matricula.jpg",
      title: "Matrícula e cadastro do aluno",
      desc: "Registro completo da pessoa e da matrícula, com vínculo a turma, etapa e situação escolar.",
      pros: [
        "Histórico contínuo do aluno na rede",
        "Menos retrabalho na transferência e renovação",
        "Dados consistentes para documentos e Educacenso",
      ],
    },
    {
      src: "assets/img/tela-idiario.jpg",
      title: "i-Diário · microssistema conectado ao i-Educar",
      desc: "Microssistema do professor acoplado ao SGE: diário de classe, chamada, notas e planejamento na mesma base de alunos e turmas do i-Educar — sem cadastro paralelo.",
      pros: [
        "Produto próprio (web/app) conectado ao núcleo, não uma tela isolada",
        "Lançamento na sala com reflexo imediato na secretaria",
        "Reduz papel e atraso na consolidação de faltas e notas",
        "Apoia busca ativa, boletim e acompanhamento pedagógico",
      ],
    },
    {
      src: "assets/img/tela-fila.jpg",
      title: "Pré-matrícula · fila e vagas",
      desc: "Organização da demanda por vaga com protocolos, status e critérios definidos pela rede.",
      pros: [
        "Transparência para famílias e gestores",
        "Apoio às exigências de lista de espera pública",
        "Planejamento de oferta com demanda real",
      ],
    },
    {
      src: "assets/img/tela-censo.jpg",
      title: "Educacenso · validação e exportação",
      desc: "Preparação do arquivo para o INEP com conferência por escola e acompanhamento do progresso.",
      pros: [
        "Menos força-tarefa manual no prazo do Censo",
        "Validação antes do envio reduz glosas e retrabalho",
        "Usa a mesma base já operada no dia a dia",
      ],
    },
    {
      src: "assets/img/tela-transporte.jpg",
      title: "Transporte escolar v2",
      desc: "Rotas com mapa, frota, passageiros, portal da família e operação de viagens.",
      pros: [
        "Ocupação e rotas ligadas ao aluno matriculado",
        "Visibilidade para a família e para a SME",
        "Base para gastos, conformidade e prestação de contas",
      ],
    },
    {
      src: "assets/img/tela-relatorios.jpg",
      title: "Advanced Reports · documentos",
      desc: "Emissão de boletins e documentos em PDF/Excel, com validação pública por QR Code.",
      pros: [
        "Documentos oficiais sem depender de Java no dia a dia",
        "Autenticidade verificável pelo cidadão",
        "Menus temáticos para secretaria e pedagógico",
      ],
    },
    {
      src: "assets/img/tela-servlitcys.jpg",
      title: "SERVLITCYS · analytics municipal",
      desc: "Painéis de consultoria e mapa Horizonte cruzando i-Educar com FUNDEB, Censo e SAEB.",
      pros: [
        "Decisão com dado territorial e financeiro",
        "Uma leitura integrada da rede e do contexto público",
        "Apoio a expansão, priorização e diagnóstico",
      ],
    },
  ];

  /* Reveal on scroll */
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
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    nodes.forEach((el) => io.observe(el));
  }

  /* Album lightbox */
  const lightbox = document.getElementById("lightbox");
  const lbImage = document.getElementById("lb-image");
  const lbTitle = document.getElementById("lb-title");
  const lbDesc = document.getElementById("lb-desc");
  const lbPros = document.getElementById("lb-pros");
  const lbIndex = document.getElementById("lb-index");
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
    lightbox.setAttribute("aria-hidden", "false");
    lightbox.classList.add("is-open");
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
    btn.addEventListener("click", () => {
      openAlbum(Number(btn.dataset.albumIndex) || 0);
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
})();
