from google.cloud.firestore_v1.base_query import FieldFilter
from dotenv import load_dotenv
load_dotenv()

from google.cloud import firestore

# Firestore client to fetch quotes from the database
# Returns a dictionary with the quote's text, author, book, and document ID
def get_next_quote():
    
    # Connect to Firestore
    database = firestore.Client()
    
    # Query the "quotes" collection for the next unused quote
    docs = (database.collection("quotes").where("used", "==", False).limit(1).stream())
    
    # Loop through the query results and return the first unused quote
    for doc in docs:
        data = doc.to_dict()
        return{
            "id": doc.id,
            "text": data.get("text"),
            "author": data.get("author"),
            "book": data.get("book")
        }
        
    # If no unused quotes are found, return None
    return None


# Function to mark a quote as used in the Firestore database
def mark_quote_as_used(quote_id, date_posted):
    database = firestore.Client()
    database.collection("quotes").document(quote_id).update({
        "used": True,
        "date_posted": date_posted
    })
    
    
# Function to get the count of remaining unused quotes in the Firestore database
# Returns an integer representing the number of unused quotes
# Used in the dauly email as a reminder to top up the quote database when it runs low on quotes
def get_remaining_count() -> int:
    database = firestore.Client()
    
    docs = (
        database.collection("quotes").where(filter=FieldFilter("used", "==", False)).stream()
    )
    
    return sum (1 for _ in docs)