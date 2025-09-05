# RCM GCC - AI-Native Revenue Cycle Management Platform

A production-ready, demoable AI-native Revenue Cycle Management (RCM) platform designed specifically for GCC healthcare workflows.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd rcm-gcc

# Start the full stack
make up

# Seed demo data
make seed

# Access the application
# Frontend: http://localhost:3001
# API: http://localhost:8000
```

## 🏗️ Architecture

- **Backend**: Flask + LangChain + Gemini AI
- **Frontend**: Next.js + TypeScript + TailwindCSS + shadcn/ui
- **Database**: PostgreSQL with synthetic GCC data
- **AI**: Google Gemini 1.5 Pro for intelligent RCM assistance

## 📋 RCM Workflow Stages

1. **Eligibility** - Patient coverage verification
2. **Prior Auth** - Authorization request management
3. **Clinical Docs** - Document processing
4. **Medical Coding** - ICD-10/CPT code assignment
5. **Claims Scrubbing** - Pre-submission validation
6. **Claims Submission** - Electronic claim filing
7. **Remittance Tracking** - Payment monitoring
8. **Denial Management** - Appeal processing
9. **Claims Resubmission** - Corrected claim filing
10. **Reconciliation** - Financial reconciliation

## 🎯 Demo Credentials

- **Admin**: admin@demo.com / admin123
- **Biller**: biller@demo.com / biller123
- **Coder**: coder@demo.com / coder123
- **Analyst**: analyst@demo.com / analyst123

## 🛠️ Development

```bash
# Backend development
cd api
uv run dev

# Frontend development
cd web
yarn dev

# Run tests
make test
```

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Data Flow](docs/DATAFLOW.md)
- [Phasing Strategy](docs/PHASING.md)
- [Deployment Guide](docs/DEPLOY.md)

## 🤝 Contact

**Peter** - +234 814 970 0428  
**Email**: contact@humaein.com

---

*Built with modern AI-first architecture for GCC healthcare excellence.*
