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
MUTED = HexColor("#2f4a50")
LINE = HexColor("#d5e0dd")
PAPER = white


def make_icon(name: str, kind: str, bg: tuple[int, int, int], light: bool = False) -> Path:
    """Filled silhouettes (survive PDF downscale). light=True = pale disc + dark glyph."""
    path = ICON_DIR / f"{name}{'-light' if light else ''}.png"
    size = 128
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if light:
        d.ellipse((2, 2, 126, 126), fill=(244, 255, 251, 255))
        ink = (10, 79, 69, 255)
        cut = (244, 255, 251, 255)
    else:
        d.ellipse((2, 2, 126, 126), fill=(10, 79, 69, 255))
        ink = (255, 255, 255, 255)
        cut = (10, 79, 69, 255)
    if kind == "school":
        d.polygon([(64, 34), (98, 62), (98, 96), (30, 96), (30, 62)], fill=ink)
        d.rectangle([56, 72, 72, 96], fill=cut)
        d.rectangle([40, 68, 52, 80], fill=cut)
        d.rectangle([76, 68, 88, 80], fill=cut)
    elif kind == "person":
        d.ellipse((46, 28, 82, 64), fill=ink)
        d.pieslice((28, 70, 100, 130), 200, 340, fill=ink)
    elif kind == "users":
        d.ellipse((28, 30, 56, 58), fill=ink)
        d.ellipse((72, 30, 100, 58), fill=ink)
        d.pieslice((12, 64, 72, 124), 200, 340, fill=ink)
        d.pieslice((56, 64, 116, 124), 200, 340, fill=ink)
    elif kind == "bus":
        d.rounded_rectangle((26, 40, 102, 88), radius=12, fill=ink)
        d.rectangle([34, 48, 52, 64], fill=cut)
        d.rectangle([58, 48, 76, 64], fill=cut)
        d.rectangle([82, 48, 94, 64], fill=cut)
        d.ellipse((38, 84, 56, 102), fill=ink)
        d.ellipse((72, 84, 90, 102), fill=ink)
        d.ellipse((42, 88, 52, 98), fill=cut)
        d.ellipse((76, 88, 86, 98), fill=cut)
    elif kind == "chart":
        d.rectangle([40, 68, 54, 98], fill=ink)
        d.rectangle([60, 50, 74, 98], fill=ink)
        d.rectangle([80, 36, 94, 98], fill=ink)
        d.rectangle([34, 98, 100, 106], fill=ink)
    elif kind == "book":
        d.rounded_rectangle((36, 28, 92, 104), radius=8, fill=ink)
        d.rectangle([48, 28, 54, 104], fill=cut)
        d.rectangle([62, 48, 82, 54], fill=cut)
        d.rectangle([62, 64, 82, 70], fill=cut)
    elif kind == "clipboard":
        d.rounded_rectangle((38, 36, 90, 108), radius=10, fill=ink)
        d.rounded_rectangle((50, 26, 78, 44), radius=6, fill=ink)
        d.rectangle([50, 56, 78, 62], fill=cut)
        d.rectangle([50, 72, 78, 78], fill=cut)
        d.rectangle([50, 88, 70, 94], fill=cut)
    elif kind == "family":
        d.ellipse((32, 30, 60, 58), fill=ink)
        d.ellipse((68, 34, 92, 58), fill=ink)
        d.pieslice((16, 64, 76, 124), 200, 340, fill=ink)
        d.pieslice((56, 68, 112, 124), 200, 340, fill=ink)
    elif kind == "check":
        d.line([(38, 66), (56, 86), (94, 42)], fill=ink, width=14)
        d.line([(38, 66), (56, 86), (94, 42)], fill=ink, width=10)
    elif kind == "flow":
        d.ellipse((24, 48, 56, 80), fill=ink)
        d.ellipse((72, 48, 104, 80), fill=ink)
        d.rectangle([52, 58, 76, 70], fill=ink)
        d.polygon([(70, 48), (90, 64), (70, 80)], fill=ink)
    else:
        d.ellipse((40, 40, 88, 88), fill=ink)
    im.save(path, "PNG")
    return path


