"""
Agent 8: Subtitle Generator
Transcribes narration audio via OpenAI's Whisper API and exports an SRT
file, synchronized to the actual generated speech.
"""
import os
from openai import OpenAI
from app.core.config import settings
from app.models.schemas import SubtitleRequest, SubtitleResponse

_OUTPUT_ROOT = "generated"


class SubtitleGeneratorAgent:
    def __init__(self) -> None:
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            if not settings.openai_api_key:
                raise RuntimeError("OPENAI_API_KEY is not set. Add it to backend/.env")
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def _project_dir(self, project_id: str) -> str:
        path = os.path.join(_OUTPUT_ROOT, project_id, "subtitles")
        os.makedirs(path, exist_ok=True)
        return path

    def generate(self, req: SubtitleRequest) -> SubtitleResponse:
        if not os.path.exists(req.audio_path):
            raise RuntimeError(f"Audio file not found: {req.audio_path}")

        with open(req.audio_path, "rb") as audio_file:
            srt_text = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="srt",
            )

        out_dir = self._project_dir(req.project_id)
        srt_path = os.path.join(out_dir, "narration.srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_text if isinstance(srt_text, str) else str(srt_text))

        segment_count = srt_text.count("-->") if isinstance(srt_text, str) else 0

        return SubtitleResponse(srt_path=srt_path, segment_count=segment_count)


subtitle_generator_agent = SubtitleGeneratorAgent()
