# Quick Deployment Guide (Easiest Free Option)

This is the fastest way to deploy your app for free using Vercel + Render.

## Prerequisites
- GitHub account
- Vercel account (free) - https://vercel.com
- Render account (free) - https://render.com

## Step 1: Push to GitHub

```bash
cd c:\Users\decub\OneDrive\Desktop\Imgtodesmos
git init
git add .
git commit -m "Initial commit - Image to Desmos app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/imgtodesmos.git
git push -u origin main
```

## Step 2: Deploy Backend to Render

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render will detect the `render.yaml` configuration
5. Click **"Create Web Service"**
6. Wait for deployment (5-10 minutes)
7. **Copy your backend URL** (e.g., `https://imgtodesmos-backend.onrender.com`)

### Important Notes:
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- You need to install Potrace on Render - add this to your render.yaml if needed

## Step 3: Deploy Frontend to Vercel

### Option A: Using Vercel Dashboard (Easiest)

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. **Configure Project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. **Add Environment Variable:**
   - Key: `VITE_API_URL`
   - Value: `https://imgtodesmos-backend.onrender.com` (your Render URL)
5. Click **"Deploy"**
6. Wait 2-3 minutes
7. Done! Your app is live at `https://your-app.vercel.app`

### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (choose your account)
# - Link to existing project? No
# - What's your project's name? imgtodesmos
# - In which directory is your code located? ./
# - Want to override settings? Yes
# - Build Command: npm run build
# - Output Directory: dist
# - Development Command: npm run dev

# Set environment variable
vercel env add VITE_API_URL production
# Paste your Render backend URL when prompted

# Redeploy with env vars
vercel --prod
```

## Step 4: Update Backend CORS

Once you have your Vercel URL, update the backend environment variables on Render:

1. Go to your Render dashboard
2. Select your backend service
3. Go to **Environment** tab
4. Add variable:
   - Key: `ALLOWED_ORIGINS`
   - Value: `https://your-app.vercel.app`
5. Click **Save Changes**
6. Service will redeploy automatically

## Step 5: Test Your Deployment

1. Visit your Vercel URL
2. Upload an image
3. Wait for processing (first request may be slow if backend was sleeping)
4. Copy equations to Desmos!

## Troubleshooting

### Backend returns 500 error
- Check Render logs for errors
- Make sure Potrace is installed (see render.yaml)
- Verify all Python dependencies are in requirements.txt

### CORS errors
- Make sure ALLOWED_ORIGINS is set correctly on Render
- Check that VITE_API_URL points to your Render backend

### Frontend can't reach backend
- Verify VITE_API_URL environment variable on Vercel
- Check backend is running on Render
- Try visiting the backend health endpoint: `https://your-backend.onrender.com/api/health`

### Backend is slow
- Free tier sleeps after 15 minutes
- First request wakes it up (takes ~30 seconds)
- Consider upgrading to paid tier ($7/month) for always-on

## Your URLs

After deployment, save these:
- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://imgtodesmos-backend.onrender.com`
- **Backend Health:** `https://imgtodesmos-backend.onrender.com/api/health`

## Cost

- **Vercel Frontend:** FREE (unlimited hobby projects)
- **Render Backend:** FREE (sleeps after 15min inactivity)
- **Total:** $0/month

## Upgrade Options

If you need better performance:
- **Render Paid:** $7/month (always-on, no sleep)
- **Vercel Pro:** $20/month (better analytics, more bandwidth)

---

## Alternative: Deploy Both to Render

If you prefer one platform:

1. Deploy backend as shown above
2. Add a second service for frontend:
   - Type: Static Site
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`
   - Add env var: `VITE_API_URL=https://your-backend.onrender.com`

Both services free tier!

---

**That's it! Your app is now live and accessible worldwide!** 🚀