_BASE = {
    "school": ((14, 127, 108), "school"),
    "person": ((14, 127, 108), "person"),
    "users": ((14, 127, 108), "users"),
    "bus": ((14, 127, 108), "bus"),
    "chart": ((14, 127, 108), "chart"),
    "book": ((14, 127, 108), "book"),
    "clipboard": ((14, 127, 108), "clipboard"),
    "family": ((14, 127, 108), "family"),
    "check": ((14, 127, 108), "check"),
    "flow": ((14, 127, 108), "flow"),
}
ICONS = {k: make_icon(k, kind, bg, False) for k, (bg, kind) in _BASE.items()}
ICONS_LIGHT = {k: make_icon(k, kind, bg, True) for k, (bg, kind) in _BASE.items()}


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
    c.line(MARGIN, 32, W - MARGIN, 32)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 16, "iEducar · Buriti · LibreCode · Portábilis")
    c.drawRightString(W - MARGIN, 16, f"{page} / {TOTAL}")
    c.setFont("Helvetica", 7)
    c.drawCentredString(W / 2, 16, "Uso em reunião de gestão · dado indicativo não substitui o FNDE")


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


def icon(c, name: str, x: float, y: float, size: float = 28, light: bool = False):
    src = ICONS_LIGHT[name] if light else ICONS[name]
    c.drawImage(ImageReader(str(src)), x, y, width=size, height=size, mask="auto")


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
        c.setFillColor(INK2)
        c.setFont("Helvetica", 8)
        draw_lines(c, wrap(c, sem, "Helvetica", 8, col2 - 18), x0 + col1 + 10, y + row_h - 16, "Helvetica", 8, 10, INK2, 3)
        # tint "com" column
        c.setFillColor(HexColor("#e4f5f0"))
        c.rect(x0 + col1 + col2, y, col3, row_h, fill=1, stroke=0)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.line(x0 + col1 + col2, y, x0 + col1 + col2, y + row_h)
        c.setFillColor(INK)
        c.setFont("Helvetica", 8)
        draw_lines(c, wrap(c, com, "Helvetica", 8, col3 - 18), x0 + col1 + col2 + 10, y + row_h - 16, "Helvetica", 8, 10, INK, 3)


def flow_boxes(c, items, y, box_w=118, box_h=86, gap=14):
    """items: list of (icon, title, subtitle)"""
    n = len(items)
    total_w = n * box_w + (n - 1) * gap
    x = max(MARGIN, (W - total_w) / 2)
    for i, (ic, title, sub) in enumerate(items):
        bx = x + i * (box_w + gap)
        c.setFillColor(HexColor("#f4fffb"))
        c.setStrokeColor(LINE)
        c.setLineWidth(1)
        c.roundRect(bx, y, box_w, box_h, 10, fill=1, stroke=1)
        # icon top-centered, text below with clear gap
        icon(c, ic, bx + (box_w - 26) / 2, y + box_h - 36, 26)
        text_top = y + box_h - 48
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8)
        title_lines = wrap(c, title, "Helvetica-Bold", 8, box_w - 12)
        draw_lines(c, title_lines, bx + 6, text_top, "Helvetica-Bold", 8, 10, INK, 2)
        sub_top = text_top - 10 * min(len(title_lines), 2) - 2
        c.setFillColor(INK2)
        c.setFont("Helvetica", 7)
        sub_lines = wrap(c, sub, "Helvetica", 7, box_w - 12)
        draw_lines(c, sub_lines, bx + 6, sub_top, "Helvetica", 7, 9, INK2, 2)
        if i < n - 1:
            c.setStrokeColor(MINT)
            c.setFillColor(MINT)
            c.setLineWidth(2)
            ax0 = bx + box_w + 1
            ax1 = bx + box_w + gap - 1
            mid = y + box_h / 2
            c.line(ax0, mid, ax1 - 5, mid)
            c.line(ax1 - 9, mid + 4, ax1 - 3, mid)
            c.line(ax1 - 9, mid - 4, ax1 - 3, mid)


