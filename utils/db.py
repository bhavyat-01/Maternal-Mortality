from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

def get_hospitals_collection():
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
    db = client["Mortality-App"]
    return db["Hospitals"]