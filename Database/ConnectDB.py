# database/ConnectDB.py
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo.errors

def get_database():
    """
    Establishes a connection to the MongoDB database and returns the database object.
    Loads environment variables from env/config/.env.
    """
    # Load environment variables
    load_dotenv(os.path.join("env", "config", ".env"))

    # Get environment variables
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_CLUSTER = os.getenv("DB_CLUSTER")
    DB_NAME = os.getenv("DB_NAME")

    # Validate environment variables
    if not all([DB_USERNAME, DB_PASSWORD, DB_CLUSTER, DB_NAME]):
        raise ValueError("Missing required environment variables: DB_USERNAME, DB_PASSWORD, DB_CLUSTER, DB_NAME")

    # Construct MongoDB connection string
    uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CLUSTER}.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&appName=Cluster0"

    # Initialize MongoDB client
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Test connection with a ping
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        # Return the database object
        return client[DB_NAME]
    except pymongo.errors.ConnectionError as e:
        print(f"Connection failed: {e}")
        raise
    except pymongo.errors.ConfigurationError as e:
        print(f"Configuration error: {e}")
        raise

def get_collection():
    """
    Returns the collection from the database.
    """
    db = get_database()
    return db["BooksCollection"]