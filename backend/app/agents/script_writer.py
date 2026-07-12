"""
Agent 3: Script Writer
Generates documentary-style narration scripts with a strong 3-second hook,
simple English, curiosity gaps, and no filler — tuned per target length.
"""
from openai import OpenAI
from app.core.config import settings
from app.models.schemas import ScriptRequest, ScriptResponse

_LENGTH_GUIDANCE = {
    "30s": "~75-90 words total. One hook, one twist, one payoff.",
    "60s": "~150-170 words total. Hook, 2 supporting beats, payoff.",
    "5min": "~750-800 words total. Hook, timeline, 3-4 acts, payoff, call to reflect.",
    "10min": "~1500-1600 words total. Hook, deep timeline, multiple acts, "
             "competing theories, payoff, call to reflect.",
}

_SYSTEM_PROMPT = """You are an expert documentary scriptwriter for a faceless \
YouTube channel in the History & Mystery niche, in the style of Netflix \
documentaries. Rules:
- The first 3 seconds must be a powerful hook (a question, shocking fact, or \
mystery statement).
- Simple, spoken English. Short sentences. No filler words.
- Build curiosity gaps between beats — never resolve everything at once.
- Natural pacing suited for narration (no stage directions, no scene numbers).
- End on a memorable, thought-provoking line.
Return ONLY the narration script as plain text, nothing else.
"""


class ScriptWriterAgent:
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

    def generate(self, req: ScriptRequest) -> ScriptResponse:
        guidance = _LENGTH_GUIDANCE[req.length]
        user_prompt = (
            f"Topic: {req.topic}\n"
            f"Target length: {req.length} ({guidance})\n"
            f"Language: {req.language}\n"
            f"Tone: {req.tone}\n"
        )

        completion = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8,
        )
        script_text = completion.choices[0].message.content.strip()
        hook = script_text.split("\n")[0][:200]
        word_count = len(script_text.split())

        return ScriptResponse(
            topic=req.topic,
            length=req.length,
            hook=hook,
            script=script_text,
            estimated_word_count=word_count,
        )


script_writer_agent = ScriptWriterAgent()
