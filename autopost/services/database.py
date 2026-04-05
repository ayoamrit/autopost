import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from autopost.models.quote import Quote

# Read environment variables from .env file
load_dotenv()

class QuoteRepository:
    def __init__(self):
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        collection_name = os.getenv('FIRESTORE_COLLECTION')
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred)
            
        self.database = firestore.client()
        self.collection = collection_name
        
    def fetch_next_quote(self):
        docs = (self.database.collection(self.collection).where("used", "==", False).limit(1).stream())
        
        doc = next(iter(docs), None)
        
        if(doc is None):
            raise Exception("No unused quotes found in the database.")
        
        data = doc.to_dict()
        return Quote(
            doc_id=doc.id,
            text=data["text"],
            author=data["author"],
            category=data.get("category"),
            used=data["used"]
        )
        