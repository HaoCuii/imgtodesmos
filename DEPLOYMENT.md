# Deployment Guide

This guide covers multiple deployment options for your Image to Desmos application.

## Deployment Options

1. **Vercel (Frontend) + Render/Railway (Backend)** - Easiest, Free tier available
2. **Heroku** - Simple, all-in-one deployment
3. **DigitalOcean/AWS/GCP** - Full control, VPS deployment
4. **Docker** - Containerized deployment (any platform)

---

## Option 1: Vercel + Render (Recommended - Free)

### Backend Deployment (Render.com)

1. **Create a `render.yaml` in the project root:**
   ```yaml
   services:
     - type: web
       name: imgtodesmos-backend
       env: python
       buildCommand: "cd backend && pip install -r requirements.txt"
       startCommand: "cd backend && gunicorn app:app"
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0
   ```

2. **Add Gunicorn to backend requirements:**
   ```bash
   cd backend
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

3. **Update `backend/app.py` for production:**
   - Change the last lines from:
     ```python
     if __name__ == '__main__':
         app.run(debug=True, port=5000)
     ```
   - To:
     ```python
     if __name__ == '__main__':
         app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
     ```

4. **Deploy to Render:**
   - Push your code to GitHub
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the render.yaml
   - Click "Create Web Service"
   - Copy the backend URL (e.g., `https://imgtodesmos-backend.onrender.com`)

### Frontend Deployment (Vercel)

1. **Update API URL in frontend:**
   Create `frontend/.env.production`:
   ```
   VITE_API_URL=https://imgtodesmos-backend.onrender.com
   ```

2. **Update `frontend/src/components/ImageUploader.tsx`:**
   Replace the hardcoded URL:
   ```typescript
   const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
   const response = await axios.post(`${apiUrl}/api/process-image`, formData, {
   ```

3. **Deploy to Vercel:**
   ```bash
   # Install Vercel CLI
   npm install -g vercel

   # Deploy
   cd frontend
   vercel
   ```

   Or use the Vercel website:
   - Go to https://vercel.com
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Deploy!

---

## Option 2: Railway (Full Stack - Free Tier)

1. **Create `railway.json` in project root:**
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "cd backend && gunicorn app:app",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

2. **Add `Procfile` in backend:**
   ```
   web: gunicorn app:app
   ```

3. **Deploy:**
   - Push to GitHub
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-deploy both frontend and backend

---

## Option 3: Docker Deployment

### Create Dockerfiles

**backend/Dockerfile:**
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    potrace \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**frontend/Dockerfile:**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**frontend/nginx.conf:**
```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**docker-compose.yml (project root):**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/output:/app/output

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://localhost:5000
```

**Deploy with Docker:**
```bash
# Build and run
docker-compose up -d

# Access at http://localhost
```

---

## Option 4: DigitalOcean App Platform

1. **Push code to GitHub**

2. **Create `app.yaml` in project root:**
   ```yaml
   name: imgtodesmos
   services:
     - name: backend
       github:
         repo: your-username/imgtodesmos
         branch: main
         deploy_on_push: true
       source_dir: backend
       build_command: pip install -r requirements.txt
       run_command: gunicorn app:app
       http_port: 5000
       environment_slug: python
       envs:
         - key: PYTHON_VERSION
           value: "3.11"

     - name: frontend
       github:
         repo: your-username/imgtodesmos
         branch: main
         deploy_on_push: true
       source_dir: frontend
       build_command: npm install && npm run build
       run_command: npm run preview
       http_port: 4173
       environment_slug: node-js
   ```

3. **Deploy:**
   - Go to https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Connect GitHub repository
   - DigitalOcean will auto-detect the config
   - Click "Deploy"

---

## Option 5: Traditional VPS (Ubuntu)

### SSH into your server and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip nodejs npm nginx potrace

# Clone your repository
git clone https://github.com/your-username/imgtodesmos.git
cd imgtodesmos

# Setup backend
cd backend
pip3 install -r requirements.txt
pip3 install gunicorn

# Setup frontend
cd ../frontend
npm install
npm run build

# Configure Nginx
sudo nano /etc/nginx/sites-available/imgtodesmos
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/imgtodesmos/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/imgtodesmos /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup systemd service for backend
sudo nano /etc/systemd/system/imgtodesmos-backend.service
```

**Systemd service:**
```ini
[Unit]
Description=Image to Desmos Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/imgtodesmos/backend
ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl enable imgtodesmos-backend
sudo systemctl start imgtodesmos-backend
```

---

## Important Production Changes

### 1. Environment Variables

Create `.env` files:

**backend/.env:**
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_UPLOAD_SIZE=10485760
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

**frontend/.env.production:**
```
VITE_API_URL=https://your-backend-domain.com
```

### 2. Update backend/app.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_SIZE', 16 * 1024 * 1024))

CORS(app, origins=os.getenv('ALLOWED_ORIGINS', '*').split(','))
```

### 3. Install python-dotenv

```bash
cd backend
pip install python-dotenv
echo "python-dotenv==1.0.0" >> requirements.txt
```

### 4. Update CORS for production

Make sure your backend only accepts requests from your frontend domain.

---

## Cost Comparison

| Platform | Frontend | Backend | Total/Month |
|----------|----------|---------|-------------|
| Vercel + Render | Free | Free* | $0 |
| Railway | Free* | Free* | $0-5 |
| Heroku | $7 | $7 | $14 |
| DigitalOcean | $5 | $5 | $10 |
| AWS (t2.micro) | $3 | $8 | $11 |
| VPS (DigitalOcean) | Included | Included | $6 |

*Free tiers have limitations (sleep after inactivity, limited hours, etc.)

---

## Recommended Stack for Beginners

**Best Free Option:**
- Frontend: **Vercel** (unlimited free hobby projects)
- Backend: **Render** (free tier, sleeps after 15min inactivity)

**Best Paid Option ($6/month):**
- **DigitalOcean Droplet** (Full VPS control, both services on one server)

---

## Post-Deployment Checklist

- [ ] Backend URL is accessible
- [ ] Frontend can reach backend API
- [ ] CORS is configured correctly
- [ ] File uploads work
- [ ] Environment variables are set
- [ ] SSL/HTTPS is enabled (use Let's Encrypt)
- [ ] Error logging is configured
- [ ] Set up monitoring (UptimeRobot, etc.)

---

## Need Help?

- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Docker Docs: https://docs.docker.com

