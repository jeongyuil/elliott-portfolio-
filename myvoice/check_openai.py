import asyncio
import openai
import os
from dotenv import load_dotenv

async def check():
    load_dotenv()
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("No API Key found")
        return
    client = openai.AsyncOpenAI(api_key=key)
    try:
        resp = await client.models.list()
        print("API Key is valid. Found models.")
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
