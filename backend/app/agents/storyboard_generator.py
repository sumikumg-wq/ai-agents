"""
Agent 4: Storyboard Generator
Splits a finished script into scenes with narration, visual description,
camera work, transitions, and audio cues — ready for Agent 5 (Prompt Gen).
"""
import json
from openai import OpenAI
from app.core.config import settings
from app.models.schemas import StoryboardRequest, StoryboardResponse

_SYSTEM_PROMPT = """You are a documentary storyboard artist. Split the given \
narration script into scenes suitable for a faceless History & Mystery \
YouTube video. Each scene should cover a natural narration beat (roughly \
5-15 seconds of spoken narration).

Respond ONLY with a JSON object: {"scenes": [ ... ]} where each scene has:
- scene_number (int, starting at 1)
- duration_seconds (int estimate)
- narration (the exact narration text for this scene, verbatim from the script)
- visual_description (what should be shown on screen — cinematic, historically inspired)
- camera_angle (e.g. "wide establishing shot", "close-up")
- camera_motion (e.g. "slow push-in", "static", "pan left")
- transition (e.g. "hard cut", "cross-dissolve", "fade to black")
- sound_effects (e.g. "wind ambience", "distant thunder", "none")
- music_suggestion (mood/style, e.g. "low tense strings")

No prose outside the JSON. No markdown fences.
"""


class StoryboardGeneratorAgent:
    def __init__(self) -> None:
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            if not settings.openai_api_key:
                raise RuntimeError("OPENAI_API_KEY is not set. Add it to backend/.env")
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def generate(self, req: StoryboardRequest) -> StoryboardResponse:
        completion = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Topic: {req.topic}\n\nScript:\n{req.script}"},
            ],
            temperature=0.6,
        )
        raw = completion.choices[0].message.content.strip()
        parsed = json.loads(raw)
        return StoryboardResponse(topic=req.topic, scenes=parsed.get("scenes", []))


storyboard_agent = StoryboardGeneratorAgent()
