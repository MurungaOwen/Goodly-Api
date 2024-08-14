from utils.db import MongoDb

mongo = MongoDb()

def register_user(userEmail):
    """receive webhook data and register user in our db"""
    user = mongo.insert_one("Users", {"userEmail": userEmail})
    return user