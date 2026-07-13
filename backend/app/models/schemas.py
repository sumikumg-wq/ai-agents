from typing import Literal
from pydantic import BaseModel, Field

VideoLength = Literal["30s", "60s", "5min", "10min"]


class ScriptRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="History/Mystery topic")
    length: VideoLength = "60s"
    language: str = "English"
    tone: str = "Netflix documentary, curiosity-driven"
    research_notes: str | None = Field(
        default=None,
        description="Optional condensed research output (from Agent 2) to "
                     "ground the script in verified facts.",
    )


class ScriptResponse(BaseModel):
    topic: str
    length: VideoLength
    hook: str
    script: str
    estimated_word_count: int


class TrendRequest(BaseModel):
    niche: str = "History & Mystery"
    count: int = 5


class TrendItem(BaseModel):
    title: str
    search_intent: str
    competition: Literal["low", "medium", "high"]
    estimated_ctr: str
    evergreen_score: int = Field(ge=1, le=10)


class TrendResponse(BaseModel):
    items: list[TrendItem]


class ResearchRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="History/Mystery topic")
    depth: Literal["brief", "standard", "deep"] = "standard"


class TimelineEvent(BaseModel):
    date: str
    event: str


class ResearchFact(BaseModel):
    statement: str
    verified: bool
    source: str


class CompetingTheory(BaseModel):
    theory: str
    supporting_evidence: str
    credibility: Literal["low", "medium", "high"]


class ResearchResponse(BaseModel):
    topic: str
    timeline: list[TimelineEvent]
    verified_facts: list[ResearchFact]
    speculative_claims: list[ResearchFact]
    competing_theories: list[CompetingTheory]
    primary_sources: list[str]


# --- Agent 4: Storyboard ---

class StoryboardRequest(BaseModel):
    script: str = Field(..., min_length=10)
    topic: str = "Untitled"


class Scene(BaseModel):
    scene_number: int
    duration_seconds: int
    narration: str
    visual_description: str
    camera_angle: str
    camera_motion: str
    transition: str
    sound_effects: str
    music_suggestion: str


class StoryboardResponse(BaseModel):
    topic: str
    scenes: list[Scene]


# --- Agent 5: Prompt Generator ---

class PromptGenRequest(BaseModel):
    scenes: list[Scene]


class ScenePrompt(BaseModel):
    scene_number: int
    image_prompt: str
    video_prompt: str


class PromptGenResponse(BaseModel):
    prompts: list[ScenePrompt]


# --- Agent 6: Image Manager ---

class ImageRequest(BaseModel):
    scene_number: int
    prompt: str
    prefer_public_domain: bool = True
    project_id: str = "default"


class ImageResult(BaseModel):
    scene_number: int
    source: Literal["ai_generated", "public_domain", "failed"]
    path_or_url: str
    attribution: str | None = None


class ImageResponse(BaseModel):
    results: list[ImageResult]


# --- Agent 7: Voice Generator ---

class VoiceRequest(BaseModel):
    text: str = Field(..., min_length=1)
    voice: str = "en-US-GuyNeural"
    project_id: str = "default"
    filename: str = "narration.mp3"


class VoiceResponse(BaseModel):
    audio_path: str
    voice: str
    characters: int


# --- Agent 8: Subtitles ---

class SubtitleRequest(BaseModel):
    audio_path: str
    project_id: str = "default"


class SubtitleResponse(BaseModel):
    srt_path: str
    segment_count: int


# --- Agent 9: Video Builder ---

class VideoBuildRequest(BaseModel):
    project_id: str = "default"
    audio_path: str
    image_paths: list[str]
    srt_path: str | None = None
    resolution: str = "1080x1920"


class VideoBuildResponse(BaseModel):
    video_path: str


# --- Agent 10: Thumbnail ---

class ThumbnailRequest(BaseModel):
    project_id: str = "default"
    title_text: str
    background_image_path: str | None = None


class ThumbnailResponse(BaseModel):
    thumbnail_path: str


# --- Agent 11: SEO ---

class SEORequest(BaseModel):
    topic: str
    script: str


class SEOResponse(BaseModel):
    title: str
    description: str
    tags: list[str]
    hashtags: list[str]
    keywords: list[str]
    pinned_comment: str
    playlist_suggestion: str


# --- Agent 12: Publisher ---

class PublishRequest(BaseModel):
    video_path: str
    thumbnail_path: str | None = None
    title: str
    description: str
    tags: list[str] = []
    privacy_status: Literal["private", "public", "unlisted"] = "private"
    scheduled_at: str | None = None


class PublishResponse(BaseModel):
    youtube_video_id: str
    youtube_url: str
    privacy_status: str


# --- Projects / persistence ---

class ProjectCreate(BaseModel):
    topic: str
    target_length: VideoLength = "60s"


class ProjectOut(BaseModel):
    id: int
    topic: str
    target_length: str
    status: str
    youtube_url: str | None = None

    class Config:
        from_attributes = True


# --- Auth ---

class UserRegister(BaseModel):
    email: str
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
