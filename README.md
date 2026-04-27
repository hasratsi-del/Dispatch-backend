# DISPATCH.
### Real-time geopolitical intelligence engine

> *"The world is talking. This is what it's saying."*

**Live:** [hasratsii.netlify.app](https://hasratsii.netlify.app)

---

## What it does

Fetches live global news → scores sentiment using NLP → aggregates by country → renders on an interactive D3.js world map with a rotating Three.js globe.

```
NewsAPI (live headlines)
        ↓
Flask backend
  — TextBlob sentiment scoring (-1.0 to +1.0)
  — keyword country detection (100+ mappings)
  — 5-minute cache
  — /api/sentiment endpoint
        ↓
D3.js + Three.js frontend
  — rotating globe with live sentiment dots
  — three map modes: Sentiment / Heat / Volume
  — AI situation report
  — country search + map highlight
  — clickable article headlines
```

---

## Deployment history

### Phase 1 — Local (localhost)

The first version ran entirely on a local Mac. Flask served the API at `localhost:5000`. This meant:
- Only worked when the terminal was open
- Only accessible from the developer's machine
- `localhost` in the browser means *your* computer — nobody else could reach it

**Repo:** [github.com/hasratsi-del/DISPATCH.](https://github.com/hasratsi-del/DISPATCH.)

### Phase 2 — Railway (production, always-on)

The backend now runs on Railway's servers 24/7. Anyone in the world can visit the site and get live data — no terminal needs to be open, no Mac needs to be on.

```
Before:  Visitor → your Mac (must be on, terminal open)
After:   Visitor → Railway servers (always on, globally available)
```

**Repo:** [github.com/hasratsi-del/dispatch-backend](https://github.com/hasratsi-del/dispatch-backend)  
**Live backend:** [dispatch-backend-production-c0e6.up.railway.app](https://dispatch-backend-production-c0e6.up.railway.app)

---

## Run locally (development)

### First time setup — run once, never again

```bash
cd ~/Downloads/dispatch-project/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Every time you want to run it

```bash
cd ~/Downloads/dispatch-project/backend
source .venv/bin/activate
export NEWS_API_KEY=your_key_here
python app.py
```

Your terminal should show:

```
* Serving Flask app 'app'
* Debug mode: off
WARNING: This is a development server...
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://172.20.10.4:5000
Press CTRL+C to quit
```

Then open a new terminal tab and run:

```bash
open ~/Downloads/dispatch-project/frontend/index.html
```

**To stop:** Press `Ctrl+C` in the backend terminal.

### After restarting your Mac

The `.venv` folder is permanent — you never reinstall packages. Just run the four commands above.

---

## Deploy

### Backend → Railway
1. Push `backend/` to GitHub (root level, no subfolders)
2. Connect to [railway.app](https://railway.app) → Deploy from GitHub
3. Add `NEWS_API_KEY` in Railway → Variables tab
4. Settings → Networking → Generate Domain
5. Copy the URL

### Frontend → Netlify
1. In `frontend/index.html` replace `YOUR-RAILWAY-URL` with your Railway URL
2. Drag `frontend/` folder onto [netlify.app](https://netlify.app)

---

## Features

| Feature | Description |
|---|---|
| **Sentiment map** | Countries colored by news sentiment |
| **Heat mode** | Most extreme countries highlighted with signal bars |
| **Volume mode** | Which countries dominate news coverage |
| **◈ AI Report** | Global tone, stress zones, stable zones |
| **Country search** | Find any country, highlights on map |
| **Live globe** | Three.js rotating globe with pulsing data points |
| **Article links** | Real clickable headlines per country |

---

## Stack

| | |
|---|---|
| Backend | Python · Flask · TextBlob · Gunicorn |
| Data | NewsAPI |
| Frontend | D3.js v7 · Three.js r128 · Vanilla JS |
| Hosting | Railway (backend) · Netlify (frontend) |
| Cost | **$0** |

---

## Push to GitHub

```bash
git init
git add .
git commit -m "feat: DISPATCH geopolitical intelligence engine"
git branch -M main
git remote add origin https://github.com/hasratsi-del/DISPATCH..git
git push -u origin main
```


