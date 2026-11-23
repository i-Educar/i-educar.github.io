(() => {
  const ALBUM = [
    {
      src: "assets/img/tela-ieducar-gestao.jpg",
      url: "painel da secretaria",
      title: "Painel da secretaria · visão da rede",
      desc: "Para o gestor: indicadores de alunos, escolas e turmas a partir do cadastro único — sem pedir planilha escola por escola.",
      pros: [
        "Um número oficial para apresentar ao gabinete e ao conselho",
        "Acompanhamento contínuo da rede, não só no fechamento do mês",
        "Base pronta para Censo, documentos e módulos satélite",
      ],
    },
    {
      src: "assets/img/tela-matricula.jpg",
      url: "matrícula",
      title: "Matrícula · cadastro oficial do aluno",
      desc: "Registro completo da pessoa e da matrícula, com vínculo à turma e à situação escolar — o ponto de partida de toda a gestão.",
      pros: [
        "Histórico do aluno permanece na rede, não em pasta solta",
        "Menos retrabalho em renovação e transferência",
        "Dados consistentes para documentos e Educacenso",
      ],
    },
    {
      src: "assets/img/tela-idiario.jpg",
      url: "i-diario",
      title: "i-Diário · o professor na mesma base",
      desc: "Microssistema do professor conectado ao i-Educar: chamada e notas lançadas na sala já alimentam a secretaria.",
      pros: [
        "Acaba a digitação duplicada de frequência e notas",
        "Fecha período com menos atraso",
        "Apoia busca ativa e emissão de boletim",
      ],
    },
    {
      src: "assets/img/tela-fila.jpg",
      url: "pré-matrícula",
      title: "Pré-matrícula · fila transparente",
      desc: "Organiza a demanda por vaga com protocolo e status visíveis — menos fila na porta da escola e mais critério na distribuição.",
      pros: [
        "Transparência para famílias e para a gestão",
        "Apoio às regras de lista de espera pública",
        "Planejamento de oferta com demanda real",
      ],
    },
    {
      src: "assets/img/tela-censo.jpg",
      url: "educacenso",
      title: "Educacenso · menos correção de última hora",
      desc: "A secretaria prepara e confere o envio ao INEP usando a base já operada no ano — não uma força-tarefa paralela.",
      pros: [
        "Reduz risco de erro no prazo do Censo",
        "Validação por escola antes do envio",
        "Aproveita o trabalho diário da rede",
      ],
    },
    {
      src: "assets/img/tela-transporte.jpg",
      url: "transporte",
      title: "Transporte escolar · rotas ligadas ao aluno",
      desc: "Rotas, mapa e frota conectados à matrícula: a SME sabe quem tem direito e quem está na viagem.",
      pros: [
        "Ocupação alinhada ao aluno matriculado",
        "Visibilidade para a família e para a gestão",
        "Base para controle de gastos e conformidade",
      ],
    },
    {
      src: "assets/img/tela-relatorios.jpg",
      url: "documentos",
      title: "Documentos e boletins · emissão confiável",
      desc: "Boletins e documentos oficiais com validação pública por QR Code — atendimento mais rápido ao cidadão.",
      pros: [
        "Emissão sem depender de processo manual demorado",
        "Autenticidade verificável pela família",
        "Padronização dos documentos da rede",
      ],
    },
    {
      src: "assets/img/tela-servlitcys.jpg",
      url: "servlitcys",
      title: "SERVLITCYS · indicadores para decidir",
      desc: "Painéis e mapa territorial cruzando i-Educar com FUNDEB, Censo e SAEB — leitura gerencial do município.",
      pros: [
        "Apoia priorização e diagnóstico da rede",
        "Une dado operacional e contexto público",
        "Linguagem de painel para reunião de gestão",
      ],
    },
    {
      src: "assets/img/tela-moodle.jpg",
      url: "moodle",
      title: "Moodle · capacitação sem parar a rede",
      desc: "Ambiente de treinamento híbrido: trilhas online por perfil com apoio presencial na implantação.",
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
