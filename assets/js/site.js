(() => {
  const ALBUM = [
    {
      src: "assets/img/tela-login.jpg?v=buriti1",
      url: "entrada · login",
      title: "Entrada · Portal da SME",
      desc: "Login em duas colunas no tema Buriti: acesso interno da rede e portas externas (i-Diário, transporte, documentos e ACT) sem cadastro paralelo.",
      pros: [
        "Uma porta oficial para servidores e para a família",
        "Serviços externos visíveis antes mesmo do login",
        "Identidade visual alinhada aos módulos Buriti",
      ],
    },
    {
      src: "assets/img/tela-ieducar-gestao.jpg?v=buriti1",
      url: "painel da secretaria",
      title: "Rede · Painel Buriti",
      desc: "Ponto de partida da operação: módulos da rede, caixa do dia e badges de pendência — a secretaria vê o que precisa agir sem planilha.",
      pros: [
        "Catálogo de módulos com contadores operacionais",
        "Caixa do dia com busca ativa e notificações",
        "Rodapé com status da operação e hora de atualização",
      ],
    },
    {
      src: "assets/img/tela-busca-ativa.jpg?v=buriti1",
      url: "busca ativa",
      title: "Estudante · Busca Ativa",
      desc: "Detecta infrequência nos cursos marcados, abre processos e acompanha a família — ponte com atendimento e Apps API.",
      pros: [
        "Alertas e processos na mesma base da matrícula",
        "Regras por curso e limite de faltas configuráveis",
        "Integração com fila de atendimento e família",
      ],
    },
    {
      src: "assets/img/tela-atendimento.jpg?v=buriti1",
      url: "atendimento",
      title: "Estudante · Atendimento",
      desc: "Fila, agenda e registro de acolhimento com histórico do estudante — o cuidado entra no fluxo da rede.",
      pros: [
        "Fila e agenda na mesma tela operacional",
        "Registro com anexos e devolutiva",
        "Equipe autorizada e histórico por aluno",
      ],
    },
    {
      src: "assets/img/tela-transporte.jpg?v=buriti1",
      url: "transporte",
      title: "Rede · Transporte escolar",
      desc: "Sala de controle da frota no tema Buriti: rotas, alunos, viagens, pedidos da família e mapa.",
      pros: [
        "Ocupação alinhada ao aluno matriculado",
        "Fila de atenção para pedidos e prazos",
        "Portal da família na mesma solução",
      ],
    },
    {
      src: "assets/img/tela-alimentacao.jpg?v=buriti1",
      url: "alimentação",
      title: "Rede · Alimentação escolar",
      desc: "Cardápio do dia, restrições com laudo e mapa de distribuição PNAE — da cozinha à escola.",
      pros: [
        "Bandeja por escola e por data",
        "Restrições alimentares visíveis antes de servir",
        "Catálogo PNAE e agricultura familiar",
      ],
    },
    {
      src: "assets/img/tela-horario.jpg?v=buriti1",
      url: "quadro de horários",
      title: "Rede · Quadro de horários",
      desc: "Matriz, verificação de demanda, geração automática e conflitos — grade sem choque para a rede.",
      pros: [
        "Passo a passo da matriz à publicação",
        "Detecção de choque de professor e turma",
        "Versões vigentes com histórico preservado",
      ],
    },
    {
      src: "assets/img/tela-eventos.jpg?v=buriti1",
      url: "eventos e formação",
      title: "Formação · Eventos",
      desc: "Cursos e palestras com inscrição, presença e certificados — formação continuada na mesma identidade Buriti.",
      pros: [
        "Cadastro de evento com vagas e carga horária",
        "Controle de inscrição e frequência",
        "Emissão de certificados no fluxo",
      ],
    },
    {
      src: "assets/img/tela-biblioteca.jpg?v=buriti1",
      url: "biblioteca",
      title: "Escola · Biblioteca",
      desc: "Acervo, empréstimos e inventário escolar no padrão Buriti — leitura ligada ao aluno da rede.",
      pros: [
        "Acervo e circulação na escola",
        "Empréstimos com comprovante",
        "Visão para a família via Apps API",
      ],
    },
    {
      src: "assets/img/tela-almoxarifado.jpg?v=buriti1",
      url: "almoxarifado",
      title: "Rede · Almoxarifado escolar",
      desc: "Estoque, pedidos e entregas entre SME e escolas — remessas rastreáveis sem planilha paralela.",
      pros: [
        "Pedidos escola → SME com assinatura",
        "Saldos e movimentos por item",
        "Nota e fechamento do pedido",
      ],
    },
    {
      src: "assets/img/tela-act.jpg?v=buriti1",
      url: "contratações temporárias",
      title: "RH · Contratações (ACT)",
      desc: "Editais, inscrição do candidato, classificação e escolha de vagas — portal externo e operação interna no mesmo módulo.",
      pros: [
        "Portal do candidato sem login interno",
        "Processos, comissão e recursos",
        "Alocação e admissão na rede",
      ],
    },
    {
      src: "assets/img/tela-idiario.jpg?v=buriti1",
      url: "i-diario",
      title: "Sala · i-Diário",
      desc: "O professor lança na sala e a SME já lê frequência e notas — microssistema na mesma base, com SSO.",
      pros: [
        "Acaba a digitação duplicada",
        "Fecha período com menos atraso",
        "Apoia busca ativa e boletim",
      ],
    },
  ]

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

  // Fluxo de implantação no cabeçalho fixo
  const navLinks = [...document.querySelectorAll(".nav-flow-list a[href^='#']")];
  const sectionIds = navLinks.map((a) => a.getAttribute("href").slice(1));
  const sections = sectionIds
    .map((id) => document.getElementById(id))
    .filter(Boolean);

  const setActiveNav = (id) => {
    const activeIndex = sectionIds.indexOf(id);
    navLinks.forEach((a, index) => {
      const on = index === activeIndex;
      const done = activeIndex > -1 && index < activeIndex;
      a.classList.toggle("is-active", on);
      a.classList.toggle("is-done", done);
      a.parentElement?.classList.toggle("is-active-step", on);
      a.parentElement?.classList.toggle("is-done-step", done);
      if (on) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    });
  };

  const syncActiveNav = () => {
    if (!sections.length) return;
    const header = document.querySelector(".site-header");
    const marker = (header?.offsetHeight || 78) + 28;
    let current = sectionIds[0];
    for (const el of sections) {
      const top = el.getBoundingClientRect().top;
      if (top - marker <= 0) current = el.id;
    }
    // final da página (ex.: fechar-decisão) mantém a última etapa ativa
    const docEnd =
      window.scrollY + window.innerHeight >=
      document.documentElement.scrollHeight - 12;
    if (docEnd) current = sectionIds[sectionIds.length - 1];
    setActiveNav(current);
  };

  if (sections.length) {
    syncActiveNav();
    window.addEventListener("scroll", syncActiveNav, { passive: true });
    window.addEventListener("resize", syncActiveNav);
    navLinks.forEach((a) => {
      a.addEventListener("click", () => {
        const id = a.getAttribute("href")?.slice(1);
        if (id) {
          // reforça o estado ao clicar, antes do scroll terminar
          setActiveNav(id);
          window.setTimeout(syncActiveNav, 350);
        }
      });
    });
  }

  const toTop = document.getElementById("to-top");
  if (toTop) {
    const toggleToTop = () => {
      const show = window.scrollY > 480;
      toTop.hidden = !show;
    };
    toggleToTop();
    window.addEventListener("scroll", toggleToTop, { passive: true });
  }

  // Cookies / privacidade
  const COOKIE_KEY = "ieducar_cookie_consent";
  const banner = document.getElementById("cookie-banner");
  const acceptBtn = document.getElementById("cookie-accept");
  const rejectBtn = document.getElementById("cookie-reject");
  const settingsBtn = document.getElementById("cookie-settings");

  const readConsent = () => {
    try { return localStorage.getItem(COOKIE_KEY); } catch (_) { return null; }
  };
  const writeConsent = (value) => {
    try { localStorage.setItem(COOKIE_KEY, value); } catch (_) {}
  };
  const showBanner = () => {
    if (!banner) return;
    banner.hidden = false;
  };
  const hideBanner = () => {
    if (!banner) return;
    banner.hidden = true;
  };

  if (banner && !readConsent()) showBanner();

  acceptBtn?.addEventListener("click", () => {
    writeConsent("accepted");
    hideBanner();
  });
  rejectBtn?.addEventListener("click", () => {
    writeConsent("essential");
    hideBanner();
  });
  settingsBtn?.addEventListener("click", () => {
    showBanner();
  });
})();
