# Quick Deployment Guide

## 🚀 Fastest Way to Deploy (Using DigitalOcean)

### Step 1: Create a Droplet
1. Sign up for [DigitalOcean](https://www.digitalocean.com/) (get $200 credit with referral)
2. Create a new Droplet:
   - Choose Ubuntu 22.04 LTS
   - Select at least 4GB RAM / 2 vCPUs ($24/month)
   - Add your SSH key
   - Choose a datacenter near your users

### Step 2: Initial Server Setup
```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Install git
apt install git -y
```

### Step 3: Deploy the Application
```bash
# Clone the repository
git clone https://github.com/NJersyHiro/ai-career-discovery-assistant.git
cd ai-career-discovery-assistant

# Copy and configure environment
cp .env.production.example .env.production
nano .env.production  # Edit with your values

# IMPORTANT: Add your Gemini API key
# Get it from: https://makersuite.google.com/app/apikey

# Run deployment script
./deploy.sh
```

### Step 4: Set Up Domain (Optional)
1. Buy a domain (Namecheap, Google Domains, etc.)
2. Point it to your server IP:
   - Add A record: `@` → `your-server-ip`
   - Add A record: `www` → `your-server-ip`

### Step 5: Enable HTTPS with Let's Encrypt
```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 🎯 Alternative: One-Click Deployments

### Option 1: Railway (Easiest)
1. Fork the repository
2. Sign up for [Railway](https://railway.app/)
3. Create new project from GitHub
4. Add environment variables
5. Deploy!

### Option 2: Render
1. Fork the repository
2. Sign up for [Render](https://render.com/)
3. Create:
   - Web Service (Backend)
   - Static Site (Frontend)
   - PostgreSQL database
   - Redis instance
4. Configure environment variables
5. Deploy!

### Option 3: Heroku
1. Fork the repository
2. Create Heroku account
3. Create new app
4. Add buildpacks:
   - heroku/nodejs
   - heroku/python
5. Add add-ons:
   - Heroku Postgres
   - Heroku Redis
6. Configure and deploy

## 💰 Cost Estimates

### Small Scale (< 100 users/day)
- **DigitalOcean Droplet**: $24/month
- **Domain**: $12/year
- **Total**: ~$25/month

### Medium Scale (100-1000 users/day)
- **DigitalOcean Droplet**: $48/month (8GB RAM)
- **Managed Database**: $15/month
- **CDN**: $10/month
- **Total**: ~$75/month

### Large Scale (1000+ users/day)
- **Multiple servers**: $200+/month
- **Load balancer**: $10/month
- **Managed services**: $100+/month
- **Total**: ~$300+/month

## 🔧 Post-Deployment Checklist

- [ ] Test user registration and login
- [ ] Upload a test PDF and verify analysis works
- [ ] Check that Celery workers are processing tasks
- [ ] Verify email notifications (if configured)
- [ ] Set up monitoring (UptimeRobot is free)
- [ ] Configure backups
- [ ] Review security settings

## 🆘 Troubleshooting

### Application not accessible
```bash
# Check if services are running
docker compose -f docker-compose.prod.yml ps

# Check logs
docker compose -f docker-compose.prod.yml logs
```

### Database connection issues
```bash
# Check database is running
docker compose -f docker-compose.prod.yml logs db

# Test connection
docker compose -f docker-compose.prod.yml exec backend python -c "from app.core.database import engine; print('DB connected!')"
```

### Celery not processing tasks
```bash
# Check Celery logs
docker compose -f docker-compose.prod.yml logs celery-worker

# Restart Celery
docker compose -f docker-compose.prod.yml restart celery-worker
```

## 📞 Need Help?

1. Check the logs: `docker compose -f docker-compose.prod.yml logs`
2. Review DEPLOYMENT.md for detailed instructions
3. Open an issue on GitHub