"""
Agent 7: Voice Generator
Generates narration audio using Edge TTS (free, default). ElevenLabs can be
added later as a premium alternative behind the same interface.
"""
import os
import asyncio
import edge_tts
from app.models.schemas import VoiceRequest, VoiceResponse

_OUTPUT_ROOT = "generated"


class VoiceGeneratorAgent:
    def _project_dir(self, project_id: str) -> str:
        path = os.path.join(_OUTPUT_ROOT, project_id, "audio")
        os.makedirs(path, exist_ok=True)
        return path

    async def _synthesize(self, text: str, voice: str, out_path: str) -> None:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(out_path)

    def generate(self, req: VoiceRequest) -> VoiceResponse:
        out_dir = self._project_dir(req.project_id)
        out_path = os.path.join(out_dir, req.filename)

        asyncio.run(self._synthesize(req.text, req.voice, out_path))

        return VoiceResponse(
            audio_path=out_path,
            voice=req.voice,
            characters=len(req.text),
        )


voice_generator_agent = VoiceGeneratorAgent()
