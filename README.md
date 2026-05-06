# DAST Platform — Dynamic Application Security Testing

> A professional-grade web vulnerability scanner built for bug bounty hunters, security researchers, and penetration testers.

![DAST Platform](frontend/public/hero-bg.png)

---

## Overview

DAST Platform is a full-stack automated vulnerability scanning tool that orchestrates multiple security engines from a single dashboard. It performs real-time vulnerability detection with live scan logs, severity classification, and downloadable PDF reports.

---

## Features

- **Multi-Phase Scanning** — Recon, Content Discovery, Crawling, Vulnerability Scanning, Fuzzing
- **Nuclei Engine** — Template-based CVE detection with 8,000+ community templates
- **OWASP ZAP** — Automated spidering and active vulnerability scanning
- **Advanced Fuzzer** — Detects SQLi, XSS, SSTI, SSRF, LFI, CORS, Open Redirect, Clickjacking, Security Headers
- **Real-time WebSocket** — Live scan logs and vulnerability findings as they happen
- **PDF Reports** — Professional executive summary reports with CVSS scores and CWE mappings
- **JWT Authentication** — Secure login/registration with access and refresh tokens
- **SSRF Protection** — Three-tier target verification with DNS resolution and private IP blocking

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript |
| Backend | FastAPI (Python), Uvicorn |
| Database | PostgreSQL 18 (pgAdmin) |
| Task Queue | Celery + Redis |
| Scan Engines | Nuclei, OWASP ZAP, Custom Fuzzer |
| Auth | JWT (python-jose), bcrypt |
| PDF | ReportLab |

---

## Prerequisites

- Python 3.11+ (recommended) or 3.14
- Node.js 18+
- PostgreSQL 18 (via pgAdmin)
- Redis (installed via winget or Docker)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/dast-platform.git
cd dast-platform
```

### 2. Backend setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5433/dast_db
DATABASE_URL_SYNC=postgresql://postgres:YOUR_PASSWORD@localhost:5433/dast_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=7
APP_NAME=DAST Platform
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
DEBUG=true
```

### 3. Database setup

In pgAdmin Query Tool:

```sql
-- Create tables
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_admin BOOLEAN NOT NULL DEFAULT false,
    tos_accepted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

Or let the backend auto-create tables on startup.

### 4. Frontend setup

```bash
cd frontend
npm install
```

---

## Running the Project

Open **3 terminals** and run one command in each:

**Terminal 1 — Backend:**
```powershell
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — Celery Worker:**
```powershell
cd backend
celery -A app.workers.celery_app worker --loglevel=info --pool=solo
```

**Terminal 3 — Frontend:**
```powershell
cd frontend
npm run dev
```

Open: **http://localhost:3000**

---

## API Documentation

Once the backend is running, visit:

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

---

## Scan Types

| Type | Description |
|---|---|
| 🔥 Full Scan | All phases — most thorough |
| 🔎 Nuclei Only | Template-based CVE detection |
| 🌐 Discovery + Fuzzing | SQLi, XSS, Headers, CORS, LFI |
| 🧠 ZAP Spider | Deep crawling and active testing |
| 💥 ZAP + Nuclei | Combined active + template scan |

---

## Vulnerability Detection

The fuzzer detects:

- SQL Injection (error-based + time-based)
- Reflected XSS
- Server-Side Template Injection (SSTI)
- Server-Side Request Forgery (SSRF)
- Local File Inclusion (LFI)
- Open Redirect
- Clickjacking
- CORS Misconfiguration
- Missing Security Headers (7 checks)
- Information Disclosure
- Exposed sensitive files (.env, .git, backups)
- Admin panel exposure

---

## Project Structure

```
dast-platform/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes (auth, scans, reports, websocket)
│   │   ├── core/         # Security, target verification
│   │   ├── models/       # SQLAlchemy models (User, Scan, Vulnerability)
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # PDF generator
│   │   ├── workers/      # Celery tasks, Nuclei, ZAP, Fuzzer engines
│   │   └── utils/        # CVSS, CWE mapping
│   ├── alembic/          # Database migrations
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── app/          # Next.js pages (dashboard, scans, reports, about)
│       ├── components/   # HackerScene animation
│       ├── hooks/        # useAuth, useWebSocket
│       ├── lib/          # API client, constants
│       └── types/        # TypeScript types
└── docker-compose.yml    # PostgreSQL, Redis, ZAP
```

---

## Legal Disclaimer

This tool is designed for **authorized security testing only**. You must have explicit written permission from the target owner before scanning. Unauthorized scanning is illegal and may result in criminal prosecution. The developers are not responsible for any misuse of this tool.

---

## Author

Built by **Mulugeta Ababi** — Ethical Hacker & Security Researcher

- GitHub: [github.com/mulugeta24](https://github.com/mulugeta24)
- Telegram: [t.me/InfoSecureTech](https://t.me/InfoSecureTech)
- YouTube: [@ApexTechEthiopia](https://www.youtube.com/@ApexTechEthiopia)
