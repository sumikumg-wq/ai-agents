"""
Agent 9: Video Builder
Assembles narration audio + scene images + burned-in subtitles into a
final MP4 using FFmpeg. MVP: even-duration slideshow synced to audio length
(swap in per-scene durations from the storyboard once available).
"""
import os
import subprocess
from app.models.schemas import VideoBuildRequest, VideoBuildResponse

_OUTPUT_ROOT = "generated"


class VideoBuilderAgent:
    def _project_dir(self, project_id: str) -> str:
        path = os.path.join(_OUTPUT_ROOT, project_id, "video")
        os.makedirs(path, exist_ok=True)
        return path

    def _audio_duration_seconds(self, audio_path: str) -> float:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", audio_path,
            ],
            capture_output=True, text=True, check=True,
        )
        return float(result.stdout.strip())

    def build(self, req: VideoBuildRequest) -> VideoBuildResponse:
        if not req.image_paths:
            raise RuntimeError("At least one image is required to build a video.")

        out_dir = self._project_dir(req.project_id)
        out_path = os.path.join(out_dir, "final.mp4")
        concat_list_path = os.path.join(out_dir, "concat_list.txt")

        total_duration = self._audio_duration_seconds(req.audio_path)
        per_image = max(total_duration / len(req.image_paths), 0.5)

        with open(concat_list_path, "w") as f:
            for img in req.image_paths:
                f.write(f"file '{os.path.abspath(img)}'\n")
                f.write(f"duration {per_image}\n")
            # ffmpeg concat demuxer requires the last file repeated without duration
            f.write(f"file '{os.path.abspath(req.image_paths[-1])}'\n")

        width, height = req.resolution.split("x")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_list_path,
            "-i", req.audio_path,
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=increase,"
                   f"crop={width}:{height}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest",
            out_path,
        ]

        if req.srt_path and os.path.exists(req.srt_path):
            cmd[cmd.index("-vf") + 1] += f",subtitles={req.srt_path}"

        subprocess.run(cmd, check=True, capture_output=True)

        return VideoBuildResponse(video_path=out_path)


video_builder_agent = VideoBuilderAgent()
