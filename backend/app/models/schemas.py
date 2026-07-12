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
