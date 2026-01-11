# 🏗️ Phase 2: Production Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   Web App    │    │  Mobile App  │    │  Chrome Ext  │          │
│  │  (Next.js)   │    │ (React Native)│   │  (Optional)  │          │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘          │
│         │                    │                    │                  │
│         └────────────────────┴────────────────────┘                  │
│                              │                                       │
└──────────────────────────────┼───────────────────────────────────────┘
                               │
                               │ HTTPS / REST API
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│                       API GATEWAY LAYER                               │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌────────────────────────────────────────────────────────────┐      │
│  │                   FastAPI Backend                           │      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │      │
│  │  │   Auth   │  │  Leads   │  │  Search  │  │  Export  │   │      │
│  │  │   API    │  │   API    │  │   API    │  │   API    │   │      │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │      │
│  └────────────────────────────────────────────────────────────┘      │
│                                                                        │
└────────────────────────────────┬──────────────────────────────────────┘
                                 │
                                 │
┌────────────────────────────────▼──────────────────────────────────────┐
│                       SERVICE LAYER                                    │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│  │   Scoring    │  │  Enrichment  │  │   Pipeline   │                │
│  │   Engine     │  │   Service    │  │   Scheduler  │                │
│  └──────────────┘  └──────────────┘  └──────────────┘                │
│                                                                         │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 │
┌────────────────────────────────▼───────────────────────────────────────┐
│                       DATA SOURCES LAYER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  PubMed  │  │ LinkedIn │  │Conference│  │ Crunchbase│ │  NIH   │  │
│  │   API    │  │(Proxycurl)│ │ Scrapers │  │    API   │  │ Grants │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                             │
│  │ Hunter.io│  │ Clearbit │  │  Google  │                             │
│  │  Email   │  │ Company  │  │  Scholar │                             │
│  └──────────┘  └──────────┘  └──────────┘                             │
│                                                                          │
└─────────────────────────────────┬──────────────────────────────────────┘
                                  │
                                  │
┌─────────────────────────────────▼──────────────────────────────────────┐
│                       PERSISTENCE LAYER                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │   PostgreSQL     │    │    Redis     │    │   S3 Storage │         │
│  │   (Supabase)     │    │  (Upstash)   │    │ (Cloudflare) │         │
│  │   - Leads        │    │  - Cache     │    │  - Exports   │         │
│  │   - Users        │    │  - Sessions  │    │  - Uploads   │         │
│  │   - Searches     │    │  - Jobs      │    │              │         │
│  └──────────────────┘    └──────────────┘    └──────────────┘         │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                       INFRASTRUCTURE LAYER                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  │
│  │  Render  │  │  Vercel  │  │  GitHub  │  │  Sentry  │  │ Grafana │  │
│  │ (Backend)│  │(Frontend)│  │ Actions  │  │  (Logs)  │  │(Metrics)│  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └─────────┘  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Frontend (Client Layer)

**Primary: Next.js Web App**
- **Framework:** Next.js 14 (App Router)
- **Styling:** TailwindCSS + shadcn/ui
- **State:** React Query + Zustand
- **Charts:** Recharts + Plotly
- **Deployment:** Vercel (free tier - 100GB bandwidth/month)

**Optional: Chrome Extension**
- LinkedIn lead capture
- One-click lead addition
- Real-time scoring

### 2. Backend API (API Gateway)

**Framework:** FastAPI
- **Authentication:** JWT tokens + Supabase Auth
- **Documentation:** Auto-generated OpenAPI/Swagger
- **Rate Limiting:** slowapi middleware
- **CORS:** Configured for frontend domain
- **Deployment:** Render.com (free tier - 750 hours/month)

**API Endpoints:**
```
/api/v1/auth/*          - Authentication
/api/v1/leads/*         - Lead management
/api/v1/search/*        - Lead search/filter
/api/v1/enrich/*        - Data enrichment
/api/v1/export/*        - Data export
/api/v1/scoring/*       - Scoring operations
/api/v1/pipelines/*     - Data pipeline control
/api/v1/analytics/*     - Usage analytics
```

### 3. Service Layer

**Scoring Engine**
- Weighted algorithm (configurable)
- ML-based predictions (optional)
- Batch scoring capability
- Historical score tracking

**Enrichment Service**
- Email finding (Hunter.io)
- Company data (Clearbit)
- Social profiles (LinkedIn)
- Contact verification

**Pipeline Scheduler**
- Automated daily searches
- Data refresh jobs
- Email notifications
- Webhook triggers

### 4. Data Sources Integration

**Implemented (Free):**
- ✅ PubMed API
- ✅ Google Scholar (web scraping)
- ✅ NIH RePORTER API
- ✅ Conference websites (scraping)

**Paid APIs (with free tiers):**
- 🔸 Proxycurl (LinkedIn) - 100 free credits
- 🔸 Hunter.io (Email) - 25 searches/month
- 🔸 Clearbit (Company) - 50 requests/month
- 🔸 Crunchbase (Funding) - Limited free access

### 5. Database Architecture

**PostgreSQL Schema (Supabase):**

```sql
-- Users table
users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE,
  full_name TEXT,
  created_at TIMESTAMP,
  subscription_tier TEXT
)

-- Leads table
leads (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name TEXT,
  title TEXT,
  company TEXT,
  location TEXT,
  email TEXT,
  linkedin_url TEXT,
  propensity_score INTEGER,
  rank INTEGER,
  data_sources JSONB,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

-- Searches table
searches (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  query TEXT,
  filters JSONB,
  results_count INTEGER,
  created_at TIMESTAMP
)

-- Enrichments table
enrichments (
  id UUID PRIMARY KEY,
  lead_id UUID REFERENCES leads(id),
  enrichment_type TEXT,
  data JSONB,
  source TEXT,
  created_at TIMESTAMP
)

-- Exports table
exports (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  file_url TEXT,
  format TEXT,
  records_count INTEGER,
  created_at TIMESTAMP
)

-- Pipelines table
pipelines (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name TEXT,
  config JSONB,
  schedule TEXT,
  last_run TIMESTAMP,
  next_run TIMESTAMP,
  status TEXT
)
```

