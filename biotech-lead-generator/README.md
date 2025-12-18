# 🧬 Biotech Lead Generation System

**AI-Powered Lead Scoring for 3D In-Vitro Models**

A comprehensive web application that identifies, enriches, and ranks potential leads in the biotech/pharma space who are likely to adopt 3D in-vitro models for drug discovery and toxicology research.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Overview

This system helps business developers identify high-value prospects by:

1. **Identifying** leads from LinkedIn, PubMed, and conference databases
2. **Enriching** data with contact information and company details
3. **Scoring** leads using a weighted propensity algorithm (0-100)
4. **Prioritizing** prospects based on likelihood to purchase

### Key Features

- ✅ **PubMed Integration**: Find researchers publishing on relevant topics
- ✅ **Intelligent Scoring**: Weighted algorithm considering role, publications, funding, location
- ✅ **Interactive Dashboard**: Real-time filtering, search, and visualization
- ✅ **Data Export**: CSV, Excel with formatted reports
- ✅ **Configurable Weights**: Adjust scoring criteria on the fly
- ✅ **Database Persistence**: SQLite for local data storage

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip or conda
- Git

### Installation (5 minutes)

```bash
# 1. Clone repository (or create directory structure)
mkdir biotech-lead-generator
cd biotech-lead-generator

# 2. Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install streamlit pandas numpy beautifulsoup4 requests biopython sqlalchemy openpyxl xlsxwriter python-dotenv pydantic plotly

# 4. Create .env file (optional for APIs)
cat > .env << EOL
PUBMED_EMAIL=your.email@example.com
PUBMED_API_KEY=optional
EOL

# 5. Run the application
streamlit run app.py
```

Visit `http://localhost:8501` in your browser!

---

## 📁 Project Structure

```
biotech-lead-generator/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── .gitignore
├── README.md
│
├── src/
│   ├── data_sources/
│   │   ├── pubmed_scraper.py      # PubMed API integration
│   │   ├── linkedin_mock.py       # Mock LinkedIn data
│   │   └── conference_scraper.py   # Conference data
│   │
│   ├── enrichment/
│   │   ├── email_finder.py        # Email enrichment
│   │   └── company_enricher.py    # Company data
│   │
│   ├── scoring/
│   │   └── propensity_scorer.py   # Lead scoring engine
│   │
│   ├── database/
│   │   └── db_manager.py          # SQLite manager
│   │
│   └── utils/
│       ├── export_helper.py       # Export utilities
│       └── data_validator.py      # Data validation
│
└── data/
    ├── raw/                       # Raw scraped data
    ├── processed/                 # Processed data
    └── sample/                    # Demo data
```

---

## 🎨 Usage Guide

### 1. Load Sample Data

Click "Load Sample Data" to start with demo data (10 pre-scored leads).

### 2. Search PubMed for New Leads

1. Navigate to **Dashboard** tab
2. Select "PubMed Search" from sidebar
3. Enter query: `drug-induced liver injury 3D models`
4. Click "Search PubMed"
5. System will find researchers and calculate scores automatically

### 3. Adjust Scoring Weights

In the sidebar:
- **Role Fit** (default: 30 points): Job title relevance
- **Recent Publication** (default: 40 points): Published in last 2 years
- **Company Funding** (default: 20 points): Series A/B/C funding
- **Strategic Location** (default: 10 points): Boston, Bay Area, Basel, etc.

Click "Apply Weights" to recalculate scores.

### 4. Filter and Search

Navigate to **Search & Filter** tab:
- Search by name, title, or company
- Filter by minimum score
- Filter by location
- Export filtered results

### 5. Export Data

Sidebar > Export section:
- **CSV**: Plain text export
- **Excel**: Formatted with color-coded scores

---

## 🧮 Scoring Algorithm

### Propensity Score Calculation (0-100)

```python
Score = Role_Fit + Publication + Funding + Location

Default Weights:
- Role Fit: 30 points
- Publication: 40 points  
- Funding: 20 points
- Location: 10 points
```

### Scoring Logic

#### 1. Role Fit (30 points max)

- **Full Score**: Title contains "toxicology", "safety", "hepatic"
- **80%**: Title contains "3D", "in vitro"
- **60%**: Other relevant keywords
- **+20% Bonus**: Senior roles (Director, VP, Head)

#### 2. Recent Publication (40 points max)

- **Full Score**: Published in last 2 years on DILI/3D models
- **80%**: Recent but less relevant publication
- **50%**: Older publication (3-5 years)
- **10%**: No recent publication (baseline)

#### 3. Company Funding (20 points max)

- **Full Score**: Series A/B/C (prime buying stage)
- **80%**: Public/IPO (established)
- **40%**: Seed/Early stage
- **20%**: Unknown

#### 4. Strategic Location (10 points max)

- **Full Score**: Major hubs (Cambridge MA, Boston, Bay Area, Basel)
- **60%**: Secondary hubs
- **20%**: Other locations

### Priority Tiers

- 🟢 **High Priority (70-100)**: Immediate outreach
- 🟡 **Medium Priority (50-69)**: Qualified leads
- 🔴 **Low Priority (0-49)**: Nurture campaign

### Example Scores

| Lead Profile | Role | Pub | Fund | Loc | **Total** |
|-------------|------|-----|------|-----|-----------|
| Director of Tox @ Series B biotech in Cambridge, recent DILI paper | 36 | 40 | 20 | 10 | **95** 🟢 |
| Senior Scientist @ Public pharma in Boston, older paper | 24 | 20 | 16 | 10 | **70** 🟢 |
| Research Scientist @ Startup in Texas, no publications | 18 | 4 | 8 | 2 | **32** 🔴 |

