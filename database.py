from dotenv import load_dotenv
import os
from datetime import datetime
from pymongo import MongoClient

load_dotenv()
print("Loaded MONGO_URI:", os.getenv("MONGO_URI"))

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["resume_screener"]
resumes_collection = db["resumes"]

def save_result(resume_text, job_description, score):
    """Save a screening result to MongoDB with a timestamp"""
    result = {
        "resume_text": resume_text,
        "job_description": job_description,
        "score": score,
        "timestamp": datetime.utcnow()
    }
    resumes_collection.insert_one(result)
    return result

def get_all_results():
    """Fetch all past screening results, most recent first"""
    results = list(
        resumes_collection.find({}, {"_id": 0}).sort("timestamp", -1)
    )
    return results


if __name__ == "__main__":
    print("Connected! Collections:", db.list_collection_names())