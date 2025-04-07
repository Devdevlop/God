from fastapi import APIRouter, Query
from typing import Dict
from crud import get_videos, get_images, update_media_order
from schemas import MediaResponse, MediaSchema

router = APIRouter()

@router.get("/media", response_model=MediaResponse)
async def fetch_media(page: int = Query(1, ge=1), limit: int = Query(6, ge=1, le=20)):
    """Fetches media URLs (videos & images) with pagination."""
    videos_data = await get_videos(page, limit)
    images_data = await get_images(page, limit)
    return {"videos": videos_data, "images": images_data}

@router.put("/media", response_model=Dict[str, str])
async def update_media(media_data: MediaSchema):
    """Updates the order of media elements to maintain the desired arrangement."""
    await update_media_order(media_data)
    return {"message": "Media order updated successfully"}
