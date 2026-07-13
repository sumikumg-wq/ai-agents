from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    ScriptRequest, ScriptResponse,
    TrendRequest, TrendResponse,
    ResearchRequest, ResearchResponse,
    StoryboardRequest, StoryboardResponse,
    PromptGenRequest, PromptGenResponse,
    ImageRequest, ImageResult,
    VoiceRequest, VoiceResponse,
    SubtitleRequest, SubtitleResponse,
    VideoBuildRequest, VideoBuildResponse,
    ThumbnailRequest, ThumbnailResponse,
    SEORequest, SEOResponse,
    PublishRequest, PublishResponse,
)
from app.agents.script_writer import script_writer_agent
from app.agents.trend_hunter import trend_hunter_agent
from app.agents.research_agent import research_agent
from app.agents.storyboard_generator import storyboard_agent
from app.agents.prompt_generator import prompt_generator_agent
from app.agents.image_manager import image_manager_agent
from app.agents.voice_generator import voice_generator_agent
from app.agents.subtitle_generator import subtitle_generator_agent
from app.agents.video_builder import video_builder_agent
from app.agents.thumbnail_generator import thumbnail_generator_agent
from app.agents.seo_agent import seo_agent
from app.agents.publisher import publisher_agent

router = APIRouter(prefix="/api/agents", tags=["agents"])


def _wrap(fn, *args):
    try:
        return fn(*args)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"{fn.__qualname__} failed: {e}")


@router.post("/research", response_model=ResearchResponse)
def get_research(req: ResearchRequest) -> ResearchResponse:
    return _wrap(research_agent.research, req)


@router.post("/script", response_model=ScriptResponse)
def generate_script(req: ScriptRequest) -> ScriptResponse:
    return _wrap(script_writer_agent.generate, req)


@router.post("/trends", response_model=TrendResponse)
def get_trends(req: TrendRequest) -> TrendResponse:
    return _wrap(trend_hunter_agent.find_trends, req)


@router.post("/storyboard", response_model=StoryboardResponse)
def generate_storyboard(req: StoryboardRequest) -> StoryboardResponse:
    return _wrap(storyboard_agent.generate, req)


@router.post("/prompts", response_model=PromptGenResponse)
def generate_prompts(req: PromptGenRequest) -> PromptGenResponse:
    return _wrap(prompt_generator_agent.generate, req)


@router.post("/image", response_model=ImageResult)
def get_image(req: ImageRequest) -> ImageResult:
    return _wrap(image_manager_agent.get_image, req)


@router.post("/voice", response_model=VoiceResponse)
def generate_voice(req: VoiceRequest) -> VoiceResponse:
    return _wrap(voice_generator_agent.generate, req)


@router.post("/subtitles", response_model=SubtitleResponse)
def generate_subtitles(req: SubtitleRequest) -> SubtitleResponse:
    return _wrap(subtitle_generator_agent.generate, req)


@router.post("/video", response_model=VideoBuildResponse)
def build_video(req: VideoBuildRequest) -> VideoBuildResponse:
    return _wrap(video_builder_agent.build, req)


@router.post("/thumbnail", response_model=ThumbnailResponse)
def generate_thumbnail(req: ThumbnailRequest) -> ThumbnailResponse:
    return _wrap(thumbnail_generator_agent.generate, req)


@router.post("/seo", response_model=SEOResponse)
def generate_seo(req: SEORequest) -> SEOResponse:
    return _wrap(seo_agent.generate, req)


@router.post("/publish", response_model=PublishResponse)
def publish_video(req: PublishRequest) -> PublishResponse:
    return _wrap(publisher_agent.publish, req)
