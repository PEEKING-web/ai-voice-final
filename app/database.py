import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.voice_assistant

async def save_interaction(user_input, bot_response):
    interaction = {"user_input": user_input, "bot_response": bot_response}
    await db.interactions.insert_one(interaction)
