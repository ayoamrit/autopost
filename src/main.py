import os
import sys
from datetime import date
from dotenv import load_dotenv

from logger import get_logger
from firestore_client import get_next_quote, mark_quote_as_used, get_remaining_count
from image_renderer import create_image
from email_client import send_email
from llm_client import generate_caption

# Paused imports (uncomment to re-enable TikTok pipeline)
# from tiktok_client import upload_to_tiktok
# from renderer import create_video

load_dotenv()
log = get_logger(__name__)

def run():
    log.info("Starting the autopost process...")
    today = date.today().strftime("%B %d, %Y")
        
    # Step 1: Fetch the next quote from Firestore (firestore_client.py)
    log.info("Step 1: Fetching the next quote from Firestore...")
    quote = get_next_quote()
    
    if not quote:
        log.critical("No unused quotes left in the database. Add more using seed_quotes.py")
        return
    
    log.info(
        "Quote fetched: '%s' — %s — %s",
        quote['text'][:60],
        quote['author'],
        quote['book']
    )
    
    # Step 2: Generate the caption and hastags using Gemini (llm_client.py)
    log.info("Step 2:Generating caption and hashtags using Gemini...")
    caption_data = generate_caption(quote)
    log.info("Caption: %s", caption_data['caption'])
    log.info("Hashtags: %s", caption_data['hashtags'])
    
    # Step 3: Create image with quote using image_renderer.py
    log.info("Step 3: Creating the quote image...")
    image_path = create_image(quote, today)
    log.info("Quote image created at: %s", image_path)
    
    # Step 4: Send the quote image and caption via email (email_client.py)
    log.info("Step 4: Sending the quote image and caption via email...")
    remaining_quote_count = get_remaining_count()
    email_success = send_email(image_path, caption_data, remaining_quote_count)
    
    if not email_success:
        log.error("Email failed to send. Quote will not be marked as used.")
        sys.exit(1)
        
    # Step 5: Clean up image file
    log.info("Step 5: Cleaning up image file...")
    try:
        os.remove(image_path)
        log.info("Image file deleted successfully.")
    except Exception as e:
        log.warning("Error deleting image file: %s", e)
        
    # Step 6: Mark the quote as used in Firestore (firestore_client.py)
    log.info("Step 6: Marking the quote as used in Firestore...")
    mark_quote_as_used(quote["id"], today)
    log.info("Quote marked as used successfully.")
    
    log.info("\n" + "=" * 50)
    log.info("Autopost process completed successfully!")
    
        
        
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------
    # PAUSED: TikTok Video Pipeline (renderer.py, tiktok_client.py)
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------
    
    # Step 2: Create the video with the quote and date overlay (renderer.py)
    # log.info("Step 2:Creating the video with the quote and date overlay...")
    # video_path = create_video(quote, today)
    # log.info("Video created at: %s", video_path)
    
    
    #Step 4: Upload the video to TikTok (tiktok_client.py)
    # log.info("Step 4: Uploading the video to TikTok...")
    # upload_success = upload_to_tiktok(video_path, f"{caption_data['caption']} {caption_data['hashtags']}")
    
    # if not upload_success:
    #    log.error("Pipeline stopped due to upload failure.")
    #    log.error(" -> Quote was NOT marked as used.")
    #    log.error(" -> Video file was NOT deleted.")
    #    log.error(" -> Fix the issue and run again.")
    #    sys.exit(1)
        
    
    # Step 5: Clean up video file
    # log.info("Step 5: Cleaning up video file...")
    # try:
    #     os.remove(video_path)
    #     log.info("Video file deleted successfully.")
    # except Exception as e:
    #     log.warning("Error deleting video file: %s", e)
    #     log.warning("Please check the file and delete it manually.")
    
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------
    # PAUSED: TikTok Video Pipeline (renderer.py, tiktok_client.py)
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------

    
if __name__ == "__main__":
    run()