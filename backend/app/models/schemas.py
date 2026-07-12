from typing import Literal
from pydantic import BaseModel, Field

VideoLength = Literal["30s", "60s", "5min", "10min"]


class ScriptRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="History/Mystery topic")
    length: VideoLength = "60s"
    language: str = "English"
    tone: str = "Netflix documentary, curiosity-driven"


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
