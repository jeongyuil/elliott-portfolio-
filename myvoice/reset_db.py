import asyncio
from app.database import engine, Base
from app.models import * 

async def reset_db():
    async with engine.begin() as conn:
        print("Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
    print("DB Reset complete.")

if __name__ == "__main__":
    asyncio.run(reset_db())
