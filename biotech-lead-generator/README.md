# 🧬 Biotech Lead Generation System

**AI-Powered Lead Scoring for 3D In-Vitro Models in Drug Discovery**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A comprehensive web application that identifies, enriches, and ranks potential leads in the biotech/pharma space who are likely to adopt 3D in-vitro models for toxicology research and drug discovery.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Demo](#-demo)
- [Features](#-features)
- [Scoring Algorithm](#-scoring-algorithm)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Data Sources](#-data-sources)
- [Deployment](#-deployment)
- [Examples](#-examples)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

This system automates the lead generation process for businesses selling 3D in-vitro models and related technologies to biotech and pharmaceutical companies. It combines data from multiple sources, applies intelligent scoring, and presents actionable insights through an interactive dashboard.

### The Problem

Business development teams spend weeks manually:
- Searching for potential leads on LinkedIn and publications
- Gathering contact information and company details
- Prioritizing prospects based on gut feeling
- Managing spreadsheets of unstructured data

### The Solution

This automated system:
- **Identifies** leads from PubMed publications, LinkedIn, and conferences
- **Enriches** data with contact info, funding status, and publications
- **Scores** each lead (0-100) based on propensity to purchase
- **Prioritizes** prospects automatically for maximum ROI

**Result:** Weeks of manual work reduced to minutes with data-driven prioritization.

---

## 🚀 Demo

### Live Application
🔗 **Streamlit App**: [https://YOUR-APP.streamlit.app]([https://YOUR-APP.streamlit.app](https://leadgenerationsystem-vkyz4vssnk4mmwdm7tytr9.streamlit.app)

### Output Data
📊 **Google Sheets**: [View 200+ Scored Leads]([https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID](https://docs.google.com/spreadsheets/d/1MhaO7-NPyqkllQpHvSa8ZMYYumBmvFwLUIyolrtvusQ/edit?usp=sharing)

### Repository
💻 **GitHub**: [https://github.com/YOUR_USERNAME/biotech-lead-generator]([https://github.com/YOUR_USERNAME/biotech-lead-generator](https://github.com/Irfhan-04/Lead_Generation_System.git)

---

## ✨ Features

### Core Functionality

- ✅ **Intelligent Propensity Scoring** - Weighted algorithm (0-100) considering role, publications, funding, location
- ✅ **PubMed Integration** - Finds researchers from recent relevant publications via official NCBI API
- ✅ **Configurable Weights** - Adjust scoring criteria in real-time
- ✅ **Interactive Dashboard** - Search, filter, and explore leads with modern UI
- ✅ **Multiple Export Formats** - CSV, Excel with conditional formatting, Google Sheets ready
- ✅ **Database Persistence** - SQLite for local storage with search capabilities
- ✅ **Sample Data Generator** - Create realistic test datasets

### User Experience

- 🎨 Clean, intuitive Streamlit interface
- 🔍 Advanced search and filtering
- 📊 Visual score distribution charts
- 🎯 Priority tier classification (High/Medium/Low)
- 📈 Real-time statistics and metrics
- 🔄 Instant score recalculation

---

## 🧮 Scoring Algorithm

### Propensity Score Calculation

Each lead receives a score from **0-100** based on four weighted factors:

```
Total Score = Role Fit (30%) + Recent Publication (40%) + Funding (20%) + Location (10%)
```

### Detailed Breakdown

#### 1. Role Fit (30 points max)

**What we measure:**
- Job title contains toxicology/safety keywords
- Seniority level (Director, VP, Head)
- Relevance to 3D models and in-vitro research

**Scoring:**
- **Full Score (30 pts)**: "Director of Toxicology", "Head of Safety Assessment"
- **High Score (24 pts)**: "Principal Scientist - Hepatic", "VP Preclinical Safety"
- **Medium Score (18 pts)**: "Senior Scientist", "Research Associate"
- **Low Score (6 pts)**: "Research Scientist II", "Scientist I"

**Bonus:** +20% for senior roles (Director, VP, Head, Chief)

#### 2. Recent Publication (40 points max)

**What we measure:**
- Published papers in last 2 years
- Relevance to DILI, 3D models, toxicology
- Authorship position (corresponding author = budget holder)

**Scoring:**
- **Full Score (40 pts)**: Published 2023-2024 on DILI/3D models
- **High Score (32 pts)**: Published 2023-2024, less relevant topic
- **Medium Score (20 pts)**: Published 2020-2022
- **Low Score (4 pts)**: No recent publication

#### 3. Company Funding (20 points max)

**What we measure:**
- Funding stage indicates budget availability
- Series A/B/C companies are prime buyers
- Public companies have established budgets

**Scoring:**
- **Full Score (20 pts)**: Series A, B, or C funding
- **High Score (16 pts)**: Public/IPO (established budgets)
- **Medium Score (8 pts)**: Seed/Early stage
- **Low Score (4 pts)**: Unknown funding

#### 4. Strategic Location (10 points max)

**What we measure:**
- Proximity to biotech hubs enables in-person meetings
- Major hubs have dense networks and ecosystem

**Scoring:**
- **Full Score (10 pts)**: Cambridge MA, Boston, Bay Area, Basel
- **Medium Score (6 pts)**: Seattle, San Diego, Oxford UK, London
- **Low Score (2 pts)**: Other locations (remote work still valuable)

### Priority Tiers

Leads are automatically categorized:

- 🟢 **High Priority (70-100)**: Immediate outreach recommended
- 🟡 **Medium Priority (50-69)**: Qualified leads for nurture campaign
- 🔴 **Low Priority (0-49)**: Long-term nurture or deprioritize

### Example Scores

| Lead Profile | Role | Pub | Fund | Loc | **Total** | Priority |
|-------------|------|-----|------|-----|-----------|----------|
| Director of Toxicology @ Series B biotech in Cambridge, published on DILI 2024 | 36 | 40 | 20 | 10 | **106 → 95** | 🟢 High |
| Senior Scientist @ Public pharma in Boston, published 2021 | 24 | 20 | 16 | 10 | **70** | 🟢 High |
| Research Scientist @ Seed startup in Texas, no publications | 18 | 4 | 8 | 2 | **32** | 🔴 Low |

---

## 🛠 Tech Stack

### Backend
- **Python 3.11+** - Core language
- **Pandas** - Data manipulation and analysis
- **Biopython** - PubMed API integration
- **SQLAlchemy** - Database ORM
- **SQLite** - Local database

### Frontend
- **Streamlit** - Interactive web application
- **Plotly** - Data visualizations
- **Custom CSS** - Enhanced UI styling

### APIs & Data Sources
- **PubMed E-utilities** - NCBI official API (free)
- **Future**: LinkedIn (Proxycurl), Hunter.io (email), Crunchbase (funding)

### Development Tools
- **Git** - Version control
- **Docker** - Containerization
- **pytest** - Testing framework
- **python-dotenv** - Environment management

---

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/biotech-lead-generator.git
cd biotech-lead-generator

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Generate sample data (optional)
python scripts/generate_leads.py 200

# 6. Run the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Environment Variables (Optional)

Create a `.env` file for API keys:

```env
# PubMed
PUBMED_EMAIL=your.email@example.com
PUBMED_API_KEY=optional_api_key

# Future integrations
HUNTER_API_KEY=your_hunter_key
PROXYCURL_API_KEY=your_proxycurl_key
```

---

## 💡 Usage

### 1. Load Sample Data

On first launch:
1. Click **"Load Sample Data"** button in the sidebar
2. System loads 10 pre-scored leads for demonstration
3. Explore the dashboard, charts, and filters

### 2. Search PubMed for Real Leads

To find actual researchers:
1. Navigate to **Dashboard** tab
2. Select **"PubMed Search"** from data source dropdown
3. Enter query: `drug-induced liver injury 3D models`
4. Click **"Search PubMed"**
5. Wait 30-60 seconds for API calls
6. View discovered leads with automatic scoring

**Example Queries:**
- `hepatotoxicity organoids`
- `liver spheroids drug screening`
- `DILI prediction in vitro`
- `microphysiological systems toxicity`

### 3. Adjust Scoring Weights

Customize scoring algorithm:
1. Open sidebar **"Scoring Weights"** section
2. Adjust sliders:
   - **Role Fit**: 0-50 points
   - **Recent Publication**: 0-50 points
   - **Company Funding**: 0-30 points
   - **Strategic Location**: 0-20 points
3. Ensure total = 100
4. Click **"Apply Weights"**
5. Scores recalculate instantly

### 4. Search and Filter

Find specific leads:
1. Navigate to **"Search & Filter"** tab
2. **Text Search**: Type name, title, or company
3. **Score Filter**: Set minimum score (e.g., 70 for high-priority only)
4. **Location Filter**: Select specific locations
5. Results update in real-time

### 5. Export Data

Download leads in multiple formats:
1. Sidebar → **"Export"** section
2. **CSV**: Plain text, compatible with any tool
3. **Excel**: Formatted with color-coded scores (green/yellow/red)
4. Click download button
5. File downloads to your computer

**For Google Sheets:**
1. Export as CSV
2. Go to sheets.google.com
3. File → Import → Upload CSV
4. Apply formatting as needed

### 6. Add Manual Leads

Supplement with custom entries:
1. Navigate to **"Add New Leads"** tab
2. Fill in form:
   - Name (required)
   - Job Title (required)
   - Company (required)
   - Location (required)
   - Email, LinkedIn (optional)
   - Publication status
   - Funding stage
3. Click **"Add Lead"**
4. Lead is scored and added to database

---

## 📁 Project Structure

```
biotech-lead-generator/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variables template
├── .gitignore                         # Git ignore rules
├── Dockerfile                         # Docker configuration
├── docker-compose.yml                 # Docker Compose setup
│
├── app.py                             # Main Streamlit application
├── config.py                          # Configuration management
│
├── src/                               # Source code
│   ├── __init__.py
│   │
│   ├── data_sources/                  # Data collection modules
│   │   ├── __init__.py
│   │   ├── pubmed_scraper.py         # PubMed API integration
│   │   ├── linkedin_mock.py          # LinkedIn data (mock/future)
│   │   ├── conference_scraper.py     # Conference scraping (future)
│   │   └── funding_scraper.py        # Funding data (future)
│   │
│   ├── enrichment/                    # Data enrichment
│   │   ├── __init__.py
│   │   ├── email_finder.py           # Email discovery (future)
│   │   └── company_enricher.py       # Company data (future)
│   │
│   ├── scoring/                       # Scoring engine
│   │   ├── __init__.py
│   │   └── propensity_scorer.py      # Lead scoring algorithm
│   │
│   ├── database/                      # Database management
│   │   ├── __init__.py
│   │   └── db_manager.py             # SQLite operations
│   │
│   └── utils/                         # Utilities
│       ├── __init__.py
│       ├── export_helper.py          # CSV/Excel export
│       ├── data_validator.py         # Data validation
│       └── google_sheets_exporter.py # Google Sheets prep
│
├── data/                              # Data storage
│   ├── raw/                          # Raw scraped data
│   ├── processed/                    # Processed data
│   ├── sample/                       # Sample datasets
│   │   └── sample_leads.csv
│   └── leads.db                      # SQLite database
│
├── scripts/                           # Utility scripts
│   ├── generate_leads.py             # Sample data generator
│   ├── test_system.py                # System tests
│   └── db_utils.py                   # Database utilities
│
├── tests/                            # Unit tests
│   ├── __init__.py
│   ├── test_scoring.py
│   ├── test_pubmed.py
│   └── test_export.py
│
└── .streamlit/                       # Streamlit configuration
    └── config.toml
```

---

## 🔌 Data Sources

### Currently Implemented

| Source | Status | API | Cost | Coverage |
|--------|--------|-----|------|----------|
| **PubMed** | ✅ Active | Official NCBI E-utilities | Free | Researchers, academic institutions, publications |
| **Sample Data** | ✅ Active | N/A | Free | Demo/testing purposes |
| **Manual Entry** | ✅ Active | N/A | Free | Custom lead addition |

### Future Integrations

| Source | Purpose | Estimated Effort | API/Tool |
|--------|---------|------------------|----------|
| **LinkedIn** | Job titles, company info, locations | 2-3 days | Proxycurl API ($99/mo) |
| **Hunter.io** | Email discovery and verification | 1 day | Hunter.io API ($49/mo) |
| **Crunchbase** | Funding data, company stages | 1-2 days | Crunchbase API ($29/mo) |
| **Conference Sites** | SOT, AACR, ISSX attendee lists | 3-4 days | Web scraping |
| **NIH RePORTER** | Grant recipients (academic) | 2 days | Free API |
| **Clearbit** | Company enrichment | 1 day | Clearbit API |

### PubMed Integration Details

**How it works:**
1. Search PubMed with relevant queries (e.g., "DILI 3D models")
2. Retrieve recent papers (last 2-3 years)
3. Extract corresponding authors (usually PI with budget)
4. Parse affiliations for company/institution
5. Create lead profile with publication data
6. Calculate propensity score

**Rate Limits:**
- 3 requests per second without API key
- 10 requests per second with API key (free)

**Example Query:**
```python
from src.data_sources.pubmed_scraper import PubMedScraper

scraper = PubMedScraper(email="your.email@example.com")
leads = scraper.search_authors(
    query="drug-induced liver injury 3D models",
    max_results=50,
    years_back=2
)
```

---

## 🚀 Deployment

### Option 1: Streamlit Cloud (Recommended)

**Free, easy, perfect for demos:**

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repository and branch
5. Main file: `app.py`
6. Click **"Deploy"**

**Limitations:** 1GB RAM, 1 CPU core, public access only

### Option 2: Docker

**For consistent environments:**

```bash
# Build image
docker build -t biotech-lead-gen .

# Run container
docker run -p 8501:8501 biotech-lead-gen

# Or use Docker Compose
docker-compose up -d
```

**Production deployment:**
```bash
# Build for production
docker build -t biotech-lead-gen:prod --build-arg ENV=production .

# Run with environment variables
docker run -p 8501:8501 --env-file .env biotech-lead-gen:prod
```

### Option 3: Railway.app

**Simple, affordable hosting:**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

**Cost:** ~$5/month, includes custom domain

### Option 4: AWS/GCP (Enterprise)

**For production scale:**

**AWS Elastic Beanstalk:**
```bash
eb init
eb create biotech-lead-gen-env
eb deploy
```

**Google Cloud Run:**
```bash
gcloud run deploy biotech-lead-gen \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Cost:** ~$20-50/month depending on usage

---

## 📊 Examples

### Example 1: Finding High-Priority Leads

```python
# Using the scoring module programmatically
from src.scoring.propensity_scorer import PropensityScorer
import pandas as pd

# Create lead
lead = pd.Series({
    'title': 'Director of Toxicology',
    'recent_publication': True,
    'publication_year': 2024,
    'company_funding': 'Series B',
    'location': 'Cambridge, MA'
})

# Score it
scorer = PropensityScorer()
score = scorer.calculate_score(lead)
print(f"Propensity Score: {score}/100")  # Output: 95/100

# Get explanation
explanation = scorer.explain_score(lead)
print(explanation)
```

### Example 2: Batch Processing

```python
# Score multiple leads at once
from src.database.db_manager import DatabaseManager
from src.scoring.propensity_scorer import PropensityScorer

# Load leads from database
db = DatabaseManager()
leads_df = db.get_all_leads()

# Score and rank
scorer = PropensityScorer()
scored_df = scorer.score_batch(leads_df)

# Filter high-priority
high_priority = scored_df[scored_df['propensity_score'] >= 70]
print(f"Found {len(high_priority)} high-priority leads")
```

### Example 3: Custom Scoring Weights

```python
# Adjust weights for different campaigns
custom_weights = {
    'role_fit': 40,        # Emphasize role
    'publication': 30,     # Less focus on pubs
    'funding': 20,         # Same
    'location': 10         # Same
}

scorer = PropensityScorer(weights=custom_weights)
score = scorer.calculate_score(lead)
```

---

## 🗺 Roadmap

### Phase 1: MVP ✅ (Current)
- [x] Core scoring algorithm
- [x] PubMed integration
- [x] Streamlit dashboard
- [x] CSV/Excel export
- [x] Sample data generator
- [x] Database persistence
- [x] Documentation

### Phase 2: Data Enrichment (Next 1-2 months)
- [ ] LinkedIn integration (Proxycurl API)
- [ ] Email discovery (Hunter.io)
- [ ] Company data enrichment (Clearbit)
- [ ] Conference attendee scraping
- [ ] Automated data pipelines (Apache Airflow)

### Phase 3: Advanced Features (2-4 months)
- [ ] User authentication and multi-tenancy
- [ ] PostgreSQL database for production scale
- [ ] CRM integrations (Salesforce, HubSpot)
- [ ] Email campaign integration
- [ ] Advanced AI scoring with GPT-4
- [ ] Predictive analytics and trends

### Phase 4: Enterprise (4-6 months)
- [ ] White-label solution
- [ ] API for third-party integrations
- [ ] Mobile application
- [ ] Real-time alerts and notifications
- [ ] Team collaboration features
- [ ] Advanced reporting and analytics

---

## 🤝 Contributing

Contributions are welcome! This project is actively maintained.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Make your changes**
4. **Commit with clear messages**
   ```bash
   git commit -m 'Add AmazingFeature: description'
   ```
5. **Push to your branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
6. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/biotech-lead-generator.git

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/biotech-lead-generator.git

# Create development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Additional dev dependencies

# Run tests
pytest tests/ -v

# Run with hot reload
streamlit run app.py
```

### Code Style

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Write unit tests for new features
- Keep functions focused and small

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_scoring.py -v

# Run with output
pytest tests/ -v -s
```

### Test Data

```bash
# Generate test data
python scripts/generate_leads.py 50

# Test scoring algorithm
python -c "from tests.test_scoring import test_scoring_algorithm; test_scoring_algorithm()"

# Test PubMed integration
python -c "from tests.test_pubmed import test_pubmed_search; test_pubmed_search()"
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📚 Additional Resources

### Documentation
- [PubMed E-utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Best Practices](https://docs.python-guide.org/)

### Related Tools
- [Clay.com](https://clay.com) - Commercial lead enrichment
- [Apollo.io](https://apollo.io) - Sales intelligence platform
- [ZoomInfo](https://zoominfo.com) - B2B database

### Research Papers
- NAMs (New Approach Methodologies) in Toxicology
- 3D Cell Culture Models in Drug Discovery
- Predictive Toxicology Using In Vitro Systems

---

## 💬 FAQ

**Q: How accurate is the scoring algorithm?**
A: The algorithm provides data-driven prioritization. Accuracy improves with weight calibration based on your actual conversion data.

**Q: Can I use this for other industries?**
A: Yes! The modular design allows adaptation to any B2B lead generation use case. Modify scoring criteria and data sources accordingly.

**Q: How many leads can the system handle?**
A: Current SQLite setup handles 10,000+ leads efficiently. For enterprise scale (100,000+), migrate to PostgreSQL.

**Q: Is PubMed the only data source?**
A: Currently yes, but the system is designed for multiple sources. LinkedIn, Hunter.io, and Crunchbase integration is planned.

**Q: How often should I update lead data?**
A: Recommended: Weekly for high-priority leads, monthly for full database. PubMed updates daily.

**Q: Can I customize the scoring algorithm?**
A: Absolutely! Adjust weights in the UI or modify `propensity_scorer.py` for custom logic.

---

## 📈 Performance

**Current Metrics:**
- Load time: < 2 seconds
- PubMed search: 30-60 seconds for 50 results
- Scoring speed: 1000+ leads/second
- Export speed: < 5 seconds for 500 leads
- Database query: < 100ms for most operations

**Optimization Tips:**
- Cache PubMed results to avoid re-fetching
- Use database indexes for large datasets
- Enable Streamlit caching for expensive operations
- Batch process large imports

---

## 🔐 Security & Privacy

**Data Handling:**
- All data stored locally (SQLite)
- No cloud storage by default
- API keys stored in environment variables
- No logging of sensitive information

**Compliance:**
- PubMed data: Public domain
- Respect website Terms of Service
- GDPR: Add consent mechanisms for EU contacts
- CCPA: Implement opt-out for California contacts

**Best Practices:**
- Never commit `.env` files
- Rotate API keys regularly
- Use HTTPS in production
- Implement authentication for multi-user deployments
---

**Version:** 1.0.0  
**Last Updated:** December 2024  
**Status:** Active Development
