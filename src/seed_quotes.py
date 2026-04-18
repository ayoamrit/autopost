# Run this once to bulk upload all passages to Firestore.
# Usage: python src/seed_quotes.py

import os
from dotenv import load_dotenv
from google.cloud import firestore

load_dotenv()

db = firestore.Client()

quotes = [

    # Template for adding new quotes
    {
        "text": "To live is the rarest thing in the world. Most people exist, that is all. They move through their days like water finding the lowest point, never asking why they always end up there, never questioning the invisible forces that pull them down, away from everything they once believed they were capable of becoming.",
        "author": "Oscar Wilde",
        "book": "The Soul of Man Under Socialism",
        "used": False,
        "date_posted": ""
    }
]


def seed():
    print(f"📖 Uploading {len(quotes)} passages to Firestore...")
    collection = db.collection("quotes")

    for i, quote in enumerate(quotes, start=1):
        collection.add(quote)
        print(f"   ✅ {i}/{len(quotes)} — {quote['author']}: {quote['text'][:60]}...")

    print(f"\n🎉 Done! {len(quotes)} passages added to Firestore.")


if __name__ == "__main__":
    seed()