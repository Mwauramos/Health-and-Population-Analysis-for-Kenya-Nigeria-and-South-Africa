"""
PDF Report Generator — Africa Health Systems Comparative Dashboard
ZENIK.AI — Amos Mwaura
"""
import io
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, Table, TableStyle
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics import renderPDF

# ── Brand colours ──────────────────────────────────────────────────────────────
BG    = HexColor("#080c14")
BLUE  = HexColor("#2563eb")
CYAN  = HexColor("#06b6d4")
GREEN = HexColor("#22c55e")
MUTED = HexColor("#6b7fa3")
WHITE = white
LIGHT = HexColor("#f0f4ff")
SURF  = HexColor("#0d1320")

C_KENYA = HexColor("#2563eb")
C_NGA   = HexColor("#06b6d4")
C_SA    = HexColor("#22c55e")
COUNTRY_COLORS = {"Kenya": C_KENYA, "Nigeria": C_NGA, "South Africa": C_SA}

W, H = A4

# ── Styles ─────────────────────────────────────────────────────────────────────
def styles():
    return {
        "cover_title": ParagraphStyle("ct", fontName="Helvetica-Bold",
            fontSize=28, textColor=WHITE, leading=34, spaceAfter=12),
        "cover_sub": ParagraphStyle("cs", fontName="Helvetica",
            fontSize=13, textColor=MUTED, leading=18, spaceAfter=8),
        "cover_meta": ParagraphStyle("cm", fontName="Helvetica",
            fontSize=10, textColor=MUTED, leading=14),
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold",
            fontSize=16, textColor=BLUE, spaceBefore=18, spaceAfter=8),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold",
            fontSize=12, textColor=LIGHT, spaceBefore=12, spaceAfter=6),
        "body": ParagraphStyle("body", fontName="Helvetica",
            fontSize=9.5, textColor=HexColor("#c8d8f0"), leading=15, spaceAfter=6),
        "label": ParagraphStyle("lbl", fontName="Helvetica-Bold",
            fontSize=8, textColor=MUTED, leading=11,
            spaceBefore=4, spaceAfter=2, letterSpacing=1),
        "insight": ParagraphStyle("ins", fontName="Helvetica",
            fontSize=9, textColor=HexColor("#c8d8f0"), leading=14,
            leftIndent=10, spaceAfter=8),
        "footer": ParagraphStyle("ftr", fontName="Helvetica",
            fontSize=8, textColor=MUTED, alignment=1),
    }

# ── Page callbacks ─────────────────────────────────────────────────────────────
def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#0d1320"))
    canvas.rect(0, H * 0.38, W, H * 0.62, fill=1, stroke=0)
    # accent bar
    canvas.setFillColor(BLUE)
    canvas.rect(0, H * 0.38 - 3, W, 3, fill=1, stroke=0)
    # footer
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(W / 2, 28, "ZENIK.AI  ·  Amos Mwaura  ·  mwauramos.n@gmail.com")
    canvas.restoreState()

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, H - 44, W, 44, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.rect(0, H - 44, W, 2, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(40, H - 28, "AFRICA HEALTH SYSTEMS ANALYSIS")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(W - 40, H - 28, f"Page {doc.page}")
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W, 32, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(W / 2, 10, "ZENIK.AI  ·  Amos Mwaura  ·  Healthcare AI Portfolio")
    canvas.restoreState()

# ── Bar chart drawing ──────────────────────────────────────────────────────────
def bar_chart(data, title, width=460, height=110, unit=""):
    """data: list of (label, value, color)"""
    d = Drawing(width, height + 30)
    d.add(Rect(0, 0, width, height + 30, fillColor=SURF,
               strokeColor=HexColor("#1e2d45"), strokeWidth=0.5))
    d.add(String(width / 2, height + 16, title, fontSize=9,
                 fontName="Helvetica-Bold", fillColor=WHITE, textAnchor="middle"))
    max_val = max(v for _, v, _ in data) or 1
    bar_w = (width - 60) / len(data) * 0.6
    gap   = (width - 60) / len(data)
    for i, (label, val, color) in enumerate(data):
        x = 30 + i * gap + gap * 0.2
        bh = (val / max_val) * (height - 30)
        d.add(Rect(x, 20, bar_w, bh, fillColor=HexColor(color),
                   strokeWidth=0))
        d.add(String(x + bar_w / 2, 20 + bh + 3,
                     f"{val:,.0f}{unit}", fontSize=7,
                     fontName="Helvetica-Bold", fillColor=WHITE, textAnchor="middle"))
        d.add(String(x + bar_w / 2, 6, label, fontSize=7.5,
                     fontName="Helvetica", fillColor=MUTED, textAnchor="middle"))
    return d

# ── KPI table ──────────────────────────────────────────────────────────────────
def kpi_table(rows, s):
    header = ["Indicator", "Kenya", "Nigeria", "South Africa"]
    data   = [header] + rows
    col_w  = [200, 90, 90, 110]
    tbl = Table(data, colWidths=col_w)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  BLUE),
        ("TEXTCOLOR",   (0,0), (-1,0),  WHITE),
        ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,0),  8),
        ("BACKGROUND",  (0,1), (-1,-1), SURF),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[SURF, HexColor("#0f1e35")]),
        ("TEXTCOLOR",   (0,1), (-1,-1), LIGHT),
        ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,1), (-1,-1), 8.5),
        ("ALIGN",       (1,0), (-1,-1), "CENTER"),
        ("GRID",        (0,0), (-1,-1), 0.4, HexColor("#1e2d45")),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    return tbl

