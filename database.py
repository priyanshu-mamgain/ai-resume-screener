from dotenv import load_dotenv
import os
import certifi
from datetime import datetime
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())

db = client["resume_screener"]
resumes_collection = db["resumes"]

def save_result(resume_text, job_description, score, user_id):
    """Save a screening result to MongoDB, tagged with the visitor's user_id"""
    result = {
        "user_id": user_id,
        "resume_text": resume_text,
        "job_description": job_description,
        "score": score,
        "timestamp": datetime.utcnow()
    }
    resumes_collection.insert_one(result)
    return result

def get_all_results(user_id):
    """Fetch only this visitor's past screening results, most recent first"""
    results = list(
        resumes_collection.find({"user_id": user_id}, {"_id": 0}).sort("timestamp", -1)
    )
    return results


if __name__ == "__main__":
    print("Connected! Collections:", db.list_collection_names())