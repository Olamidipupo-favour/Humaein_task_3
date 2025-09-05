# RCM GCC API

AI-Native Revenue Cycle Management API for GCC healthcare workflows.

## Features

- **Eligibility Verification** - AI-powered patient coverage checks
- **Prior Authorization** - Automated PA requirements and letter generation
- **Medical Coding** - ICD-10/CPT code suggestions with rationale
- **Claims Scrubbing** - Pre-submission validation and error detection
- **Claims Submission** - Electronic claim filing with tracking
- **Remittance Tracking** - Payment monitoring and reconciliation
- **Denial Management** - Appeal processing with AI guidance

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL
- Google API Key (for Gemini AI)

### Development Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Run development server:**
   ```bash
   uv run dev
   ```

4. **Seed demo data:**
   ```bash
   uv run seed
   ```

### Production

```bash
uv run start
```

## API Endpoints

### Health Check
- `GET /health` - Service health status

### RCM Workflows
- `POST /rcm/eligibility/check` - Check patient eligibility
- `POST /rcm/prior-auth/draft` - Generate prior authorization
- `POST /rcm/coding/suggest` - Suggest medical coding
- `POST /rcm/scrub` - Scrub claims for issues
- `POST /rcm/claims/submit` - Submit claims to payers
- `GET /rcm/remittance/{claim_id}` - Get remittance info
- `POST /rcm/denials/appeal` - Appeal claim denials
- `GET /rcm/dashboard/stats` - Get dashboard statistics

## AI Integration

The API integrates with Google Gemini 1.5 Pro for intelligent RCM assistance:

- **Eligibility Analysis** - Coverage verification and suggestions
- **Prior Auth Generation** - Requirements checklist and letter drafts
- **Coding Assistance** - ICD-10/CPT code suggestions with confidence
- **Claims Scrubbing** - Issue detection and recommendations
- **Denial Analysis** - Appeal guidance and success strategies

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google AI API key | Required |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://postgres:postgres@db:5432/rcm` |
| `APP_ENV` | Environment (dev/prod) | `dev` |
| `ALLOW_ORIGINS` | CORS allowed origins | `*` |
| `MODEL_NAME` | AI model name | `gemini-1.5-pro` |

## Database Schema

The API uses SQLAlchemy with the following main entities:

- **Provider** - Healthcare providers and their specialties
- **Payer** - Insurance companies and government payers
- **Patient** - Patient demographics and insurance info
- **Encounter** - Clinical encounters and documentation
- **Claim** - Insurance claims with status tracking
- **ClaimLine** - Individual claim line items
- **Remittance** - Payment and adjustment information
- **Denial** - Claim denials and appeal tracking
- **User** - System users with role-based access

## Development

### Code Quality

```bash
# Format code
uv run black .

# Lint code
uv run ruff check .

# Type checking
uv run mypy .
```

### Testing

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=app
```

## Docker

```bash
# Build image
docker build -t rcm-gcc-api .

# Run container
docker run -p 8000:8000 --env-file .env rcm-gcc-api
```

## License

Built for Humaein - Contact: contact@humaein.com
