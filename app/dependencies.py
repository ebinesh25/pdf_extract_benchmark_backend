from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings

settings = get_settings()

class Mongo:
    client: AsyncIOMotorClient | None = None

mongo = Mongo()


async def connect_to_mongo():
    mongo.client = AsyncIOMotorClient(settings.mongo_uri)


async def close_mongo():
    mongo.client.close()


def get_db():
    return mongo.client[settings.mongo_db_name]
