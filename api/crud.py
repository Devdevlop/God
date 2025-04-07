from database import database
from models import videos, images
from schemas import MediaSchema
from fastapi import HTTPException

async def get_videos(page: int, limit: int):
    query = videos.select().offset((page - 1) * limit).limit(limit)
    return await database.fetch_all(query)

async def get_images(page: int, limit: int):
    query = images.select().offset((page - 1) * limit).limit(limit)
    return await database.fetch_all(query)

async def save_media(media_data):
    if media_data.video_url:  # It's a video
        query = videos.insert().values(
            video_url=media_data.video_url,
            title=media_data.title,
            uploaded_by=media_data.uploaded_by
        )
        return await database.execute(query)

    elif media_data.image_url:  # It's an image
        query = images.insert().values(
            image_url=media_data.image_url,
            alt_text=media_data.alt_text,
            uploaded_by=media_data.uploaded_by
        )
        return await database.execute(query)

    raise HTTPException(status_code=400, detail="Invalid media type")

async def modify_media(media_id: int, media_data):
    if media_data.video_url:  # Updating a video
        query = videos.update().where(videos.c.id == media_id).values(
            video_url=media_data.video_url,
            title=media_data.title
        )
    elif media_data.image_url:  # Updating an image
        query = images.update().where(images.c.id == media_id).values(
            image_url=media_data.image_url,
            alt_text=media_data.alt_text
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid media type")

    result = await database.execute(query)
    
    if result == 0:  # If no row was updated
        raise HTTPException(status_code=404, detail="Media not found")
    
    return {"message": "Media updated successfully"}

async def remove_media(media_id: int):
    video_query = videos.delete().where(videos.c.id == media_id)
    image_query = images.delete().where(images.c.id == media_id)
    
    video_deleted = await database.execute(video_query)
    image_deleted = await database.execute(image_query)
    
    if not video_deleted and not image_deleted:
        raise HTTPException(status_code=404, detail="Media not found")
    
    return {"message": "Media deleted successfully"}

# ✅ New function: Update Media Order
async def update_media_order(media_list):
    """
    Updates the order of media items in the database.
    """
    for media in media_list:
        if media.get("video_url"):
            query = videos.update().where(videos.c.id == media["id"]).values(order_position=media["order"])
        elif media.get("image_url"):
            query = images.update().where(images.c.id == media["id"]).values(order_position=media["order"])
        else:
            continue  # Skip invalid entries
        await database.execute(query)
    
    return {"message": "Media order updated successfully"}
