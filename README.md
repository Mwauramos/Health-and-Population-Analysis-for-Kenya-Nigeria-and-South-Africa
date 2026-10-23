# Africa Health Systems Comparative Analysis

**ZENIK.AI · Amos Mwaura**

A multi-tab Streamlit dashboard comparing health spending, outcomes, and system capacity across **Kenya, Nigeria, and South Africa** (2010–2024), with a downloadable PDF report. Rebuilt from a prior R-based comparative analysis as a fully interactive Python dashboard.

---

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://africa-health-systems.streamlit.app)

> App may take 30 seconds to wake up on first load (Streamlit Community Cloud free tier).

---

## Overview

| Tab | What it shows |
|-----|---------------|
| 💰 **Health Spending** | Per-capita spend trends, % of GDP, out-of-pocket burden vs WHO targets |
| ❤️ **Health Outcomes** | Life expectancy, under-5 mortality, maternal mortality, DTP3 immunisation |
| ⚕️ **System Capacity** | WHO-threshold gauges (beds/doctors/nurses), radar chart, UHC index trends |
| 🌐 **Country Profiles** | Side-by-side 15-indicator snapshot table for all three countries |
| 📄 **Download Report** | One-click PDF export — financing, outcomes, capacity, policy recommendations |

---

## Tech Stack

- **Streamlit** — multi-tab dashboard framework
- **Plotly** — interactive charts (line, bar, gauge, radar/polar, scatter)
- **ReportLab** — programmatic PDF generation (ZENIK.AI brand palette)
- **Pandas / NumPy** — data simulation and transformation

---

## Data

All figures are sourced live from the **World Bank Health Nutrition and Population Statistics API** via `wbgapi`. 15 indicators are pulled for Kenya, Nigeria, and South Africa covering 2010 to 2024. Missing years (common for workforce density indicators) are filled by linear interpolation. The app caches data for 24 hours so it loads fast after the first visit.

| Indicator | World Bank code |
|-----------|----------------|
| Health expenditure per capita | SH.XPD.CHEX.PC.CD |
| Health expenditure % of GDP | SH.XPD.CHEX.GD.ZS |
| Out-of-pocket % of health spend | SH.XPD.OOPC.CH.ZS |
| Life expectancy at birth | SP.DYN.LE00.IN |
| Under-5 mortality rate | SH.DYN.MORT |
| Maternal mortality ratio | SH.STA.MMRT |
| DTP3 immunisation coverage | SH.IMM.IDPT |
| Hospital beds per 1,000 | SH.MED.BEDS.ZS |
| Physicians per 1,000 | SH.MED.PHYS.ZS |
| Nurses and midwives per 1,000 | SH.MED.NUMW.P3 |
| HIV prevalence | SH.DYN.AIDS.ZS |
| TB incidence per 100,000 | SH.TBS.INCD |
| UHC service coverage index | SH.UHC.SRVS.CV.XD |

---

## Run Locally

```bash
git clone https://github.com/Mwauramos/Health-and-Population-Analysis-for-Kenya-Nigeria-and-South-Africa.git
cd Health-and-Population-Analysis-for-Kenya-Nigeria-and-South-Africa
pip install -r requirements.txt
streamlit run app.py
```

---

## Key Findings

- **Nigeria's OOP burden (69%)** exceeds the WHO catastrophic threshold by 4.6×, concentrated in the poorest quintile — health financing reform is the single highest-leverage intervention.
- **South Africa's life expectancy** rose from 57.0 to 64.9 years (2010–2023) almost entirely due to ART programme scale-up, not income growth — a model for the continent.
- All three countries fall **below the WHO minimum of 2.5 hospital beds per 1,000** population; Nigeria at 0.5 beds per 1,000 faces the most acute infrastructure deficit.
- **Kenya's UHC trajectory** (43 → 58, 2010–2023) reflects successful NHIF expansion and declining OOP share — the most sustainable financing path of the three.

---

## Related Portfolio Projects

This platform is part of the [ZENIK.AI Healthcare AI Portfolio](https://mwauramos.github.io/zenik-ai):

- **Kenya County Health Analytics Platform** — 47-county disease burden and health system dashboard
- **Outbreak Surveillance Agent** — LangGraph multi-agent epidemic alerting system
- **Malaria-TB Dual Classifier** — XGBoost + SHAP clinical decision support

---

## Author

**Amos Mwaura** — Machine Learning Engineer · Nairobi, Kenya  
[mwauramos.github.io/zenik-ai](https://mwauramos.github.io/zenik-ai) · [mwauramos.n@gmail.com](mailto:mwauramos.n@gmail.com)
