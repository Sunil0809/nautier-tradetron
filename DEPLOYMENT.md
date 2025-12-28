# Build & Deployment Guide

## Local Development

### 1. Start Database (PostgreSQL)

```bash
# Using Docker (recommended)
docker run --name algo-platform-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=algo_platform \
  -p 5432:5432 \
  -d postgres:15

# Verify
psql postgresql://postgres:postgres@localhost/algo_platform
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Initialize Database

```bash
python -c "from app.database import create_all_tables; create_all_tables()"
```

### 4. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API Docs: http://localhost:8000/docs

## Docker Deployment

### 1. Build Image

```bash
docker build -t algo-platform:latest .
```

### 2. Run Container

```bash
docker run -d \
  --name algo-platform \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e FYERS_APP_ID=... \
  --link algo-platform-db:db \
  algo-platform:latest
```

## Production on Ubuntu VPS

### 1. SSH to Server

```bash
ssh user@your-vps-ip
```

### 2. Install Dependencies

```bash
sudo apt update
sudo apt install -y python3.11 python3-venv postgresql postgresql-contrib nginx
```

### 3. Clone Repo

```bash
git clone https://github.com/your-username/algo-platform.git
cd algo-platform
```

### 4. Setup App

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
sudo nano .env
```

### 6. Setup Systemd Service

```bash
sudo tee /etc/systemd/system/algo-platform.service <<EOF
[Unit]
Description=Algo Trading Platform
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/user/algo-platform
Environment="PATH=/home/user/algo-platform/venv/bin"
ExecStart=/home/user/algo-platform/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable algo-platform
sudo systemctl start algo-platform
```

### 7. Configure Nginx Reverse Proxy

```bash
sudo tee /etc/nginx/sites-available/algo-platform <<EOF
upstream algo_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://algo_api;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/algo-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Setup SSL (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 9. Setup Database

```bash
sudo -u postgres psql
CREATE DATABASE algo_platform;
CREATE USER algo_user WITH PASSWORD 'strong_password';
GRANT ALL ON DATABASE algo_platform TO algo_user;
\q

# Run migrations
python3 -c "from app.database import create_all_tables; create_all_tables()"
```

## CI/CD with GitHub Actions

### 1. Create `.github/workflows/deploy.yml`

```yaml
name: Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to VPS
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /home/user/algo-platform
            git pull origin main
            source venv/bin/activate
            pip install -r requirements.txt
            sudo systemctl restart algo-platform
```

### 2. Add GitHub Secrets

```
VPS_HOST: your-vps-ip
VPS_USER: ubuntu
VPS_SSH_KEY: (your private key)
```

## Monitoring

### View Logs

```bash
# Local
tail -f logs/app.log

# Production
sudo journalctl -u algo-platform -f
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Scaling Considerations

1. **Database**: Use connection pooling (SQLAlchemy pool_size)
2. **Event Queue**: Move to Redis for distributed queues
3. **API**: Use Gunicorn + multiple workers:

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000
```

4. **Broker Connection**: Maintain persistent WebSocket for live data
5. **Alerts**: Use separate async task queue (Celery/RQ)

---

**Next Phase**: Implement CI/CD, monitoring, and scale to 100+ users.