---

## 🔌 API Integration

### PubMed (Built-in, Free)

```python
from src.data_sources.pubmed_scraper import PubMedScraper

scraper = PubMedScraper(email="your.email@example.com")
leads = scraper.search_authors(
    query="drug-induced liver injury 3D models",
    max_results=50
)
```

### Optional APIs (Paid)

#### Hunter.io (Email Finding)
```bash
# .env
HUNTER_API_KEY=your_key
```
- Free tier: 25 searches/month
- Paid: $49/month for 500 searches

#### Proxycurl (LinkedIn Data)
```bash
# .env
PROXYCURL_API_KEY=your_key
```
- 100 free credits on signup
- Then $99/month for regular use

---

## 📊 Data Sources

### Current Implementation

| Source | Status | Cost | Coverage |
|--------|--------|------|----------|
| PubMed | ✅ Implemented | Free | Researchers, academic institutions |
| Sample Data | ✅ Included | Free | Demo purposes |
| Manual Entry | ✅ Implemented | Free | Custom leads |

### Future Integration

| Source | Use Case | Estimated Effort |
|--------|----------|------------------|
| LinkedIn API | Job titles, locations | 2-3 days |
| Crunchbase | Funding data | 1-2 days |
| Conference Sites | SOT, AACR attendees | 3-4 days |
| Hunter.io | Email enrichment | 1 day |
| Clearbit | Company data | 1 day |

---

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Easiest, Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy automatically

**Limitations**: 1GB RAM, 1 CPU, public access

### Option 2: Railway.app (Recommended for Demo)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Cost**: ~$5/month, custom domain, 512MB RAM

### Option 3: Docker (Production)

```bash
# Build image
docker build -t biotech-lead-gen .

# Run container
docker run -p 8501:8501 biotech-lead-gen

# Or use docker-compose
docker-compose up -d
```

### Option 4: AWS/GCP (Enterprise)

**AWS Elastic Beanstalk**:
```bash
eb init
eb create biotech-lead-gen
eb deploy
```

**Google Cloud Run**:
```bash
gcloud run deploy biotech-lead-gen \
  --source . \
  --platform managed \
  --region us-central1
```

**Cost**: ~$20-50/month depending on usage

---

## 🧪 Testing

### Run Unit Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Test Scoring Algorithm

```python
from src.scoring.propensity_scorer import PropensityScorer
import pandas as pd

# Test lead
lead = pd.Series({
    'title': 'Director of Toxicology',
    'recent_publication': True,
    'publication_year': 2024,
    'company_funding': 'Series B',
    'location': 'Cambridge, MA'
})

scorer = PropensityScorer()
score = scorer.calculate_score(lead)
print(f"Score: {score}/100")
```

---

## 🔐 Security & Compliance

### Data Privacy

- ✅ Local SQLite database (no cloud storage by default)
- ✅ Environment variables for API keys
- ✅ No plaintext password storage
- ⚠️ GDPR: Add consent mechanism for EU contacts
- ⚠️ CCPA: Add opt-out for California contacts

### Best Practices

1. **Never commit** `.env` file
2. **Use HTTPS** in production
3. **Rotate API keys** regularly
4. **Audit exports** for compliance
5. **Respect rate limits** on APIs

---

## 🛠️ Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'streamlit'`
```bash
# Solution: Ensure venv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

**Issue**: PubMed search returns no results
```bash
# Solution: Check internet connection and query
# Try broader terms: "liver toxicity" instead of "DILI 3D models NAMs"
```

**Issue**: Score calculation errors
```bash
# Solution: Ensure all required columns exist
# Check sample_leads.csv for correct format
```

**Issue**: Port 8501 already in use
```bash
# Solution: Use different port
streamlit run app.py --server.port=8502
```

---

## 📈 Roadmap

### Phase 1: Demo (Current) ✅
- [x] Core scoring algorithm
- [x] PubMed integration
- [x] Streamlit dashboard
- [x] CSV/Excel export

### Phase 2: MVP (Next 1-2 months)
- [ ] LinkedIn API integration (Proxycurl)
- [ ] Email enrichment (Hunter.io)
- [ ] Automated data pipelines (Airflow)
- [ ] PostgreSQL database
- [ ] User authentication

### Phase 3: Production (3-6 months)
- [ ] Multi-tenant architecture
- [ ] CRM integrations (Salesforce, HubSpot)
- [ ] Advanced AI scoring (GPT-4 for company analysis)
- [ ] Conference attendee scraping
- [ ] Funding database integration

### Phase 4: Enterprise (6-12 months)
- [ ] Chrome extension
- [ ] Mobile app
- [ ] Real-time alerts
- [ ] Predictive analytics
- [ ] White-label solution

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🎓 Acknowledgments

- **PubMed/NCBI**: For providing free access to biomedical literature
- **Streamlit**: For the awesome app framework
- **Biopython**: For PubMed API client

---

## 📚 Additional Resources

### Documentation
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [Streamlit Docs](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Related Tools
- [Clay.com](https://clay.com) - Commercial alternative
- [Apollo.io](https://apollo.io) - Sales intelligence
- [ZoomInfo](https://zoominfo.com) - B2B database

---

## ⚡ Performance Tips

1. **Cache PubMed results** to avoid re-fetching
2. **Batch process** large datasets
3. **Use indexes** on database columns
4. **Enable Streamlit caching** for expensive operations
5. **Optimize queries** with proper SQL indexes

---