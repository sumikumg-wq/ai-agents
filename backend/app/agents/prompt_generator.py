"""
Agent 5: Prompt Generator
Converts each storyboard scene into cinematic prompts suitable for AI image
and AI video generation models.
"""
import json
from openai import OpenAI
from app.core.config import settings
from app.models.schemas import PromptGenRequest, PromptGenResponse

_SYSTEM_PROMPT = """You write prompts for AI image and AI video generation \
models (e.g. Midjourney/SDXL style for images, Runway/Pika style for video). \
Prompts must be cinematic, realistic, historically inspired, and suitable \
for documentary storytelling — no text-in-image requests, no modern \
anachronisms unless the scene calls for it.

Respond ONLY with a JSON object: {"prompts": [ ... ]} where each entry has:
- scene_number (int, matching the input scene)
- image_prompt (single descriptive prompt string)
- video_prompt (single descriptive prompt string, including implied camera motion)

No prose outside the JSON. No markdown fences.
"""


class PromptGeneratorAgent:
    def __init__(self) -> None:
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            if not settings.openai_api_key:
                raise RuntimeError("OPENAI_API_KEY is not set. Add it to backend/.env")
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def generate(self, req: PromptGenRequest) -> PromptGenResponse:
        scenes_payload = [s.model_dump() for s in req.scenes]
        completion = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(scenes_payload)},
            ],
            temperature=0.7,
        )
        raw = completion.choices[0].message.content.strip()
        parsed = json.loads(raw)
        return PromptGenResponse(prompts=parsed.get("prompts", []))


prompt_generator_agent = PromptGeneratorAgent()
