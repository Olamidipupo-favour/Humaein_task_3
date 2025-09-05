# RCM GCC Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the RCM GCC platform across different environments, from local development to production.

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **Docker**: Docker Engine 20.10+
- **Docker Compose**: Docker Compose 2.0+
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: 20GB free space
- **Network**: Stable internet connection for AI API calls

### Required Accounts
- **Google Cloud**: For Gemini AI API access
- **GitHub**: For source code repository
- **Docker Hub**: For container registry (optional)

## Local Development Deployment

### 1. Clone Repository
```bash
git clone <repository-url>
cd rcm-gcc
```

### 2. Environment Setup
```bash
# Copy environment files
cp api/env.example api/.env
cp web/.env.example web/.env.local

# Edit environment variables
# Add your Google API key to api/.env
GOOGLE_API_KEY=your-google-api-key-here
```

### 3. Start Services
```bash
# Start all services
make up

# Check service status
make health

# View logs
make logs
```

### 4. Seed Database
```bash
# Wait for services to be healthy, then seed
make seed
```

### 5. Access Application
- **Frontend**: http://localhost:3001
- **API**: http://localhost:8000
- **Database**: localhost:5432

## Staging Deployment

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Application Deployment
```bash
# Clone repository
git clone <repository-url>
cd rcm-gcc

# Set environment variables
export GOOGLE_API_KEY=your-google-api-key
export APP_ENV=staging

# Build and start services
make build
make up
```

### 3. SSL Configuration (Optional)
```bash
# Install Nginx
sudo apt install nginx

# Configure reverse proxy
sudo nano /etc/nginx/sites-available/rcm-gcc

# Enable site
sudo ln -s /etc/nginx/sites-available/rcm-gcc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Production Deployment

### 1. Infrastructure Setup

#### Option A: Single Server
```bash
# Minimum specs: 4 CPU, 16GB RAM, 100GB SSD
# Follow staging deployment steps with production environment
export APP_ENV=production
export SECRET_KEY=your-secure-secret-key
```

#### Option B: Multi-Server (Recommended)
```bash
# Load Balancer: 2 CPU, 4GB RAM
# API Servers: 4 CPU, 16GB RAM each
# Database Server: 8 CPU, 32GB RAM, 500GB SSD
# Frontend Server: 2 CPU, 8GB RAM
```

### 2. Database Setup
```bash
# Create production database
sudo -u postgres createdb rcm_production

# Set up database user
sudo -u postgres psql
CREATE USER rcm_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE rcm_production TO rcm_user;
\q
```

### 3. Environment Configuration
```bash
# Production environment file
cat > .env.production << EOF
APP_ENV=production
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=postgresql+psycopg://rcm_user:secure_password@db:5432/rcm_production
GOOGLE_API_KEY=your-google-api-key
ALLOW_ORIGINS=https://yourdomain.com
MODEL_NAME=gemini-1.5-pro
EOF
```

### 4. Deployment Commands
```bash
# Deploy with production config
docker-compose -f infra/docker-compose.yml --env-file .env.production up -d

# Run database migrations
docker-compose -f infra/docker-compose.yml exec api alembic upgrade head

# Seed production data
docker-compose -f infra/docker-compose.yml exec api python -m app.rcm.seed
```

## Cloud Deployment Options

### AWS Deployment
```bash
# Using AWS ECS
aws ecs create-cluster --cluster-name rcm-gcc

# Deploy with ECS Compose
ecs-cli compose --file infra/docker-compose.yml up

# Using AWS RDS for database
# Update DATABASE_URL to point to RDS instance
```

### Google Cloud Deployment
```bash
# Using Google Cloud Run
gcloud run deploy rcm-gcc-api --source ./api
gcloud run deploy rcm-gcc-web --source ./web

# Using Cloud SQL for database
# Update DATABASE_URL to point to Cloud SQL instance
```

### Azure Deployment
```bash
# Using Azure Container Instances
az container create --resource-group rcm-gcc --name api --image rcm-gcc-api
az container create --resource-group rcm-gcc --name web --image rcm-gcc-web

# Using Azure Database for PostgreSQL
# Update DATABASE_URL to point to Azure Database
```

## Monitoring and Maintenance

### Health Monitoring
```bash
# Check service health
make health

# Monitor logs
make logs

# Check resource usage
docker stats
```

### Backup and Recovery
```bash
# Database backup
docker-compose exec db pg_dump -U postgres rcm > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres rcm < backup.sql

# Volume backup
docker run --rm -v rcm-gcc_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_data.tar.gz -C /data .
```

### Scaling
```bash
# Scale API services
docker-compose -f infra/docker-compose.yml up -d --scale api=3

# Scale with load balancer
# Configure Nginx or HAProxy for load balancing
```

## Security Considerations

### Environment Security
- Use strong, unique passwords
- Rotate API keys regularly
- Enable firewall rules
- Use HTTPS in production
- Implement rate limiting

### Data Security
- Encrypt data at rest
- Use secure database connections
- Implement access controls
- Regular security audits
- Compliance with HIPAA/GCC regulations

### Network Security
- Use private networks
- Implement VPN access
- Monitor network traffic
- Regular vulnerability scans

## Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check logs
docker-compose logs api

# Check resource usage
docker stats

# Restart services
docker-compose restart
```

#### Database Connection Issues
```bash
# Check database status
docker-compose exec db pg_isready -U postgres

# Check connection string
echo $DATABASE_URL

# Restart database
docker-compose restart db
```

#### AI API Issues
```bash
# Check API key
echo $GOOGLE_API_KEY

# Test API connection
curl -H "Authorization: Bearer $GOOGLE_API_KEY" https://generativelanguage.googleapis.com/v1beta/models
```

### Performance Issues
```bash
# Check resource usage
docker stats

# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# Check database performance
docker-compose exec db psql -U postgres -c "SELECT * FROM pg_stat_activity;"
```

## Support and Maintenance

### Regular Maintenance
- Weekly security updates
- Monthly performance reviews
- Quarterly security audits
- Annual disaster recovery testing

### Support Contacts
- **Technical Support**: dev@humaein.com
- **Emergency Contact**: +234 814 970 0428
- **Documentation**: https://docs.humaein.com/rcm-gcc

### Update Procedures
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
make build
make down
make up

# Run migrations
docker-compose exec api alembic upgrade head
```
