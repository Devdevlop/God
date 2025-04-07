from pydantic import BaseModel,field_validator
from typing import Optional, List

class AdminLogin(BaseModel):
    username: str
    password: str

class VideoSchema(BaseModel):
    id: int
    video_url: str
    title: Optional[str] = None
    uploaded_by: Optional[int] = None
    created_at: Optional[str] = None

class ImageSchema(BaseModel):
    id: int
    image_url: str
    alt_text: Optional[str] = None
    uploaded_by: Optional[int] = None
    created_at: Optional[str] = None

class MediaResponse(BaseModel):
    videos: List[VideoSchema]
    images: List[ImageSchema]

class MediaSchema(BaseModel):
    media_ids: List[int]

    @field_validator("media_ids", mode="before")
    @classmethod
    def check_non_empty_list(cls, value):
        """Ensures that media_ids list is not empty."""
        if not value or not isinstance(value, list):
            raise ValueError("media_ids must be a non-empty list.")
        return value

class MFAVerifyRequest(BaseModel):
    username: str
    token: str