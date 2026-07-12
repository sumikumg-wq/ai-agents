"""
Agent 1: Trend Hunter
MVP stub — returns model-generated topic ideas via OpenAI reasoning over the
niche. Swap the `_fetch_signals` internals later for real YouTube/Google
Trends API calls without changing the public interface.
"""
import json
from openai import OpenAI
from app.core.config import settings
from app.models.schemas import TrendRequest, TrendResponse, TrendItem

_SYSTEM_PROMPT = """You are a YouTube trend research analyst specializing in \
the History & Mystery niche. Given a niche, propose video topic ideas that \
are evergreen, have low-to-medium competition, and high curiosity potential. \
Respond ONLY with a JSON array of objects, each with keys: \
title, search_intent, competition (low|medium|high), estimated_ctr (e.g. "8-11%"), \
evergreen_score (1-10 integer). No prose, no markdown fences."""


class TrendHunterAgent:
    def __init__(self) -> None:
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            if not settings.openai_api_key:
                raise RuntimeError(
                    "OPENAI_API_KEY is not set. Add it to backend/.env"
                )
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def find_trends(self, req: TrendRequest) -> TrendResponse:
        user_prompt = f"Niche: {req.niche}\nHow many ideas: {req.count}"
        completion = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.9,
            response_format={"type": "json_object"} if False else None,
        )
        raw = completion.choices[0].message.content.strip()
        # Model may wrap array in an object; handle both shapes defensively.
        parsed = json.loads(raw)
        items_raw = parsed if isinstance(parsed, list) else parsed.get("items", [])
        items = [TrendItem(**item) for item in items_raw]
        return TrendResponse(items=items)


trend_hunter_agent = TrendHunterAgent()
