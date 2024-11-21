from pymongo import MongoClient
import os


def test_mongo_connection():
    try:
        # Get MongoDB URI from environment variables
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

        # Establish a connection
        client = MongoClient(mongo_uri)

        # List available databases as a test
        databases = client.list_database_names()
        print("Successfully connected to MongoDB!")
        print(f"Available Databases: {databases}")
        return True
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return False


# Connect to MongoDB
def get_mongo_client():
    client = MongoClient(os.getenv("MONGO_URI"))
    return client["application_db"]


def upload_to_mongodb(data, collection_name):
    db = get_mongo_client()
    db[collection_name].insert_one(data)


def fetch_from_mongodb(collection_name):
    db = get_mongo_client()
    return list(db[collection_name].find())


def update_application_status(application_id, new_status):
    db = get_mongo_client()
    db["applications"].update_one({"_id": application_id}, {"$set": {"status": new_status}})

def fetch_from_mongodb_by_id(collection_name, user_id):
    db = get_mongo_client()
    return list(db[collection_name].find({"userid": user_id}))

def fetch_reviews_from_mongodb(collection_name="reviews"):
    # Establish a connection to the MongoDB server
    client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string if needed
    db = client["your_database_name"]  # Replace with your database name
    collection = db[collection_name]

    # Fetch all reviews from the collection
    reviews = list(collection.find({}))

    # Close the connection
    client.close()

    return reviews

from pymongo import MongoClient

def update_review_in_mongodb(psid, reviewer, comments, rating, status, collection_name="reviews"):
    # Establish a connection to the MongoDB server
    client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string if needed
    db = client["your_database_name"]  # Replace with your database name
    collection = db[collection_name]

    # Update the review in the collection
    collection.update_one(
        {"psid": psid},
        {"$set": {
            "reviewer": reviewer,
            "comments": comments,
            "rating": rating,
            "status": status
        }},
        upsert=True  # Create the document if it doesn't exist
    )

    # Close the connection
    client.close()