"""
Agent 2: Research Agent
Collects factual information for a topic: timeline, verified facts vs.
speculation (clearly separated), competing theories, and primary sources.
Feeds directly into Agent 3 (Script Writer) — call this first in the
video workflow.
"""
import json
from openai import OpenAI
from app.core.config import settings
from app.models.schemas import ResearchRequest, ResearchResponse

_DEPTH_GUIDANCE = {
    "brief": "3-5 timeline events, 3-5 verified facts, 0-2 competing theories.",
    "standard": "6-10 timeline events, 6-10 verified facts, 1-3 competing theories.",
    "deep": "10-15 timeline events, 10-15 verified facts, 2-5 competing theories, "
            "with more nuance in speculative claims.",
}

_SYSTEM_PROMPT = """You are a rigorous historical researcher for a documentary \
production team. For the given topic, produce structured research. You MUST \
clearly separate verified historical facts from speculation/legend/disputed \
claims — never blend them. When uncertain about a specific source, use a \
general but honest source description (e.g. "widely cited in mainstream \
historical accounts") rather than inventing a specific citation you are not \
certain exists.

Respond ONLY with a single JSON object with these exact keys:
- "timeline": array of {"date": string, "event": string}
- "verified_facts": array of {"statement": string, "verified": true, "source": string}
- "speculative_claims": array of {"statement": string, "verified": false, "source": string}
- "competing_theories": array of {"theory": string, "supporting_evidence": string, "credibility": "low"|"medium"|"high"}
- "primary_sources": array of strings (names/descriptions of primary source types or archives, not fabricated URLs)

No prose outside the JSON. No markdown fences.
"""


class ResearchAgent:
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

    def research(self, req: ResearchRequest) -> ResearchResponse:
        guidance = _DEPTH_GUIDANCE[req.depth]
        user_prompt = f"Topic: {req.topic}\nDepth: {req.depth} ({guidance})"

        completion = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
        )
        raw = completion.choices[0].message.content.strip()
        parsed = json.loads(raw)

        return ResearchResponse(
            topic=req.topic,
            timeline=parsed.get("timeline", []),
            verified_facts=parsed.get("verified_facts", []),
            speculative_claims=parsed.get("speculative_claims", []),
            competing_theories=parsed.get("competing_theories", []),
            primary_sources=parsed.get("primary_sources", []),
        )


research_agent = ResearchAgent()
