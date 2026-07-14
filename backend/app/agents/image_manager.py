"""
Agent 6: Image Manager
Generates AI images via OpenAI's image API, or fetches public-domain
historical assets from Wikimedia Commons when a real photo/artwork fits
better than a generated one.
"""
import os
import base64
import requests
from openai import OpenAI
from app.core.config import settings
from app.models.schemas import ImageRequest, ImageResult

_OUTPUT_ROOT = "generated"

_WIKIMEDIA_SEARCH_URL = "https://commons.wikimedia.org/w/api.php"


class ImageManagerAgent:
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
        path = os.path.join(_OUTPUT_ROOT, project_id, "images")
        os.makedirs(path, exist_ok=True)
        return path

    def _try_public_domain(self, prompt: str) -> tuple[str, str] | None:
        """Search Wikimedia Commons for a usable public-domain image. Returns
        (image_url, attribution) or None if nothing suitable was found."""
        try:
            resp = requests.get(
                _WIKIMEDIA_SEARCH_URL,
                params={
                    "action": "query",
                    "format": "json",
                    "generator": "search",
                    "gsrsearch": prompt,
                    "gsrnamespace": 6,
                    "gsrlimit": 1,
                    "prop": "imageinfo",
                    "iiprop": "url|extmetadata",
                },
                timeout=10,
            )
            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            for _, page in pages.items():
                info = page.get("imageinfo", [{}])[0]
                url = info.get("url")
                artist = (
                    info.get("extmetadata", {})
                    .get("Artist", {})
                    .get("value", "Wikimedia Commons")
                )
                if url:
                    return url, f"Source: Wikimedia Commons — {artist}"
        except Exception:
            return None
        return None

    def _generate_ai_image(self, prompt: str, out_path: str) -> None:
        result = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1536",
        )
        image_b64 = result.data[0].b64_json
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(image_b64))

    def get_image(self, req: ImageRequest) -> ImageResult:
        out_dir = self._project_dir(req.project_id)
        filename = f"scene_{req.scene_number}.png"
        out_path = os.path.join(out_dir, filename)

        if req.prefer_public_domain:
            found = self._try_public_domain(req.prompt)
            if found:
                url, attribution = found
                return ImageResult(
                    scene_number=req.scene_number,
                    source="public_domain",
                    path_or_url=url,
                    attribution=attribution,
                )

        try:
            self._generate_ai_image(req.prompt, out_path)
            return ImageResult(
                scene_number=req.scene_number,
                source="ai_generated",
                path_or_url=out_path,
            )
        except Exception as e:
            return ImageResult(
                scene_number=req.scene_number,
                source="failed",
                path_or_url="",
                attribution=str(e),
            )


image_manager_agent = ImageManagerAgent()
