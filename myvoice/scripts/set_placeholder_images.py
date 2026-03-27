import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.curriculum import Activity

settings = get_settings()

async def set_placeholder():
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        stmt = select(Activity).where(
            (Activity.image_path == None) | (Activity.image_path == "")
        )
        result = await db.execute(stmt)
        activities = result.scalars().all()
        
        print(f"Assigning placeholder to {len(activities)} activities...")
        for activity in activities:
            activity.image_path = "/vite.svg"
            
        await db.commit()
    
    await engine.dispose()
    print("Done.")

if __name__ == "__main__":
    asyncio.run(set_placeholder())
