import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.config import get_settings

settings = get_settings()

async def check_columns():
    engine = create_async_engine(settings.database_url)
    async with engine.connect() as conn:
        print("Checking columns in 'activities' table...")
        result = await conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'activities';"))
        columns = result.fetchall()
        for col in columns:
            print(f" - {col[0]} ({col[1]})")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_columns())
