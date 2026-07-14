# Chronicle AI Studio — Build Roadmap

## Done
- Repo structure: `frontend/`, `backend/`, `docs/`, `.github/workflows/`
- Backend: FastAPI app, config via `.env`, CORS, health check, SQLite persistence
- All 12 agents implemented (`backend/app/agents/`):
  1. Trend Hunter — OpenAI-reasoned topic ideas (MVP; swap in real trend APIs later)
  2. Research Agent — timeline, verified facts vs. speculation, competing theories
  3. Script Writer — hook-driven narration, 4 length presets, optionally grounded in research
  4. Storyboard Generator — splits script into scenes with camera/transition/SFX cues
  5. Prompt Generator — cinematic image/video prompts per scene
  6. Image Manager — AI image generation (OpenAI images) or Wikimedia Commons public-domain fetch
  7. Voice Generator — Edge TTS narration audio
  8. Subtitle Generator — Whisper transcription → synced SRT
  9. Video Builder — FFmpeg slideshow assembly with audio + burned-in subtitles
  10. Thumbnail Generator — Pillow-composed high-CTR thumbnail
  11. SEO Agent — title/description/tags/hashtags/keywords/pinned comment/playlist
  12. Publisher — YouTube Data API upload (draft/private/unlisted/public, thumbnail, scheduling)
- Auth: JWT-based register/login (`backend/app/core/auth.py`, `routers/auth.py`) —
  swap-in point for Firebase/Supabase noted in the module docstring
- Persistence: SQLAlchemy `User` and `Project` models, `/api/projects` CRUD
- Frontend: dark glassmorphism theme, sidebar nav, Dashboard, Create Video
  (wired to Script Writer), Library (wired to real `/api/projects` data),
  Login/Register pages, protected routing
- CI: GitHub Actions workflow — backend compile check, frontend build check
- Docker: backend + frontend Dockerfiles, docker-compose

## Still ahead
1. **Full pipeline orchestration**: one endpoint/UI flow that chains all 12
   agents end-to-end per the workflow diagram (Topic → Trend → Research →
   Script → Storyboard → Prompts → Images → Voice → Subtitles → Video →
   Thumbnail → SEO → Human Approval → Upload), persisting progress to the
   `Project` row at each stage.
2. **Human approval step**: UI gate before Publisher is called.
3. **Analytics page**: pull real stats from the YouTube Data API (views,
   watch time, retention) instead of the current placeholder.
4. **Settings page**: UI for OpenAI/YouTube keys, voice, output resolution,
   subtitle preferences (currently only set via `.env`).
5. **Multi-platform export**: Instagram Reels/TikTok/Facebook/LinkedIn/
   Pinterest/X/Threads variants (spec's "Future Features" section).
6. **n8n automation hooks** for scheduling/triggering runs.
7. Swap JWT auth for Firebase Auth or Supabase Auth if preferred.
8. Move image/audio/video artifacts from local `generated/` to cloud storage
   (S3/GCS) before this goes to production — local disk won't survive a
   redeploy.

## Notes
- Every agent keeps the same shape: a class with a lazily-constructed OpenAI
  (or other) client, a typed request/response via `app/models/schemas.py`,
  and a router entry in `app/routers/agents.py`.
- Secrets stay in `.env` (gitignored); `.env.example` documents every key,
  including `JWT_SECRET_KEY` and the YouTube OAuth trio.
- `google-api-python-client` needs a real Google Cloud OAuth app with the
  YouTube Data API enabled — the Publisher agent will raise a clear
  `RuntimeError` until `YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN` are set.
