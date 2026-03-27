import asyncio
import os
import httpx
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.config import get_settings
from app.models.curriculum import Activity

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key)

async def generate_images():
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # Find activities with image_prompt but no image_path
        stmt = select(Activity).where(
            Activity.image_prompt.isnot(None),
            Activity.image_prompt != "",
            (Activity.image_path == None) | (Activity.image_path == "")
        )
        result = await db.execute(stmt)
        activities = result.scalars().all()
        
        print(f"Found {len(activities)} activities needing images.")
        
        async with httpx.AsyncClient() as http_client:
            for activity in activities:
                print(f"Generating image for {activity.name}...")
                
                # 1. Create Folder
                unit_id = activity.curriculum_unit_id
                save_dir = f"frontend/public/story_images/{unit_id}"
                os.makedirs(save_dir, exist_ok=True)
                
                # 2. Call DALL-E
                try:
                    prompt = f"Educational illustration for children storybook. 3D Pixar Style. {activity.image_prompt}"
                    # Truncate prompt if too long
                    prompt = prompt[:1000]
                    
                    response = await client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    image_url = response.data[0].url
                    
                    # 3. Download & Save
                    file_name = f"{activity.activity_id}.png"
                    file_path = f"{save_dir}/{file_name}"
                    
                    resp = await http_client.get(image_url)
                    if resp.status_code == 200:
                        content = resp.content
                        with open(file_path, "wb") as f:
                            f.write(content)
                            
                        # 4. Update DB
                        # Save relative path for usage in frontend
                        # frontend/public is root, so path starts with /story_images/...
                        db_path = f"/story_images/{unit_id}/{file_name}"
                        activity.image_path = db_path
                        await db.commit()
                        print(f"  -> Saved to {db_path}")
                    else:
                        print(f"  -> Failed to download: {resp.status_code}")
                            
                except Exception as e:
                    print(f"  -> Error generating image: {e}")
                
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(generate_images())
