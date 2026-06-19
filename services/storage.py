# services/storage.py
import os
from pymongo import MongoClient
from bson import ObjectId          # comes with pymongo

class JobStorage:
    def __init__(self, uri: str | None = None):
        self.client = MongoClient(uri or os.environ.get("MONGO_URI", "mongodb://localhost:27017/"))
        self.collection = self.client["jobgenie"]["jobs"]

    def store_jobs(self, jobs: list[dict]) -> list:
        print (f"Storing {len(jobs)} jobs in MongoDB...",jobs)
        result = self.collection.insert_many(jobs)   # nested data is fine here
        return [str(_id) for _id in result.inserted_ids]   # return the new _ids as strings

    def get_job(self, job_id: str) -> dict | None:
        return self.collection.find_one({"_id": ObjectId(job_id)})
    
    def get_all_jobs(self) -> list[dict]:
        return list(self.collection.find())