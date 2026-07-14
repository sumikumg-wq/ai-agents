"""
Agent 12: Publisher
Uploads the finished video to YouTube via the YouTube Data API, supporting
draft/private/unlisted/public, thumbnail assignment, and scheduling.
Requires YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN in backend/.env (OAuth
credentials from a Google Cloud project with the YouTube Data API enabled).
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from app.core.config import settings
from app.models.schemas import PublishRequest, PublishResponse

_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
_TOKEN_URI = "https://oauth2.googleapis.com/token"


class PublisherAgent:
    def _client(self):
        if not (
            settings.youtube_client_id
            and settings.youtube_client_secret
            and settings.youtube_refresh_token
        ):
            raise RuntimeError(
                "YouTube OAuth credentials are not set. Add YOUTUBE_CLIENT_ID, "
                "YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN to backend/.env"
            )
        creds = Credentials(
            token=None,
            refresh_token=settings.youtube_refresh_token,
            client_id=settings.youtube_client_id,
            client_secret=settings.youtube_client_secret,
            token_uri=_TOKEN_URI,
            scopes=_SCOPES,
        )
        return build("youtube", "v3", credentials=creds)

    def publish(self, req: PublishRequest) -> PublishResponse:
        youtube = self._client()

        body = {
            "snippet": {
                "title": req.title[:100],
                "description": req.description,
                "tags": req.tags,
                "categoryId": "27",  # Education
            },
            "status": {
                "privacyStatus": req.privacy_status,
                **({"publishAt": req.scheduled_at} if req.scheduled_at else {}),
            },
        }

        media = MediaFileUpload(req.video_path, chunksize=-1, resumable=True)
        insert_request = youtube.videos().insert(
            part="snippet,status", body=body, media_body=media
        )
        response = insert_request.execute()
        video_id = response["id"]

        if req.thumbnail_path:
            youtube.thumbnails().set(
                videoId=video_id, media_body=MediaFileUpload(req.thumbnail_path)
            ).execute()

        return PublishResponse(
            youtube_video_id=video_id,
            youtube_url=f"https://youtube.com/watch?v={video_id}",
            privacy_status=req.privacy_status,
        )


publisher_agent = PublisherAgent()
