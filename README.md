# Chronicle AI Studio

AI-powered SaaS platform that generates faceless History & Mystery
documentary videos for YouTube (and future platforms).

See `docs/ROADMAP.md` for build order and what's implemented vs. pending.

## Stack
- Frontend: React 19 + Vite + Tailwind + React Router + Framer Motion
- Backend: FastAPI + SQLAlchemy + SQLite (Postgres-ready)
- AI: OpenAI, modular agent architecture (`backend/app/agents/`)

## Local setup

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then fill in OPENAI_API_KEY
uvicorn app.main:app --reload
```
Backend runs at http://localhost:8000 — docs at http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:5173 and proxies `/api` to the backend.

### Or with Docker
```bash
docker compose up --build
```

## What works right now
- `POST /api/agents/script` — generates a documentary narration script
  (30s/60s/5min/10min) for a given topic.
- `POST /api/agents/trends` — suggests History & Mystery video topics.
- Dashboard + Create Video pages in the frontend, Create Video is wired
  live to the script agent.

## What's next
See `docs/ROADMAP.md`.
