"""
Agent 11: SEO Agent
Generates YouTube metadata: title, description, tags, hashtags, keywords,
a pinned comment, and a playlist suggestion.
"""
import json
from openai import OpenAI
from app.core.config import settings
from app.models.schemas import SEORequest, SEOResponse

_SYSTEM_PROMPT = """You are a YouTube SEO specialist for a faceless History \
& Mystery documentary channel. Given a topic and script, generate metadata \
optimized for search and click-through without being clickbait-dishonest.

Respond ONLY with a JSON object with keys:
- "title" (under 100 characters, curiosity-driven, accurate)
- "description" (2-4 short paragraphs, first line is the strongest hook,
  include natural keywords)
- "tags" (array of 15-20 short keyword strings)
- "hashtags" (array of 3-5 hashtags including the #)
- "keywords" (array of 8-12 SEO keyword phrases)
- "pinned_comment" (1-2 sentences that invite discussion/engagement)
- "playlist_suggestion" (a playlist name this video would fit into)

No prose outside the JSON. No markdown fences.
"""


class SEOAgent:
    def __init__(self) -> None:
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            if not settings.openai_api_key:
                raise RuntimeError("OPENAI_API_KEY is not set. Add it to backend/.env")
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def generate(self, req: SEORequest) -> SEOResponse:
        completion = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Topic: {req.topic}\n\nScript:\n{req.script}"},
            ],
            temperature=0.7,
        )
        raw = completion.choices[0].message.content.strip()
        parsed = json.loads(raw)
        return SEOResponse(**parsed)


seo_agent = SEOAgent()
