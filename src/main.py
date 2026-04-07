from datetime import date
from dotenv import load_dotenv
from firestore_client import get_next_quote, mark_quote_as_used
from renderer import create_video
from llm_client import generate_caption

load_dotenv()

def run():
    print("Starting the autopost process...")
    today = date.today().strftime("%B %d, %Y")
        
    # Step 1: Fetch the next quote from Firestore (firestore_client.py)
    print("Fetching the next quote from Firestore...")
    quote = get_next_quote()
    
    if not quote:
        print("No unused quotes left in the database.")
        return
    
    print(f"Quote fetched: '{quote['text']}' — {quote['author']} — {quote['book']}")
    
    
    # Step 2: Create the video with the quote and date overlay (renderer.py)
    print("Creating the video with the quote and date overlay...")
    video_path = create_video(quote, today)
    print(f"Video created at: {video_path}")
    
    # Step 3: Mark the quote as used in Firestore (firestore_client.py)
    # Code will be added here in the future after we implement the posting functionality
    # For now, we'll just mark it as used immediately after creating the video
    
    # Step 4: Generate the caption and hastags using Gemini (llm_client.py)
    print("Generating caption and hashtags using Gemini...")
    caption_data = generate_caption(quote)
    print(f"Caption: {caption_data['caption']}")
    print(f"Hashtags: {caption_data['hashtags']}")
    
if __name__ == "__main__":
    run()