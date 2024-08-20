from utils.db import MongoDb
mongo = MongoDb()

async def register_user(userEmail: str):
    """receive webhook data and register user in our db"""
    user_exists = await mongo.find_one("Users", {"userEmail": userEmail})
    if not user_exists:
        try:    
            user = await mongo.insert_one("Users", {"userEmail": userEmail})
        except Exception as e:
            return None
    return user