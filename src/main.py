import os
import sys
from datetime import date
from dotenv import load_dotenv
from firestore_client import get_next_quote, mark_quote_as_used, get_remaining_count
from renderer import create_video
from image_renderer import create_image
from email_client import send_email
from llm_client import generate_caption
from tiktok_client import upload_to_tiktok

load_dotenv()

def run():
    print("Starting the autopost process...")
    today = date.today().strftime("%B %d, %Y")
        
    # Step 1: Fetch the next quote from Firestore (firestore_client.py)
    print("Step 1: Fetching the next quote from Firestore...")
    quote = get_next_quote()
    
    if not quote:
        print("No unused quotes left in the database.")
        return
    
    print(f"Quote fetched: '{quote['text']}' — {quote['author']} — {quote['book']}")
    
    
    
    # Step 2: Generate the caption and hastags using Gemini (llm_client.py)
    print("Step 2:Generating caption and hashtags using Gemini...")
    caption_data = generate_caption(quote)
    print(f"Caption: {caption_data['caption']}")
    print(f"Hashtags: {caption_data['hashtags']}")
    
    # Step 3: Create image with quote using image_renderer.py
    print("Step 3: Creating the quote image...")
    image_path = create_image(quote, today)
    print(f"Quote image created at: {image_path}")
    
    # Step 4: Send the quote image and caption via email (email_client.py)
    print("Step 4: Sending the quote image and caption via email...")
    remaining_quote_count = get_remaining_count()
    email_success = send_email(image_path, caption_data, remaining_quote_count)
    
    if not email_success:
        print("Email failed to send. Quote will not be marked as used.")
        sys.exit(1)
        
    # Step 5: Clean up image file
    print("Step 5: Cleaning up image file...")
    try:
        os.remove(image_path)
        print("Image file deleted successfully.")
    except Exception as e:
        print(f"Error deleting image file: {e}")
        
    # Step 6: Mark the quote as used in Firestore (firestore_client.py)
    print("Step 6: Marking the quote as used in Firestore...")
    mark_quote_as_used(quote["id"], today)
    print("Quote marked as used successfully.")
    
    print("\n" + "=" * 50)
    print("Autopost process completed successfully!")
    
        
        
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------
    # PAUSED: TikTok Video Pipeline (renderer.py, tiktok_client.py)
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------
    
    # Step 2: Create the video with the quote and date overlay (renderer.py)
    # print("Step 2:Creating the video with the quote and date overlay...")
    # video_path = create_video(quote, today)
    # print(f"Video created at: {video_path}")
    
    
    #Step 4: Upload the video to TikTok (tiktok_client.py)
    # print("Step 4: Uploading the video to TikTok...")
    # upload_success = upload_to_tiktok(video_path, f"{caption_data['caption']} {caption_data['hashtags']}")
    
    # if not upload_success:
    #    print("Pipeline stopped due to upload failure.")
    #    print(" -> Quote was NOT marked as used.")
    #    print(" -> Video file was NOT deleted.")
    #    print(" -> Fix the issue and run again.")
    #    sys.exit(1)
        
        
    # Step 5: Clean up video file
    # print("Step 5: Cleaning up video file...")
    # try:
    #     os.remove(video_path)
    #     print("Video file deleted successfully.")
    # except Exception as e:
    #     print(f"Error deleting video file: {e}")
    #     print("Please check the file and delete it manually.")
    
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------
    # PAUSED: TikTok Video Pipeline (renderer.py, tiktok_client.py)
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------

    
if __name__ == "__main__":
    run()