"""
Agent 10: Thumbnail Generator
Composes a high-CTR thumbnail: dark cinematic background, large readable
text, strong focal point, high contrast, no watermark.
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from app.models.schemas import ThumbnailRequest, ThumbnailResponse

_OUTPUT_ROOT = "generated"
_SIZE = (1280, 720)


class ThumbnailGeneratorAgent:
    def _project_dir(self, project_id: str) -> str:
        path = os.path.join(_OUTPUT_ROOT, project_id, "thumbnail")
        os.makedirs(path, exist_ok=True)
        return path

    def _load_font(self, size: int) -> ImageFont.FreeTypeFont:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        for path in candidates:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        return ImageFont.load_default()

    def generate(self, req: ThumbnailRequest) -> ThumbnailResponse:
        out_dir = self._project_dir(req.project_id)
        out_path = os.path.join(out_dir, "thumbnail.png")

        if req.background_image_path and os.path.exists(req.background_image_path):
            bg = Image.open(req.background_image_path).convert("RGB")
            bg = bg.resize(_SIZE)
            bg = bg.filter(ImageFilter.GaussianBlur(1)).point(lambda p: p * 0.55)
        else:
            bg = Image.new("RGB", _SIZE, (11, 15, 25))  # matches app theme #0B0F19

        # Dark vignette gradient at the bottom for text contrast.
        overlay = Image.new("RGBA", _SIZE, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for i in range(_SIZE[1] // 2, _SIZE[1]):
            alpha = int(180 * (i - _SIZE[1] // 2) / (_SIZE[1] / 2))
            draw.line([(0, i), (_SIZE[0], i)], fill=(0, 0, 0, alpha))
        bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")

        draw = ImageDraw.Draw(bg)
        font = self._load_font(96)
        wrapped = textwrap.fill(req.title_text.upper(), width=14)

        # Simple outline for high-contrast large readable text.
        x, y = 60, _SIZE[1] - 260
        for dx in (-3, 0, 3):
            for dy in (-3, 0, 3):
                draw.multiline_text((x + dx, y + dy), wrapped, font=font, fill="black")
        draw.multiline_text((x, y), wrapped, font=font, fill="white")

        bg.save(out_path)

        return ThumbnailResponse(thumbnail_path=out_path)


thumbnail_generator_agent = ThumbnailGeneratorAgent()
