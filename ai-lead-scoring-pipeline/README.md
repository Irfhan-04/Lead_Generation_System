# AI Lead Scoring Pipeline for Biotech / Pharma

This project implements a reproducible, explainable lead generation and
propensity scoring pipeline for identifying biotech/pharma professionals
most likely to engage with advanced 3D in-vitro models for preclinical
safety and toxicology.

The system mirrors how a business development analyst would:
- Identify relevant decision-makers
- Enrich them with scientific and business context
- Rank them based on likelihood to engage

---

## Problem Statement

Biotech and pharma companies evaluating 3D in-vitro models require
targeted outreach to scientists and decision-makers who:
- Work in toxicology / safety assessment
- Are actively publishing relevant research
- Belong to organizations with budget and readiness to adopt new methods

This project builds a data pipeline that automates this process in a
transparent and reproducible way.

---

## System Overview

Data Sources:
- Public scientific data (PubMed)
- Public / sample professional data (titles, companies, locations)

Pipeline:
1. Load structured lead data
2. Normalize and enrich leads
3. Apply deterministic business rules
4. Augment scientific intent using AI
5. Generate ranked outputs
6. Export results to Google Sheets (primary artifact)

---

## Scoring Logic (Explainable)

Each lead is scored on a 0–100 scale using weighted signals:

- Role Fit (0–30)
- Scientific Intent – deterministic + AI (0–40)
- Company Funding Readiness (0–20)
- Location Signal (0–10)

AI is used only to **interpret scientific relevance** of publications.
Final scores remain deterministic and auditable.

---

## Outputs

Primary Output:
- Google Sheet (generated programmatically)
- Contains ranked leads, scores, and score breakdowns

Secondary Outputs:
- CSV file (`data/output/scored_leads.csv`)
- Optional Streamlit inspection app

Streamlit Output:
( https://leadgenerationsystem-hs2rvre3kc24rtgsburbea.streamlit.app/ )

---

## How to Run Locally

```bash
pip install -r requirements.txt
python main.py
