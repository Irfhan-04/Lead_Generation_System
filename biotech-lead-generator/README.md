# 🧬 Biotech Lead Generation System

AI-powered lead scoring for 3D in-vitro models in drug discovery.

## 🎯 Overview

This system identifies, enriches, and scores potential leads in biotech/pharma who are likely to adopt 3D in-vitro models for toxicology research.

### Key Features

- ✅ Intelligent propensity scoring (0-100)
- ✅ PubMed API integration (finds researchers from publications)
- ✅ Configurable scoring weights
- ✅ Interactive dashboard with filters
- ✅ CSV/Excel export

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/biotech-lead-generator.git
cd biotech-lead-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python scripts/generate_leads.py 200

# Run application
streamlit run app.py
```

Visit `http://localhost:8501`

## 📊 Output Data

See example output: [Google Sheets Link]

200 scored leads with:
- Propensity scores (0-100)
- Rankings
- Contact information
- Publication data
- Funding stages

## 🧮 Scoring Algorithm

**Weighted Scoring (0-100 points):**

- **Role Fit (30%)**: Job title relevance
- **Recent Publication (40%)**: Published in last 2 years
- **Company Funding (20%)**: Series A/B/C or Public
- **Strategic Location (10%)**: Biotech hubs

**Priority Tiers:**
- 🟢 High (70-100): Immediate outreach
- 🟡 Medium (50-69): Qualified leads
- 🔴 Low (0-49): Nurture campaign

## 📁 Project Structure

biotech-lead-generator/
├── app.py                      # Main Streamlit app
├── config.py                   # Configuration
├── requirements.txt
├── src/
│   ├── scoring/
│   │   └── propensity_scorer.py
│   ├── data_sources/
│   │   └── pubmed_scraper.py
│   └── utils/
│       └── export_helper.py
└── data/
└── sample/
└── sample_leads.csv

## 🔌 Data Sources

**Implemented:**
- ✅ PubMed (NCBI E-utilities API)
- ✅ Sample data generator

**Future Integration:**
- LinkedIn API (Proxycurl)
- Email enrichment (Hunter.io)
- Conference attendee lists

## 🧪 Testing
```bash
# Generate test data
python scripts/generate_leads.py 50

# Run application
streamlit run app.py
```

## 📄 License

MIT License