def build():
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("iEducar - Gestão Educacional em Rede")
    c.setSubject("Apresentação para a gestão municipal · pacote em rede")
    c.setAuthor("Buriti · LibreCode")
    c.setCreator("iEducar - Gestão Educacional em Rede")
    c.setKeywords("iEducar, gestão educacional, educação municipal, Buriti, LibreCode, Portábilis")

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
    for i, (ic, title, d) in enumerate(pillars):
        y = H - 170 - i * 80
        c.setFillColor(HexColor("#f4fffb"))
        c.setStrokeColor(MINT2)
        c.setLineWidth(1.2)
        c.roundRect(W * 0.48, y, W * 0.44, 68, 10, fill=1, stroke=1)
        icon(c, ic, W * 0.48 + 12, y + 16, 36)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(W * 0.48 + 56, y + 42, title)
        c.setFillColor(INK2)
        c.setFont("Helvetica", 9)
        draw_lines(
            c,
            wrap(c, d, "Helvetica", 9, W * 0.44 - 74),
            W * 0.48 + 56,
            y + 26,
            "Helvetica",
            9,
            11,
            INK2,
            2,
        )

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
        175,
        box_w=128,
        box_h=90,
        gap=14,
    )
    c.setFillColor(HexColor("#e8f6f2"))
    c.setStrokeColor(MINT)
    c.setLineWidth(1.2)
    c.roundRect(MARGIN, 55, W - 2 * MARGIN, 95, 10, fill=1, stroke=1)
    icon(c, "check", MARGIN + 18, 95, 34)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 64, 125, "Regra de ouro")
    c.setFillColor(INK2)
    c.setFont("Helvetica", 10)
    draw_lines(
        c,
        wrap(
            c,
            "Se o dado não está na matrícula, ele não entra no censo, no ônibus nem no painel. Corrigir na origem corrige o resto.",
            "Helvetica",
            10,
            W - 2 * MARGIN - 90,
        ),
        MARGIN + 64,
        105,
        "Helvetica",
        10,
        13,
        INK2,
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
    c.drawString(MARGIN, H - 82, "O que a cidade passa a operar junto")
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
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, H - 110, "Núcleo, microssistemas e módulos sob demanda — um só cadastro.")
    for i, (ic, title, d) in enumerate(mods):
        col, row = i % 4, i // 4
        x = MARGIN + col * 225
        y = H - 288 - row * 118
        c.setFillColor(HexColor("#ffffff"))
        c.setStrokeColor(LINE)
        c.setLineWidth(1)
        c.roundRect(x, y, 210, 102, 10, fill=1, stroke=1)
        icon(c, ic, x + 14, y + 64, 26)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x + 50, y + 74, title)
        c.setFillColor(INK2)
        c.setFont("Helvetica", 8.5)
        draw_lines(c, wrap(c, d, "Helvetica", 8.5, 180), x + 14, y + 48, "Helvetica", 8.5, 11, INK2, 3)
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
        55,
        box_w=200,
        box_h=88,
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
        55,
        box_w=200,
        box_h=88,
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
    for i, (n, title, d, ic) in enumerate(steps):
        y = H - 115 - i * 40
        c.setFillColor(MINT)
        c.circle(MARGIN + 16, y + 10, 12, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(MARGIN + 16, y + 6, n)
        if i < len(steps) - 1:
            c.setStrokeColor(LINE)
            c.setLineWidth(2)
            c.line(MARGIN + 16, y - 2, MARGIN + 16, y - 28)
        icon(c, ic, MARGIN + 40, y - 2, 24)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN + 74, y + 12, title)
        c.setFillColor(INK2)
        c.setFont("Helvetica", 9)
        c.drawString(MARGIN + 74, y - 2, d)

    # CTA box — clear of footer
    c.setFillColor(INK)
    c.roundRect(W - 340, 70, 300, 120, 12, fill=1, stroke=0)
    c.setFillColor(MINT2)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(W - 320, 165, "PRÓXIMO PASSO")
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 10)
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
        145,
        "Helvetica-Bold",
        10,
        13,
        white,
        4,
    )
    c.setFillColor(MINT2)
    c.setFont("Helvetica", 8)
    c.drawString(W - 320, 85, "buriti.dev.br/public/#contato")
    try:
        c.drawImage(ImageReader(str(IMG / "brand-mark.png")), MARGIN, 48, width=20, height=20, mask="auto")
        c.drawImage(ImageReader(str(IMG / "logo-buriti.png")), MARGIN + 28, 48, width=18, height=17, mask="auto")
        c.drawImage(ImageReader(str(IMG / "librecode.png")), MARGIN + 52, 50, width=40, height=15, mask="auto")
    except Exception:
        pass
    footer(c, 16)
    c.showPage()

    c.save()
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