### 6. Caching Strategy (Redis)

**Cache Keys:**
```
user:session:{user_id}          - User session (TTL: 24h)
leads:search:{hash}             - Search results (TTL: 1h)
enrichment:{lead_id}:{type}     - Enrichment data (TTL: 7d)
pubmed:results:{query}          - PubMed cache (TTL: 24h)
rate_limit:{user_id}:{endpoint} - Rate limiting (TTL: 1m)
```

### 7. File Storage (Cloudflare R2)

**Bucket Structure:**
```
exports/
  ├── {user_id}/
  │   ├── {date}/
  │   │   ├── leads_export_20241227.csv
  │   │   └── leads_export_20241227.xlsx
uploads/
  ├── {user_id}/
  │   └── bulk_upload_20241227.csv
```

### 8. Monitoring & Logging

**Sentry (Error Tracking)**
- Backend errors
- Frontend errors
- Performance monitoring
- User feedback

**Grafana + Prometheus (Metrics)**
- API response times
- Database queries
- Cache hit rates
- Active users
- Lead processing stats

### 9. CI/CD Pipeline

**GitHub Actions Workflows:**

```yaml
# .github/workflows/backend.yml
- Build and test backend
- Run migrations
- Deploy to Render

# .github/workflows/frontend.yml  
- Build Next.js app
- Run tests
- Deploy to Vercel

# .github/workflows/data-pipeline.yml
- Run daily PubMed searches
- Update lead scores
- Send summary emails
```

---

## Technology Stack (All Free Tier)

### Infrastructure & Hosting

| Service | Purpose | Free Tier Limits |
|---------|---------|------------------|
| **Vercel** | Frontend hosting | 100GB bandwidth, unlimited deployments |
| **Render** | Backend API | 750 hours/month, 512MB RAM |
| **Supabase** | PostgreSQL DB | 500MB database, 2GB bandwidth |
| **Upstash** | Redis cache | 10,000 commands/day |
| **Cloudflare R2** | Object storage | 10GB storage, 1M requests/month |
| **GitHub Actions** | CI/CD | 2,000 minutes/month |

### APIs & Services

| Service | Purpose | Free Tier Limits |
|---------|---------|------------------|
| **PubMed** | Publications | Unlimited (rate limited) |
| **NIH RePORTER** | Grant data | Unlimited |
| **Proxycurl** | LinkedIn data | 100 credits (then $99/month) |
| **Hunter.io** | Email finding | 25 searches/month |
| **Resend** | Email sending | 3,000 emails/month |
| **Sentry** | Error tracking | 5,000 events/month |

### Development Tools

| Tool | Purpose | Cost |
|------|---------|------|
| **VS Code** | IDE | Free |
| **Postman** | API testing | Free |
| **Docker** | Containerization | Free |
| **Git + GitHub** | Version control | Free |
| **Figma** | UI design | Free |

---

## Security & Compliance

### Authentication
- JWT tokens with refresh mechanism
- OAuth providers (Google, GitHub)
- Role-based access control (RBAC)
- API key management for integrations

### Data Protection
- Encrypted at rest (PostgreSQL)
- Encrypted in transit (HTTPS/TLS)
- PII masking in logs
- GDPR compliance features
- Data export/deletion tools

### Rate Limiting
- User tier-based limits
- API endpoint throttling
- DDoS protection (Cloudflare)
- Abuse prevention

---

## Deployment Strategy

### Environment Structure

```
Development (Local)
  ├── Docker Compose
  ├── Local PostgreSQL
  └── Mock APIs

Staging (Render/Vercel)
  ├── Supabase (staging DB)
  ├── Real APIs (test mode)
  └── Limited data

Production (Render/Vercel)
  ├── Supabase (prod DB)
  ├── Real APIs (live mode)
  └── Full data + monitoring
```

### Rollout Plan

**Week 1-2:** Backend API + Database
**Week 3-4:** Frontend MVP
**Week 5-6:** Data sources integration
**Week 7-8:** Authentication + Multi-tenancy
**Week 9-10:** Advanced features
**Week 11-12:** Testing + Polish

---

## Performance Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| API Response Time | < 200ms | Redis caching, DB indexes |
| Page Load Time | < 2s | Next.js optimization, CDN |
| Lead Processing | 1000/hour | Background jobs, batching |
| Uptime | 99.5% | Health checks, auto-restart |
| Concurrent Users | 100+ | Horizontal scaling ready |

---

## Cost Analysis (Free Tier)

**Monthly Costs:**
- Infrastructure: $0 (free tiers)
- APIs (within limits): $0
- Monitoring: $0 (free tiers)
- **Total: $0/month**

**When You Exceed Free Tiers:**
- Render: ~$7/month for better performance
- Supabase: ~$25/month for more DB space
- Proxycurl: ~$99/month for more LinkedIn data
- Hunter.io: ~$49/month for more email searches
- **Estimated: $50-180/month** depending on usage

---

## Next Steps

This architecture gives you:
- ✅ Production-grade scalability
- ✅ Enterprise features
- ✅ Cost-effective (starts free)
- ✅ Professional portfolio piece
- ✅ Monetization ready

Ready to start building? Let's begin with Phase 2.1: Backend API Setup!
