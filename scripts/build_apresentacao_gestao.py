#!/usr/bin/env python3
"""Gera docs/apresentacao-gestao-educacional.pdf — material gerencial atualizado."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "apresentacao-gestao-educacional.pdf"
IMG = ROOT / "assets" / "img"
ICON_DIR = ROOT / "assets" / "img" / "pdf-icons"
ICON_DIR.mkdir(parents=True, exist_ok=True)

# Formato próximo ao original (16:9)
W, H = 960, 540
MARGIN = 36
TOTAL = 16

INK = HexColor("#03161b")
INK2 = HexColor("#0a2a31")
MINT = HexColor("#0e7f6c")
MINT2 = HexColor("#17a58b")
FOAM = HexColor("#eef3f2")
SAND = HexColor("#b8891a")
SAND_SOFT = HexColor("#f5ead0")
MUTED = HexColor("#4f676d")
LINE = HexColor("#d5e0dd")
PAPER = white


def make_icon(name: str, kind: str, bg: tuple[int, int, int]) -> Path:
    path = ICON_DIR / f"{name}.png"
    size = 128
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((8, 8, 120, 120), fill=bg + (255,))
    ink = (244, 255, 251, 255)
    dark = (3, 22, 27, 255)
    stroke = ink if sum(bg) < 420 else dark
    w = 7
    if kind == "school":
        d.line([(34, 92), (94, 92)], fill=stroke, width=w)
        d.line([(40, 92), (40, 62), (64, 42), (88, 62), (88, 92)], fill=stroke, width=w)
        d.rectangle([56, 70, 72, 92], outline=stroke, width=w - 2)
    elif kind == "person":
        d.ellipse((48, 30, 80, 62), outline=stroke, width=w)
        d.arc((34, 68, 94, 118), 200, 340, fill=stroke, width=w)
    elif kind == "users":
        d.ellipse((30, 34, 56, 60), outline=stroke, width=w - 1)
        d.ellipse((72, 34, 98, 60), outline=stroke, width=w - 1)
        d.arc((16, 70, 70, 120), 200, 340, fill=stroke, width=w - 1)
        d.arc((58, 70, 112, 120), 200, 340, fill=stroke, width=w - 1)
    elif kind == "bus":
        d.rounded_rectangle((28, 44, 100, 86), radius=10, outline=stroke, width=w)
        d.line([(28, 64), (100, 64)], fill=stroke, width=w - 2)
        d.ellipse((40, 82, 56, 98), outline=stroke, width=w - 2)
        d.ellipse((72, 82, 88, 98), outline=stroke, width=w - 2)
    elif kind == "chart":
        d.line([(36, 96), (36, 36), (96, 36)], fill=stroke, width=w - 1)
        d.rectangle([46, 70, 56, 96], fill=stroke)
        d.rectangle([64, 54, 74, 96], fill=stroke)
        d.rectangle([82, 42, 92, 96], fill=stroke)
    elif kind == "book":
        d.rounded_rectangle((38, 30, 90, 100), radius=6, outline=stroke, width=w)
        d.line([(48, 30), (48, 100)], fill=stroke, width=w - 2)
    elif kind == "clipboard":
        d.rounded_rectangle((40, 36, 88, 104), radius=8, outline=stroke, width=w)
        d.rounded_rectangle((52, 28, 76, 44), radius=4, outline=stroke, width=w - 2)
        d.line([(52, 60), (76, 60)], fill=stroke, width=w - 2)
        d.line([(52, 74), (76, 74)], fill=stroke, width=w - 2)
    elif kind == "family":
        d.ellipse((34, 34, 60, 60), outline=stroke, width=w - 1)
        d.ellipse((68, 38, 90, 60), outline=stroke, width=w - 1)
        d.arc((20, 70, 74, 118), 200, 340, fill=stroke, width=w - 1)
        d.arc((58, 72, 108, 118), 200, 340, fill=stroke, width=w - 1)
    elif kind == "check":
        d.line([(40, 66), (56, 84), (90, 44)], fill=stroke, width=w + 1)
    elif kind == "flow":
        d.ellipse((28, 52, 52, 76), outline=stroke, width=w - 1)
        d.ellipse((76, 52, 100, 76), outline=stroke, width=w - 1)
        d.line([(52, 64), (76, 64)], fill=stroke, width=w - 1)
        d.polygon([(70, 56), (82, 64), (70, 72)], fill=stroke)
    else:
        d.ellipse((44, 44, 84, 84), outline=stroke, width=w)
    im.save(path, "PNG")
    return path


ICONS = {
    "school": make_icon("school", "school", (14, 127, 108)),
    "person": make_icon("person", "person", (23, 165, 139)),
    "users": make_icon("users", "users", (20, 58, 66)),
    "bus": make_icon("bus", "bus", (58, 81, 102)),
    "chart": make_icon("chart", "chart", (138, 90, 30)),
    "book": make_icon("book", "book", (14, 127, 108)),
    "clipboard": make_icon("clipboard", "clipboard", (23, 165, 139)),
    "family": make_icon("family", "family", (184, 137, 26)),
    "check": make_icon("check", "check", (14, 127, 108)),
    "flow": make_icon("flow", "flow", (23, 165, 139)),
}


def wrap(c: canvas.Canvas, text: str, font: str, size: float, max_w: float) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(c, lines, x, y, font, size, leading, color, max_lines=12):
    c.setFillColor(color)
    c.setFont(font, size)
    for i, line in enumerate(lines[:max_lines]):
        c.drawString(x, y - i * leading, line)


def footer(c, page: int):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(MARGIN, 28, W - MARGIN, 28)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 14, "iEducar - Gestão Educacional em Rede")
    c.drawCentredString(W / 2, 14, "Cooperação Buriti · LibreCode · upstream Portábilis")
    c.drawRightString(W - MARGIN, 14, f"{page} / {TOTAL}")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, 4, "Uso em reunião de gestão · dado indicativo não substitui o FNDE")


def header(c, section: str):
    c.setFillColor(FOAM)
    c.rect(0, H - 42, W, 42, fill=1, stroke=0)
    c.setFillColor(MINT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, H - 26, "iEducar")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN + 48, H - 26, "· Gestão Educacional em Rede")
    c.setFillColor(MINT)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(W - MARGIN, H - 26, section)


def icon(c, name: str, x: float, y: float, size: float = 28):
    c.drawImage(ImageReader(str(ICONS[name])), x, y, width=size, height=size, mask="auto")


def logos_small(c, x=MARGIN, y=34):
    try:
        c.drawImage(ImageReader(str(IMG / "brand-mark.png")), x, y, width=22, height=22, mask="auto")
        c.drawImage(ImageReader(str(IMG / "logo-buriti.png")), x + 28, y + 1, width=20, height=19, mask="auto")
        c.drawImage(ImageReader(str(IMG / "librecode.png")), x + 54, y + 3, width=42, height=16, mask="auto")
    except Exception:
        pass


def card(c, x, y, w, h, fill=FOAM):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=0)


def compare_table(c, rows, y_top, row_h=42):
    """rows: (tema, sem, com)"""
    col1, col2, col3 = 110, 340, 340
    x0 = MARGIN
    # header
    c.setFillColor(INK2)
    c.roundRect(x0, y_top - 26, col1 + col2 + col3, 26, 6, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0 + 10, y_top - 17, "Tema")
    c.drawString(x0 + col1 + 10, y_top - 17, "Sem o conjunto")
    c.drawString(x0 + col1 + col2 + 10, y_top - 17, "Com o conjunto")
    y = y_top - 26
    for i, (tema, sem, com) in enumerate(rows):
        y -= row_h
        bg = FOAM if i % 2 == 0 else PAPER
        c.setFillColor(bg)
        c.rect(x0, y, col1 + col2 + col3, row_h, fill=1, stroke=0)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(x0 + col1, y, x0 + col1, y + row_h)
        c.line(x0 + col1 + col2, y, x0 + col1 + col2, y + row_h)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x0 + 10, y + row_h - 16, tema)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        draw_lines(c, wrap(c, sem, "Helvetica", 8, col2 - 18), x0 + col1 + 10, y + row_h - 16, "Helvetica", 8, 10, MUTED, 3)
        c.setFillColor(MINT)
        draw_lines(c, wrap(c, com, "Helvetica", 8, col3 - 18), x0 + col1 + col2 + 10, y + row_h - 16, "Helvetica", 8, 10, MINT, 3)


def flow_boxes(c, items, y, box_w=118, box_h=64, gap=14):
    """items: list of (icon, title, subtitle)"""
    n = len(items)
    total_w = n * box_w + (n - 1) * gap
    x = (W - total_w) / 2
    for i, (ic, title, sub) in enumerate(items):
        bx = x + i * (box_w + gap)
        card(c, bx, y, box_w, box_h, FOAM)
        icon(c, ic, bx + 10, y + box_h - 34, 24)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 9)
        draw_lines(c, wrap(c, title, "Helvetica-Bold", 9, box_w - 20), bx + 10, y + 28, "Helvetica-Bold", 9, 11, INK, 2)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.5)
        draw_lines(c, wrap(c, sub, "Helvetica", 7.5, box_w - 20), bx + 10, y + 14, "Helvetica", 7.5, 9, MUTED, 2)
        if i < n - 1:
            c.setStrokeColor(MINT2)
            c.setLineWidth(2)
            ax = bx + box_w + 2
            c.line(ax, y + box_h / 2, ax + gap - 4, y + box_h / 2)
            c.line(ax + gap - 10, y + box_h / 2 + 4, ax + gap - 4, y + box_h / 2)
            c.line(ax + gap - 10, y + box_h / 2 - 4, ax + gap - 4, y + box_h / 2)


def build():
    c = canvas.Canvas(str(OUT), pagesize=(W, H))

    # ========== 1 COVER ==========
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(INK2)
    c.rect(0, 0, W * 0.42, H, fill=1, stroke=0)
    try:
        c.drawImage(ImageReader(str(IMG / "brand-mark.png")), 40, H - 120, width=72, height=72, mask="auto")
    except Exception:
        pass
    c.setFillColor(MINT2)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, H - 150, "APRESENTAÇÃO PARA A GESTÃO")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(40, H - 200, "iEducar")
    c.setFillColor(HexColor("#d8f1ea"))
    c.setFont("Helvetica", 16)
    c.drawString(40, H - 226, "Gestão Educacional em Rede")
    c.setFillColor(HexColor("#a8c0c4"))
    c.setFont("Helvetica", 10)
    for i, line in enumerate(
        [
            "A educação do município em um só fio.",
            "Da família que pede a vaga até o número",
            "que a gestão lê na reunião de governo.",
            "",
            "Software Público Brasileiro · GPL v2",
            "Upstream Portábilis",
            "Cooperação Buriti · LibreCode",
        ]
    ):
        c.drawString(40, H - 265 - i * 16, line)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(W * 0.48, H - 100, "Oferta para a rede municipal")
    # three pillars
    pillars = [
        ("school", "1 cadastro", "O aluno nasce uma vez no iEducar."),
        ("flow", "O ano inteiro", "Diário, transporte e censo usam a mesma matrícula."),
        ("chart", "Decisão", "SERVLITCYS e Power BI leem a rede, não uma cópia manual."),
    ]
    for i, (ic, t, d) in enumerate(pillars):
        y = H - 170 - i * 80
        card(c, W * 0.48, y, W * 0.44, 68, HexColor("#0f2c32"))
        icon(c, ic, W * 0.48 + 14, y + 30, 28)
        c.setFillColor(MINT2)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(W * 0.48 + 54, y + 42, t)
        c.setFillColor(HexColor("#c5d6d9"))
        c.setFont("Helvetica", 9)
        draw_lines(c, wrap(c, d, "Helvetica", 9, W * 0.44 - 70), W * 0.48 + 54, y + 26, "Helvetica", 9, 11, HexColor("#c5d6d9"), 2)

    try:
        c.drawImage(ImageReader(str(IMG / "logo-buriti.png")), W * 0.48, 48, width=36, height=34, mask="auto")
        c.drawImage(ImageReader(str(IMG / "librecode.png")), W * 0.48 + 50, 52, width=70, height=28, mask="auto")
    except Exception:
        pass
    c.setFillColor(HexColor("#7a9499"))
    c.setFont("Helvetica", 8)
    c.drawString(40, 20, "buriti.dev.br · librecode.coop · ieducar.org")
    c.drawRightString(W - MARGIN, 20, "1 / 16")
    c.showPage()

    # ========== 2 BEFORE/AFTER ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "O desafio")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, H - 78, "O que a secretaria já vive")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "O município cumpre a lei com gente dedicada e com sistemas que não conversam. "
            "O número da matrícula, o do ônibus, o do diário e o do Censo Escolar nascem em lugares diferentes.",
            "Helvetica",
            10,
            W - 2 * MARGIN,
        ),
        MARGIN,
        H - 100,
        "Helvetica",
        10,
        13,
        MUTED,
        3,
    )
    compare_table(
        c,
        [
            ("Matrícula", "Fila, papel e cadastro repetido a cada ano", "A família entra pelo processo; a escola confirma no mesmo aluno"),
            ("Sala de aula", "Frequência e conteúdo fora do cadastro", "O diário grava em cima da matrícula que já existe"),
            ("Transporte", "Lista do ônibus diferente da lista da escola", "Uma pessoa, um assento por turno, ligada à matrícula"),
            ("Censo", "Correria em abril e medo de perder aluno no FUNDEB", "A base do ano já é a base que o INEP vai receber"),
            ("Gestão", "Cada diretor manda um número", "O painel mostra a rede, com a origem do dado"),
        ],
        H - 145,
        row_h=48,
    )
    footer(c, 2)
    c.showPage()

    # ========== 3 FLOW ONE DATA ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Fluxo do dado")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, H - 78, "Uma informação, vários usos")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "O aluno e a matrícula nascem no iEducar. Transporte, diário, pré-matrícula, censo e painéis consomem esse fato. "
            "Ninguém redigita o nome para bater o relatório.",
            "Helvetica",
            10,
            W - 2 * MARGIN,
        ),
        MARGIN,
        H - 100,
        "Helvetica",
        10,
        13,
        MUTED,
        2,
    )
    flow_boxes(
        c,
        [
            ("family", "Família pede vaga", "Pré-matrícula digital"),
            ("school", "Escola efetiva", "Matrícula no iEducar"),
            ("book", "Professor dá aula", "i-Diário na turma"),
            ("bus", "Criança embarca", "Rota do mesmo aluno"),
            ("clipboard", "INEP pergunta", "Educacenso"),
            ("chart", "Gestão pergunta", "SERVLITCYS / BI"),
        ],
        210,
        box_w=130,
        box_h=78,
        gap=12,
    )
    card(c, MARGIN, 70, W - 2 * MARGIN, 100, HexColor("#e8f6f2"))
    icon(c, "check", MARGIN + 16, 120, 32)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 60, 140, "Regra de ouro")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "Se o dado não está na matrícula, ele não entra no censo, no ônibus nem no painel. Corrigir na origem corrige o resto.",
            "Helvetica",
            10,
            W - 2 * MARGIN - 80,
        ),
        MARGIN + 60,
        120,
        "Helvetica",
        10,
        13,
        MUTED,
        3,
    )
    footer(c, 3)
    c.showPage()

    # ========== 4 MODULES GRID ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Pacote")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, H - 78, "O que a cidade passa a operar junto")
    mods = [
        ("school", "iEducar", "Escola, turma, matrícula, histórico, documentos e usuários."),
        ("book", "i-Diário", "Frequência, conteúdo e avaliação na turma já matriculada."),
        ("family", "Pré-matrícula", "Processo aberto ao público, sem fila só no balcão."),
        ("bus", "Transporte", "Rota, vaga, pedido da família e aluno no ônibus."),
        ("clipboard", "Educacenso", "A etapa do INEP sai do cadastro, não de planilha paralela."),
        ("users", "Relatórios", "A secretaria tira a lista que a escola e o conselho pedem."),
        ("chart", "SERVLITCYS", "Diagnóstico, mapa, censo, FUNDEB e projeção por município."),
        ("flow", "Power BI e Moodle", "Painel da gestão e formação híbrida da equipe."),
    ]
    for i, (ic, t, d) in enumerate(mods):
        col, row = i % 4, i // 4
        x = MARGIN + col * 225
        y = H - 200 - row * 150
        card(c, x, y, 210, 130)
        icon(c, ic, x + 14, y + 88, 30)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 54, y + 100, t)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        draw_lines(c, wrap(c, d, "Helvetica", 9, 180), x + 14, y + 70, "Helvetica", 9, 12, MUTED, 4)
    footer(c, 4)
    c.showPage()

    # ========== 5 IEDUCAR ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Núcleo")
    icon(c, "school", MARGIN, H - 88, 36)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN + 48, H - 78, "iEducar: a rotina que a lei já exige")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "É o sistema de gestão escolar da rede. A secretaria deixa de depender do caderno da escola para saber quem está matriculado, em qual turma, em qual turno e com qual situação.",
            "Helvetica",
            10,
            W - 2 * MARGIN,
        ),
        MARGIN,
        H - 110,
        "Helvetica",
        10,
        13,
        MUTED,
        3,
    )
    blocks = [
        ("Gente e vaga", "Pessoa, aluno, matrícula, transferência, abandono, reclassificação e histórico."),
        ("Organização", "Escola, curso, série, turma, quadro de horário, calendário e usuários por perfil."),
        ("Ano letivo", "Rematrícula, enturmação e a base que o censo, o diário e o transporte vão ler."),
    ]
    for i, (t, d) in enumerate(blocks):
        x = MARGIN + i * 300
        card(c, x, 160, 285, 160)
        c.setFillColor(MINT)
        c.circle(x + 24, 280, 8, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 42, 274, t)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 10)
        draw_lines(c, wrap(c, d, "Helvetica", 10, 250), x + 18, 240, "Helvetica", 10, 14, MUTED, 5)
    card(c, MARGIN, 70, W - 2 * MARGIN, 70, SAND_SOFT)
    c.setFillColor(SAND)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 18, 112, "Para o secretário")
    c.setFillColor(INK)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "O ganho não é ter mais um sistema. É poder afirmar, com data, quantos alunos a rede tem e em que condição eles estão.",
            "Helvetica",
            10,
            W - 2 * MARGIN - 40,
        ),
        MARGIN + 18,
        92,
        "Helvetica",
        10,
        13,
        INK,
        2,
    )
    footer(c, 5)
    c.showPage()

    # ========== 6 IDIARIO ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Microssistema")
    icon(c, "book", MARGIN, H - 88, 36)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN + 48, H - 78, "i-Diário: a aula deixa de ser invisível")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "O professor registra frequência, conteúdo e avaliação na turma que já existe no iEducar. A direção vê atraso de lançamento. A secretaria vê a frequência da rede sem pedir planilha no fim do mês.",
            "Helvetica",
            10,
            W - 2 * MARGIN,
        ),
        MARGIN,
        H - 105,
        "Helvetica",
        10,
        13,
        MUTED,
        3,
    )
    compare_table(
        c,
        [
            ("Chamada", "A falta só aparece no boletim", "O professor registra no dia, na turma certa"),
            ("Conteúdo", "O caderno não chega à supervisão", "A supervisão acompanha o que foi dado"),
            ("Avaliação", "Nota em planilha solta", "Nota e parecer nascem na turma"),
            ("Fechamento", "Retrabalho no conselho de classe", "A secretaria fecha o que já foi lançado"),
        ],
        H - 155,
        row_h=50,
    )
    footer(c, 6)
    c.showPage()

    # ========== 7 PREMATRICULA ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Porta de entrada")
    icon(c, "family", MARGIN, H - 88, 36)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN + 48, H - 78, "Pré-matrícula: a família entra sem esperar o balcão")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "Na entrada do iEducar aparece o acesso à pré-matrícula. Cada processo em andamento tem o seu caminho. A inscrição não exige usuário de servidor.",
            "Helvetica",
            10,
            W - 2 * MARGIN,
        ),
        MARGIN,
        H - 105,
        "Helvetica",
        10,
        13,
        MUTED,
        2,
    )
    compare_table(
        c,
        [
            ("Acesso", "Fila no balcão e cadastro repetido", "Inscrição e protocolo fora do horário da escola"),
            ("Controle", "Período combinado de boca", "Etapa, série e escola definidos; processo fechado não recebe inscrição"),
            ("Efeito", "Primeira semana lotada", "A matrícula definitiva continua sendo ato da escola"),
        ],
        H - 150,
        row_h=55,
    )
    # mini flowchart
    flow_boxes(
        c,
        [
            ("family", "Família se inscreve", "Protocolo público"),
            ("users", "SME regula", "Critérios e vagas"),
            ("school", "Escola efetiva", "Matrícula oficial"),
        ],
        70,
        box_w=200,
        box_h=70,
        gap=30,
    )
    footer(c, 7)
    c.showPage()

    # ========== 8 TRANSPORTE ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Logística")
    icon(c, "bus", MARGIN, H - 88, 36)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN + 48, H - 78, "Transporte: vaga, rota e quem embarca")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "O módulo liga a matrícula à rota. A família pede. A rede analisa. Uma pessoa ocupa um assento por turno: outra matrícula no mesmo turno não abre um segundo lugar. Manhã e tarde são duas viagens.",
            "Helvetica",
            10,
            W - 2 * MARGIN,
        ),
        MARGIN,
        H - 105,
        "Helvetica",
        10,
        13,
        MUTED,
        3,
    )
    compare_table(
        c,
        [
            ("Vaga", "Lista do ônibus à parte da matrícula", "Lugar publicado por escola, rota e turno"),
            ("Pedido", "Pedido sem protocolo", "Recebido, em análise, aceito, conferido ou espera"),
            ("Quem embarca", "O mesmo aluno conta duas vezes", "Um assento por turno; a lista do ano inteiro"),
            ("Censo", "Transporte informado de memória", "A ficha acompanha a rota municipal"),
        ],
        H - 155,
        row_h=48,
    )
    footer(c, 8)
    c.showPage()

    # ========== 9 CENSO ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Censo e documentos")
    icon(c, "clipboard", MARGIN, H - 88, 36)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN + 48, H - 78, "Educacenso e relatórios")
    compare_table(
        c,
        [
            ("Censo", "Força-tarefa de abril e planilha paralela", "A exportação sai do cadastro que a escola já mantém"),
            ("Pendência", "O erro aparece depois do envio", "A pendência é corrigida antes, no mesmo aluno"),
            ("Relatório", "Cada um soma um total", "A lista sai do sistema, no recorte de quem consulta"),
            ("FUNDEB", "Aluno invisível no ano seguinte", "O censo fecha a rotina que começou na matrícula"),
        ],
        H - 120,
        row_h=55,
    )
    footer(c, 9)
    c.showPage()

    # ========== 10 SERVLITCYS ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Analytics")
    icon(c, "chart", MARGIN, H - 88, 36)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN + 48, H - 78, "SERVLITCYS: a secretaria lê o município")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "Plataforma analítica ligada à base do iEducar de cada cidade. Não substitui a matrícula. Responde o que a gestão pergunta depois que a matrícula existe.",
            "Helvetica",
            10,
            W - 2 * MARGIN,
        ),
        MARGIN,
        H - 105,
        "Helvetica",
        10,
        13,
        MUTED,
        2,
    )
    mods = [
        ("Painel analítico", "Resumo, cadastro, pedagógico, censo e finanças da rede"),
        ("Horizonte", "Onde está a oportunidade: mapa da rede e do território"),
        ("Clio", "Coleta e leitura da 1ª etapa do Educacenso"),
        ("RX Censo", "O que a base ainda não sustenta na hora de exportar"),
        ("Projeção", "Ordem de grandeza do próximo FUNDEB, a partir da matrícula"),
        ("FUNDEB", "Discrepância de cadastro e leitura de repasses (valor indicativo)"),
    ]
    for i, (t, d) in enumerate(mods):
        col, row = i % 3, i // 3
        x = MARGIN + col * 300
        y = H - 220 - row * 120
        card(c, x, y, 285, 100)
        c.setFillColor(MINT)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x + 16, y + 70, t)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        draw_lines(c, wrap(c, d, "Helvetica", 9, 250), x + 16, y + 50, "Helvetica", 9, 12, MUTED, 3)
    footer(c, 10)
    c.showPage()

    # ========== 11 POWER BI ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Gabinete")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, H - 78, "Power BI: o painel que a gestão já abre")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "A SERVLITCYS fala a língua da educação: censo, FUNDEB, mapa, discrepância. O Power BI fala a língua do governo: indicador, meta e comparação na reunião de secretariado.",
            "Helvetica",
            10,
            W - 2 * MARGIN,
        ),
        MARGIN,
        H - 105,
        "Helvetica",
        10,
        13,
        MUTED,
        3,
    )
    compare_table(
        c,
        [
            ("Origem", "Arquivo montado na sexta-feira", "Matrícula, frequência, transporte e censo"),
            ("Recorte", "Planilha que não filtra a rede", "Escola, etapa ou turno no próprio painel"),
            ("Leitura", "Cada secretaria leva o seu número", "iEducar opera, SERVLITCYS interpreta, Power BI publica o mesmo aluno"),
        ],
        H - 160,
        row_h=55,
    )
    flow_boxes(
        c,
        [
            ("school", "iEducar opera", "Fato na matrícula"),
            ("chart", "SERVLITCYS interpreta", "Diagnóstico da rede"),
            ("flow", "Power BI publica", "Reunião de gestão"),
        ],
        70,
        box_w=200,
        box_h=70,
        gap=30,
    )
    footer(c, 11)
    c.showPage()

    # ========== 12 MOODLE ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Capacitação")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, H - 78, "Formação híbrida, com Moodle")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "Sistema sem gente treinada vira senha compartilhada. O Moodle, software livre, é a sala permanente da rede. O encontro presencial resolve matrícula de pico, censo e transporte.",
            "Helvetica",
            10,
            W - 2 * MARGIN,
        ),
        MARGIN,
        H - 105,
        "Helvetica",
        10,
        13,
        MUTED,
        3,
    )
    rows = [
        ("Prefeito e secretário", "Uma manhã: o que o painel responde", "Trilha curta e glossário da rede"),
        ("Equipe da secretaria", "Oficinas de matrícula, censo e relatório", "Passo a passo e exercício em base de treino"),
        ("Direção e secretaria", "Semana da rematrícula e do diário", "Videoaula curta e lista de pendências"),
        ("Professor", "Chamada e conteúdo no i-Diário", "Módulo no horário da hora-atividade"),
        ("Transporte", "Rota, vaga e aluno no ônibus", "Simulado de pedido e de lista"),
    ]
    # custom 3-col header
    c.setFillColor(INK2)
    c.roundRect(MARGIN, H - 145, W - 2 * MARGIN, 26, 6, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN + 10, H - 136, "Público")
    c.drawString(MARGIN + 220, H - 136, "Presencial")
    c.drawString(MARGIN + 520, H - 136, "No Moodle")
    y = H - 145
    for i, (a, b, d) in enumerate(rows):
        y -= 42
        c.setFillColor(FOAM if i % 2 == 0 else PAPER)
        c.rect(MARGIN, y, W - 2 * MARGIN, 42, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(MARGIN + 10, y + 16, a)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(MARGIN + 220, y + 16, b)
        c.setFillColor(MINT)
        c.drawString(MARGIN + 520, y + 16, d)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 48, "A aula ao vivo pode usar o BigBlueButton dentro do Moodle. O curso guarda presença e certificado.")
    footer(c, 12)
    c.showPage()

    # ========== 13 WHY SET ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Conjunto")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, H - 78, "Por que este conjunto, e não peças soltas")
    compare_table(
        c,
        [
            ("Prefeito", "Surpresa no FUNDEB, no ônibus e na fila de janeiro", "A rede está no sistema e o painel lê a rede"),
            ("Secretário", "A pendência chega depois do ofício", "Matrícula, aula, ônibus e censo na mesma rotina"),
            ("Escola", "O aluno é recadastrado em três lugares", "A família chega com protocolo; o professor lança na turma"),
            ("Controle", "Planilha aberta e número sem origem", "Cada perfil vê o que lhe cabe; o dado tem origem"),
        ],
        H - 120,
        row_h=55,
    )
    card(c, MARGIN, 55, W - 2 * MARGIN, 55, SAND_SOFT)
    c.setFillColor(INK)
    c.setFont("Helvetica", 9)
    draw_lines(
        c,
        wrap(
            c,
            "O conjunto não fecha sozinho a prestação do PNATE, não paga folha e não substitui o nutricionista da merenda. "
            "O produto desta conversa é matrícula, aula, transporte, censo e a leitura desses dados.",
            "Helvetica",
            9,
            W - 2 * MARGIN - 30,
        ),
        MARGIN + 14,
        88,
        "Helvetica",
        9,
        12,
        INK,
        3,
    )
    footer(c, 13)
    c.showPage()

    # ========== 14 IMPACT ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Impacto")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, H - 78, "Impacto na educação")
    compare_table(
        c,
        [
            ("Criança rural", "Dois cadastros ocupam dois bancos", "A vaga segue a matrícula e o turno"),
            ("Família", "Depende do horário do balcão", "Pede a vaga e acompanha o protocolo"),
            ("Professor", "Caderno paralelo à turma", "Registra a aula onde a turma já está"),
            ("Direção", "A falta aparece no conselho", "Vê falta, enturmação e documento antes"),
            ("Secretaria", "Força-tarefa de abril", "O censo usa a base do ano"),
            ("Gestão", "Cada um traz um total", "Escola, etapa e financiamento no mesmo critério"),
        ],
        H - 110,
        row_h=42,
    )
    footer(c, 14)
    c.showPage()

    # ========== 15 EFFICIENCY ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Dados")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, H - 78, "Eficiência dos dados educacionais")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, H - 100, "Dado eficiente é dado que nasce uma vez, no fato certo, e chega íntegro até a decisão.")
    compare_table(
        c,
        [
            ("Censo", "Redigitar o aluno", "Exporta o cadastro que a escola já mantém"),
            ("Ônibus", "Outra planilha", "O aluno da rota é o da matrícula"),
            ("Frequência", "Não volta à secretaria", "O diário grava na turma"),
            ("Total", "Cada um soma diferente", "A mesma regra de matrícula ativa"),
            ("Formação", "A oficina acaba no dia", "O Moodle guarda o passo a passo"),
        ],
        H - 130,
        row_h=48,
    )
    footer(c, 15)
    c.showPage()

    # ========== 16 HOW TO ENTER ==========
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, "Entrada")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGIN, H - 78, "Como a cidade entra")
    steps = [
        ("1", "Base", "iEducar no ar, escolas e usuários, ano letivo aberto", "school"),
        ("2", "Porta de entrada", "Pré-matrícula no período que a secretaria definir", "family"),
        ("3", "Sala", "i-Diário nas turmas, com formação do professor", "book"),
        ("4", "Deslocamento", "Rotas, vagas e alunos no transporte do ano", "bus"),
        ("5", "Conta oficial", "Educacenso e relatórios da secretaria", "clipboard"),
        ("6", "Gestão", "SERVLITCYS ligada à cidade e painel Power BI", "chart"),
        ("7", "Gente", "Cursos no Moodle e encontros presenciais de pico", "users"),
    ]
    for i, (n, t, d, ic) in enumerate(steps):
        y = H - 120 - i * 42
        c.setFillColor(MINT if i % 2 == 0 else MINT2)
        c.circle(MARGIN + 16, y + 10, 12, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(MARGIN + 16, y + 6, n)
        if i < len(steps) - 1:
            c.setStrokeColor(LINE)
            c.setLineWidth(2)
            c.line(MARGIN + 16, y - 2, MARGIN + 16, y - 30)
        icon(c, ic, MARGIN + 40, y - 2, 22)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN + 72, y + 10, t)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN + 220, y + 10, d)

    # CTA box
    c.setFillColor(INK)
    c.roundRect(W - 340, 55, 300, 110, 12, fill=1, stroke=0)
    c.setFillColor(MINT2)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(W - 320, 140, "PRÓXIMO PASSO")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    draw_lines(
        c,
        wrap(
            c,
            "Escolher o ano letivo de entrada, as escolas piloto e quem da secretaria será o dono de matrícula, de censo e de transporte.",
            "Helvetica-Bold",
            10,
            260,
        ),
        W - 320,
        120,
        "Helvetica-Bold",
        10,
        13,
        white,
        3,
    )
    c.setFillColor(MINT2)
    c.setFont("Helvetica", 8)
    c.drawString(W - 320, 70, "buriti.dev.br/public/#contato")
    logos_small(c, MARGIN, 40)
    footer(c, 16)
    c.showPage()

    c.save()
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