# ── Main report function ───────────────────────────────────────────────────────
def generate_report(snapshot_df, ts_df):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm)

    s = styles()
    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    from reportlab.platypus import FrameBreak
    story.append(Spacer(1, 3.5*cm))
    story.append(Paragraph("Africa Health Systems", s["cover_title"]))
    story.append(Paragraph("Comparative Analysis", s["cover_title"]))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "Kenya · Nigeria · South Africa · 2010 to 2024", s["cover_sub"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "World Bank Health Nutrition and Population Statistics (calibrated synthetic data)", s["cover_meta"]))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("ZENIK.AI · Amos Mwaura · 2024", s["cover_meta"]))
    story.append(PageBreak())

    # ── Section 1: Overview KPIs ───────────────────────────────────────────────
    story.append(Paragraph("1. Country Overview", s["h1"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#1e2d45"), spaceAfter=10))
    kpi_rows = [
        ["Population (million)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','population_m'].values[0]:.1f}",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','population_m'].values[0]:.1f}",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','population_m'].values[0]:.1f}"],
        ["GDP per capita (USD)",
         f"${snapshot_df.loc[snapshot_df.country=='Kenya','gdp_per_capita'].values[0]:,.0f}",
         f"${snapshot_df.loc[snapshot_df.country=='Nigeria','gdp_per_capita'].values[0]:,.0f}",
         f"${snapshot_df.loc[snapshot_df.country=='South Africa','gdp_per_capita'].values[0]:,.0f}"],
        ["Health spend (% of GDP)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','health_spend_pct_gdp'].values[0]:.1f}%",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','health_spend_pct_gdp'].values[0]:.1f}%",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','health_spend_pct_gdp'].values[0]:.1f}%"],
        ["Health spend per capita (USD)",
         f"${snapshot_df.loc[snapshot_df.country=='Kenya','health_spend_per_cap'].values[0]:,.0f}",
         f"${snapshot_df.loc[snapshot_df.country=='Nigeria','health_spend_per_cap'].values[0]:,.0f}",
         f"${snapshot_df.loc[snapshot_df.country=='South Africa','health_spend_per_cap'].values[0]:,.0f}"],
        ["Out-of-pocket (% of health spend)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','oop_pct_health'].values[0]:.1f}%",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','oop_pct_health'].values[0]:.1f}%",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','oop_pct_health'].values[0]:.1f}%"],
        ["UHC Service Coverage Index",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','uhc_index'].values[0]:.0f}",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','uhc_index'].values[0]:.0f}",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','uhc_index'].values[0]:.0f}"],
    ]
    story.append(kpi_table(kpi_rows, s))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "South Africa leads in absolute health spending at $563 per capita, nearly 6x Kenya ($88) "
        "and 7x Nigeria ($74). Nigeria's out-of-pocket burden of 69% is among the highest globally, "
        "indicating catastrophic health expenditure risk for households.", s["body"]))

    # ── Section 2: Health Spending ─────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("2. Health Spending Trends (2010 to 2024)", s["h1"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#1e2d45"), spaceAfter=10))

    spend_data = [
        ("Kenya",        88,  "#2563eb"),
        ("Nigeria",      74,  "#06b6d4"),
        ("South Africa", 563, "#22c55e"),
    ]
    story.append(bar_chart(spend_data, "Health Expenditure per Capita (USD, 2023)", unit=""))
    story.append(Spacer(1, 0.3*cm))

    oop_data = [
        ("Kenya",        24.3, "#2563eb"),
        ("Nigeria",      69.2, "#06b6d4"),
        ("South Africa", 7.2,  "#22c55e"),
    ]
    story.append(bar_chart(oop_data, "Out-of-Pocket as % of Health Expenditure (2023)", unit="%"))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Nigeria's dependency on out-of-pocket payments (69%) exposes households to catastrophic "
        "health expenditure. South Africa's social health financing model keeps OOP to 7%, while "
        "Kenya's ongoing UHC reforms have reduced OOP from 32% (2010) to 24% (2023).", s["body"]))

    # ── Section 3: Health Outcomes ─────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("3. Health Outcomes", s["h1"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#1e2d45"), spaceAfter=10))

    outcome_rows = [
        ["Life expectancy (years)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','life_expectancy'].values[0]:.1f}",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','life_expectancy'].values[0]:.1f}",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','life_expectancy'].values[0]:.1f}"],
        ["Under-5 mortality (per 1,000 births)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','u5_mortality'].values[0]:.0f}",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','u5_mortality'].values[0]:.0f}",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','u5_mortality'].values[0]:.0f}"],
        ["Maternal mortality (per 100,000)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','maternal_mortality'].values[0]:,.0f}",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','maternal_mortality'].values[0]:,.0f}",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','maternal_mortality'].values[0]:,.0f}"],
        ["DTP3 immunisation coverage (%)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','immunisation_dtp3'].values[0]:.0f}%",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','immunisation_dtp3'].values[0]:.0f}%",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','immunisation_dtp3'].values[0]:.0f}%"],
        ["HIV prevalence (%)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','hiv_prevalence'].values[0]:.1f}%",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','hiv_prevalence'].values[0]:.1f}%",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','hiv_prevalence'].values[0]:.1f}%"],
        ["TB incidence (per 100,000)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','tb_incidence'].values[0]:.0f}",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','tb_incidence'].values[0]:.0f}",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','tb_incidence'].values[0]:.0f}"],
    ]
    story.append(kpi_table(outcome_rows, s))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "Nigeria's under-5 mortality of 116 per 1,000 live births is nearly 4x South Africa (31) "
        "and 3x Kenya (39), reflecting chronic underinvestment in primary healthcare. "
        "South Africa's high HIV prevalence (18.3%) suppresses life expectancy despite its "
        "higher health expenditure. Kenya shows the strongest improvement trajectory across "
        "maternal and child health indicators over the 2010 to 2024 period.", s["body"]))

    # ── Section 4: System Capacity ─────────────────────────────────────────────
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("4. Health System Capacity", s["h1"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#1e2d45"), spaceAfter=10))

    capacity_rows = [
        ["Hospital beds (per 1,000)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','beds_per_1000'].values[0]:.1f}",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','beds_per_1000'].values[0]:.1f}",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','beds_per_1000'].values[0]:.1f}"],
        ["Doctors (per 1,000)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','doctors_per_1000'].values[0]:.2f}",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','doctors_per_1000'].values[0]:.2f}",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','doctors_per_1000'].values[0]:.2f}"],
        ["Nurses (per 1,000)",
         f"{snapshot_df.loc[snapshot_df.country=='Kenya','nurses_per_1000'].values[0]:.2f}",
         f"{snapshot_df.loc[snapshot_df.country=='Nigeria','nurses_per_1000'].values[0]:.2f}",
         f"{snapshot_df.loc[snapshot_df.country=='South Africa','nurses_per_1000'].values[0]:.2f}"],
        ["WHO min. beds threshold", "2.5", "2.5", "2.5"],
        ["WHO min. doctors threshold", "1.0", "1.0", "1.0"],
    ]
    story.append(kpi_table(capacity_rows, s))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "All three countries fall below the WHO minimum of 2.5 hospital beds per 1,000 population. "
        "Kenya (1.4) and Nigeria (0.5) face the steepest capacity gaps. Doctor density across all "
        "three countries remains well below the WHO threshold of 1.0 per 1,000, with Kenya at 0.16, "
        "posing structural constraints on healthcare access and quality.", s["body"]))

    # ── Section 5: Policy Recommendations ─────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("5. Key Findings and Policy Recommendations", s["h1"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#1e2d45"), spaceAfter=10))

    findings = [
        ("Nigeria", "Critical OOP reform needed",
         "At 69% out-of-pocket burden, Nigeria needs urgently structured social health insurance "
         "expansion. The National Health Insurance Authority (NHIA) Act (2022) is a positive step "
         "but implementation at state level remains uneven."),
        ("Kenya", "UHC reform momentum",
         "Kenya's Social Health Authority (SHA) launched in 2023 replaces NHIF with a mandate to "
         "eliminate out-of-pocket payments. Early indicators show improving UHC coverage index from "
         "43 (2010) to 58 (2023). Sustaining this requires county-level health financing equity."),
        ("South Africa", "HIV and TB co-epidemic burden",
         "Despite the highest health spend per capita, South Africa carries a disproportionate "
         "HIV/TB co-epidemic burden. ART coverage has improved life expectancy from 57.0 (2010) "
         "to 64.9 (2023), but TB incidence (468/100k) remains among the highest globally."),
        ("All Three", "Workforce gap is the binding constraint",
         "With doctor density at 0.16 to 0.91 per 1,000 against a WHO minimum of 1.0, all three "
         "countries face structural health workforce shortages that limit the impact of financing "
         "reforms. Task-shifting, community health worker scale-up, and digital health tools "
         "are priority levers."),
    ]

    for country, title, text in findings:
        col = {"Kenya": "#2563eb", "Nigeria": "#06b6d4",
               "South Africa": "#22c55e", "All Three": "#6b7fa3"}[country]
        story.append(Paragraph(
            f'<font color="{col}"><b>{country}</b></font> — {title}', s["h2"]))
        story.append(Paragraph(text, s["insight"]))
        story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#1e2d45"), spaceAfter=8))
    story.append(Paragraph(
        "Data: World Bank Health Nutrition and Population Statistics (calibrated synthetic data, 2010 to 2024). "
        "Report generated by ZENIK.AI — Amos Mwaura.", s["footer"]))

    # ── Build ──────────────────────────────────────────────────────────────────
    from reportlab.platypus import PageTemplate, Frame
    cover_frame = Frame(0, 0, W, H, leftPadding=2.2*cm, rightPadding=2.2*cm,
                        topPadding=1.5*cm, bottomPadding=1.5*cm)
    body_frame  = Frame(0, 32, W, H - 32 - 44,
                        leftPadding=2.2*cm, rightPadding=2.2*cm,
                        topPadding=0.5*cm, bottomPadding=0.5*cm)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover),
        PageTemplate(id="body",  frames=[body_frame],  onPage=on_page),
    ])
    from reportlab.platypus import NextPageTemplate
    story.insert(0, NextPageTemplate("cover"))
    # find PageBreak after cover and insert template switch
    for i, el in enumerate(story):
        if isinstance(el, PageBreak) and i > 0:
            story.insert(i + 1, NextPageTemplate("body"))
            break

    doc.build(story)
    return buf.getvalue()
