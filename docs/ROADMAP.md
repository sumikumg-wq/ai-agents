# Chronicle AI Studio — Build Roadmap

## Done (this scaffold)
- Repo structure: `frontend/`, `backend/`, `docs/`
- Backend: FastAPI app, config via `.env`, CORS, health check
- Agent 1 — Trend Hunter (MVP via OpenAI reasoning; swap for real trend APIs later)
- Agent 3 — Script Writer (fully working, calls OpenAI, 4 length presets)
- Frontend: dark glassmorphism theme, sidebar nav, Dashboard, Create Video
  (wired live to the Script Writer agent), placeholder pages for
  Library/Analytics/Uploads/Settings
- Docker: backend + frontend Dockerfiles, docker-compose

## Next, in dependency order
1. **Agent 2 — Research Agent**: fact/timeline/sources retrieval, feeds Script Writer.
2. **Agent 4 — Storyboard Generator**: splits a script into scenes
   (narration, visual description, camera, transitions, SFX/music cues).
3. **Agent 5 — Prompt Generator**: turns each scene into cinematic
   image/video-gen prompts.
4. **Agent 6 — Image Manager**: AI image generation + public-domain asset
   fetch (Wikimedia, LoC, Internet Archive, National Archives).
5. **Agent 7 — Voice Generator**: Edge TTS integration (free), optional
   ElevenLabs.
6. **Agent 8 — Subtitle Generator**: Whisper-based SRT + burn-in.
7. **Agent 9 — Video Builder**: FFmpeg assembly (voice + images + captions + music → MP4).
8. **Agent 10 — Thumbnail Generator**: high-CTR thumbnail composition.
9. **Agent 11 — SEO Agent**: title/description/tags/hashtags/pinned comment.
10. **Agent 12 — Publisher**: YouTube Data API upload (draft/private/scheduled/public).
11. **Auth**: Firebase or Supabase auth on both frontend and backend.
12. **Persistence**: SQLAlchemy models + migrations for projects/videos
    (currently no DB models exist yet — needed before Library page is real).
13. **Library / Analytics / Uploads / Settings pages**: wire to real data
    once persistence + agents above exist.
14. **CI/CD**: GitHub Actions to build/test/push Docker images.

## Notes
- Every agent should keep the same shape as `script_writer.py`: a class with
  a lazily-constructed OpenAI client, a typed request/response via
  `app/models/schemas.py`, and a router entry in `app/routers/agents.py`.
- Keep secrets out of git — `.env` is gitignored, `.env.example` documents
  required keys.
