from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import agents

app = FastAPI(
    title=settings.app_name,
    description="AI-powered faceless YouTube video generation platform "
                 "for the History & Mystery niche.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}
