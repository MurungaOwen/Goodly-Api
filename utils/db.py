from pymongo import MongoClient
from decouple import config

if config("PRODUCTION", cast=bool):
    MONGO_URL = 'mongodb+srv://' + config("MONGO_USERNAME") + ':' + config("MONGO_PASSWORD") + '@' + config("MONGO_CLUSTER")
else:
    MONGO_URL= "mongodb://localhost:27017"

    
DATABASE_NAME = "Goodly"

class MongoDb():
    def __init__(self):
        """class constructor"""
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[DATABASE_NAME]
        print("we connected")
    
    def close(self):
        """closing the db connection"""
        self.client.close()
    
    def get_collection(self, collection_name: str):
        """get collection name"""
        return self.db[collection_name]

    def insert_one(self, collection_name: str, document: dict):
        """insert values"""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def find_one(self, collection_name: str, query: dict):
        collection = self.get_collection(collection_name)
        document = collection.find_one(query)
        if document and "_id" in document:
            document["_id"] = str(document["_id"])  # Convert ObjectId to string
        return document
    
    def find(self, collection_name: str, query: dict = {}):
        """list many"""
        collection = self.get_collection(collection_name)
        documents = list(collection.find(query))
        for doc in documents:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        return documents

    def update_one(self, collection_name: str, query: dict, update: dict):
        collection = self.get_collection(collection_name)
        result = collection.update_one(query, {"$set": update})
        return result.modified_count

    def delete_one(self, collection_name: str, query: dict):
        collection = self.get_collection(collection_name)
        result = collection.delete_one(query)
        return result.deleted_count
    
