# AI Career Discovery Assistant

AI-powered career path analysis and recommendation system focused on the Japanese market. This service analyzes resumes, CVs, and skill sheets to reveal hidden career potential and generate personalized pathways for career transitions.

## 🎯 Overview

The AI Career Discovery Assistant helps working professionals discover new career opportunities by:
- Analyzing uploaded resumes/CVs using advanced NLP
- Generating career paths across corporate, freelance, and entrepreneurship domains
- Providing skill gap analysis and learning recommendations
- Offering market insights and salary data (Premium)

## 🚀 Key Features

### Phase 1 (MVP)
- Document upload (PDF/Word) with Japanese format support
- AI-powered skill extraction and analysis
- Basic career path generation
- Visual dashboard with career recommendations

### Phase 2 (Enhanced)
- Advanced skill gap analysis
- Integration with Japanese learning platforms
- Business model templates for entrepreneurs
- User feedback system

### Phase 3 (Premium)
- Market salary data integration
- Qualification relevance analysis
- Mentor network connections
- Progress tracking

## 🏗️ Architecture

```
Frontend (React + TypeScript)
    ↓
API Gateway
    ↓
Backend Services (FastAPI)
    ↓
AI/ML Engine (Transformers + Custom Models)
    ↓
Data Layer (PostgreSQL + Redis + S3)
```

## 🛠️ Tech Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Backend**: Python, FastAPI, SQLAlchemy, Celery
- **AI/ML**: Hugging Face Transformers, Japanese BERT models, LangChain
- **Infrastructure**: Docker, Kubernetes, GitHub Actions
- **Database**: PostgreSQL, Redis, S3/GCS

## 📋 Prerequisites

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local frontend development)
- Google Gemini API key

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/NJersyHiro/ai-career-discovery-assistant.git
cd ai-career-discovery-assistant
```

2. **Set up environment variables**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add your GEMINI_API_KEY
```

3. **Start the development environment**
```bash
# Using Docker (recommended)
docker-compose up -d

# Or run the setup script
./scripts/setup-dev.sh
```

4. **Run database migrations**
```bash
# If using Docker
./scripts/run-migrations.sh

# Or using Make
make db-migrate
```

5. **Access the applications**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/v1/docs
- MinIO Console: http://localhost:9001 (minioadmin/minioadmin)

### Manual Setup (Alternative)

If you prefer to run services locally without Docker:

1. **Backend setup**
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

2. **Frontend setup**
```bash
cd frontend
npm install -g pnpm
pnpm install
pnpm dev
```

## 📁 Project Structure

```
.
├── frontend/          # React TypeScript application
├── backend/           # FastAPI Python services
├── ml-models/         # Machine learning models
├── infrastructure/    # Deployment configurations
├── docs/             # Documentation
├── DEVELOPMENT_PLAN.md # Detailed development roadmap
├── CLAUDE.md         # AI assistant guidance
└── TASKS.md          # Project requirements
```

## 🎯 Target Market

Initial focus on Japan with:
- Support for Japanese resume formats (履歴書) and CV formats (職務経歴書)
- Integration with Japanese learning platforms
- Compliance with Japan's Act on the Protection of Personal Information (APPI)

## 📊 Success Metrics

- **Activation Rate**: 50% of users complete analysis within first week
- **User Satisfaction**: 4.0/5.0 average rating
- **NPS Score**: +20 within 6 months

## 🔐 Security & Compliance

- APPI (Japan's Personal Information Protection Act) compliant
- End-to-end encryption for sensitive data
- Regular security audits
- GDPR-ready for future expansion

## 🤝 Contributing

This project is currently in initial development. Contribution guidelines will be added soon.

## 📄 License

License information will be added soon.

## 📞 Contact

For questions about this project, please open an issue on GitHub.

---

🇯🇵 **Made with ❤️ for the Japanese job market**