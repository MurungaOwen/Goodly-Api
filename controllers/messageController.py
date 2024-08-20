from utils.db import MongoDb

mongo = MongoDb()

async def create_message(message: dict):
    results = await mongo.insert_one("Message", message)
    return results
