# Deployment Plan: Epicurean AI 

This plan outlines the steps and configuration changes required to deploy the project with a separated frontend (Vercel) and backend (Railway).

## 1. Prerequisites

- A [Railway](https://railway.app/) account for the backend.
- A [Vercel](https://vercel.com/) account for the frontend.
- Your project pushed to a GitHub repository.

## 2. Configuration Changes to Make

Before deploying, the following files need to be added or modified in the repository:

### `requirements.txt` (Root Directory)
Move the dependencies from `Docs/requirements.txt` to the project root. Railway's default Python builder looks for this file at the root to install dependencies automatically.

### `Procfile` (Root Directory)
Create a `Procfile` in the root to define the startup command for the FastAPI server on Railway:
```
web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

### `frontend/vercel.json` (Vercel Configuration)
Add a Vercel configuration file inside the `frontend` directory to handle proxying API requests to the Railway backend. This proxying approach avoids CORS issues and allows the existing `fetch('/api/recommend')` code in `app.js` to work without any modifications.

```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://<YOUR_RAILWAY_URL>/api/$1"
    }
  ]
}
```
*(The placeholder `<YOUR_RAILWAY_URL>` will be updated with your actual Railway app domain once the backend is deployed.)*

### `src/api/main.py` (Optional Cleanup)
Currently, the FastAPI app mounts the `frontend` folder to serve static files. While this can safely remain, you could remove the static mounting logic in `main.py` since Vercel will handle serving the static frontend files. This makes the backend strictly an API server.

## 3. Deployment Steps

### Step A: Deploy Backend (Railway)
1. Push the configuration changes above to GitHub (`git push`).
2. In Railway, click **New Project** > **Deploy from GitHub repo** and select your repository.
3. Once the service is created, go to the **Variables** tab and add your `GROQ_API_KEY`.
4. Go to the **Settings** tab > **Networking** and click **Generate Domain** to get your public backend URL.
5. Copy this URL (e.g., `https://epicurean-api.up.railway.app`).

### Step B: Deploy Frontend (Vercel)
1. Update `<YOUR_RAILWAY_URL>` in the `frontend/vercel.json` file with the copied Railway domain from Step A, and push this change to GitHub.
2. In Vercel, click **Add New** > **Project** and import your GitHub repository.
3. In the "Configure Project" settings:
   - **Framework Preset:** Leave as `Other` (or auto-detected).
   - **Root Directory:** Edit this and select the `frontend` folder.
4. Click **Deploy**.
5. Once deployment is complete, visit the Vercel URL. Your frontend should now successfully communicate with the Railway backend!
