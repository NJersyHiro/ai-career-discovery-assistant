# AI Career Discovery Assistant - Deployment Guide

This guide will help you deploy the AI Career Discovery Assistant to production.

## Prerequisites

- Domain name (optional but recommended)
- Cloud provider account (AWS, Google Cloud, or Azure)
- Gemini API key
- SSL certificate (Let's Encrypt recommended)

## Deployment Options

### Option 1: Docker Compose on VPS (Simplest)

Perfect for: Small to medium traffic, single server deployment

1. **Get a VPS** (DigitalOcean, Linode, AWS EC2, etc.)
   - Recommended: 4GB RAM, 2 vCPUs minimum
   - Ubuntu 22.04 LTS

2. **Install Docker and Docker Compose**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo apt install docker-compose-plugin
   ```

3. **Clone your repository**
   ```bash
   git clone https://github.com/NJersyHiro/ai-career-discovery-assistant.git
   cd ai-career-discovery-assistant
   ```

4. **Create production environment file**
   ```bash
   cp .env.example .env.production
   ```

5. **Configure production settings**
   Edit `.env.production`:
   ```env
   # Backend
   BACKEND_CORS_ORIGINS=["https://your-domain.com"]
   SECRET_KEY=your-very-secure-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key
   DATABASE_URL=postgresql://postgres:your-secure-password@db:5432/career_assistant
   
   # Frontend
   VITE_API_URL=https://your-domain.com/api
   
   # Security
   POSTGRES_PASSWORD=your-secure-password
   JWT_SECRET_KEY=your-jwt-secret-key
   ```

6. **Set up Nginx as reverse proxy**
   Create `nginx.conf`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl;
       server_name your-domain.com;
       
       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. **Deploy with Docker Compose**
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```

### Option 2: Kubernetes Deployment (Scalable)

Perfect for: High traffic, auto-scaling needs

1. **Create Kubernetes manifests** (I can help create these)
2. **Use managed Kubernetes** (EKS, GKE, AKS)
3. **Deploy with Helm charts**

### Option 3: Serverless/Managed Services

Perfect for: Low maintenance, auto-scaling

**Frontend**: Vercel or Netlify
**Backend**: AWS Lambda + API Gateway or Google Cloud Run
**Database**: AWS RDS or Google Cloud SQL
**Storage**: AWS S3 or Google Cloud Storage
**Queue**: AWS SQS or Google Cloud Tasks

## Production Checklist

### Security
- [ ] Change all default passwords
- [ ] Generate secure SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Remove debug mode
- [ ] Secure MinIO/S3 buckets

### Database
- [ ] Use managed database service (recommended)
- [ ] Set up regular backups
- [ ] Configure connection pooling
- [ ] Run migrations: `alembic upgrade head`

### Performance
- [ ] Enable Redis caching
- [ ] Configure CDN for static files
- [ ] Optimize Docker images
- [ ] Set up monitoring (Prometheus, Grafana)

### Environment Variables
- [ ] GEMINI_API_KEY
- [ ] DATABASE_URL
- [ ] REDIS_URL
- [ ] SECRET_KEY
- [ ] JWT_SECRET_KEY
- [ ] AWS credentials (for S3)

## Quick Start Scripts

### 1. Production Docker Compose
Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "3000:80"
    environment:
      - VITE_API_URL=https://your-domain.com/api
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    depends_on:
      - db
      - redis
      - minio

  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    command: celery -A app.workers.celery_app worker --loglevel=info
    env_file:
      - .env.production
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: career_assistant
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${AWS_ACCESS_KEY_ID}
      MINIO_ROOT_PASSWORD: ${AWS_SECRET_ACCESS_KEY}
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  minio_data:
```

### 2. Frontend Production Dockerfile
Create `frontend/Dockerfile.prod`:

```dockerfile
# Build stage
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### 3. Backend Production Dockerfile
Create `backend/Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run with gunicorn
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "4"]
```

## Monitoring & Maintenance

1. **Set up monitoring**
   - Application metrics (Prometheus + Grafana)
   - Error tracking (Sentry)
   - Uptime monitoring (UptimeRobot)

2. **Backup strategy**
   - Daily database backups
   - Document storage backups
   - Configuration backups

3. **Logging**
   - Centralized logging (ELK stack or CloudWatch)
   - Log rotation policies

## Cost Optimization Tips

1. **Start small**
   - Single VPS with Docker Compose
   - Upgrade as traffic grows

2. **Use managed services wisely**
   - Managed database only if needed
   - CDN for static assets

3. **Monitor usage**
   - Set up billing alerts
   - Use auto-scaling with limits

## Support & Troubleshooting

Common issues and solutions will be added here based on deployment experiences.