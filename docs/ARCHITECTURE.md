# RCM GCC Architecture

## System Overview

The RCM GCC platform is a modern, AI-native revenue cycle management system designed specifically for GCC healthcare workflows. The architecture follows a microservices pattern with clear separation of concerns and robust AI integration.

## Architecture Components

### 1. Frontend Layer (Next.js)
- **Technology**: Next.js 14 with App Router, TypeScript, TailwindCSS
- **UI Framework**: shadcn/ui components with Radix UI primitives
- **State Management**: React hooks with SWR for data fetching
- **Animations**: Framer Motion for smooth interactions
- **Charts**: Recharts for data visualization

### 2. API Layer (Flask)
- **Framework**: Flask with Blueprint architecture
- **Validation**: Pydantic for request/response validation
- **Database**: SQLAlchemy ORM with PostgreSQL
- **Authentication**: Simple role-based demo system
- **CORS**: Configured for cross-origin requests

### 3. AI Layer (LangChain + Gemini)
- **LLM**: Google Gemini 1.5 Pro
- **Framework**: LangChain for chain orchestration
- **Features**: 
  - Eligibility verification
  - Prior authorization generation
  - Medical coding assistance
  - Claims scrubbing
  - Denial analysis

### 4. Data Layer (PostgreSQL)
- **Database**: PostgreSQL 15 with proper indexing
- **ORM**: SQLAlchemy with relationship management
- **Migrations**: Alembic for schema management
- **Seeding**: Comprehensive demo data generator

## Data Flow

### 1. Eligibility Workflow
```
Patient Data → AI Analysis → Coverage Verification → Suggestions
```

### 2. Prior Authorization Workflow
```
Clinical Data → AI Processing → Requirements Checklist → Draft Letter
```

### 3. Medical Coding Workflow
```
Clinical Notes → AI Analysis → ICD-10/CPT Suggestions → Confidence Scoring
```

### 4. Claims Processing Workflow
```
Claim Data → AI Scrubbing → Issue Detection → Recommendations → Submission
```

## Security Considerations

- **API Security**: Input validation with Pydantic
- **CORS**: Configured for specific origins
- **Database**: Parameterized queries via SQLAlchemy
- **Environment**: Secure configuration management
- **Docker**: Non-root user execution

## Scalability Features

- **Stateless API**: Easy horizontal scaling
- **Database**: Connection pooling and indexing
- **Caching**: SWR for frontend caching
- **Load Balancing**: Ready for container orchestration
- **Monitoring**: Health checks and logging

## Deployment Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Layer     │    │   Database      │
│   (Next.js)     │◄──►│   (Flask)       │◄──►│   (PostgreSQL)  │
│   Port: 3001    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   AI Services   │
                    │   (Gemini)     │
                    └─────────────────┘
```

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Frontend | Next.js | 14.0.4 |
| Backend | Flask | 3.0.0 |
| Database | PostgreSQL | 15 |
| AI/LLM | Google Gemini | 1.5-pro |
| Container | Docker | Latest |
| Orchestration | Docker Compose | 3.8 |

## Performance Considerations

- **Frontend**: Code splitting and lazy loading
- **API**: Connection pooling and async processing
- **Database**: Proper indexing and query optimization
- **AI**: Caching and fallback responses
- **Monitoring**: Health checks and metrics collection
