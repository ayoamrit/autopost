import os
from tiktok_uploader.upload import upload_video
from  logger import get_logger

log = get_logger(__name__)

COOKIES_PATH = "cookies.txt"


# Function to upload the video to TikTok using the tiktok-uploader library
# Parameters:
# - video_path: the file path of the video to upload
# - caption: the caption for the TikTok video
# Returns True if the upload succeeded, False otherwise.
def upload_to_tiktok(video_path: str, caption: str) -> str:
    
    # Make sure the video file exists before attempting to upload
    if not os.path.exists(video_path):
        log.error("Error: Video file not found at %s", video_path)
        return False
    
    # Make sure the cookies file exists before attempting to upload
    if not os.path.exists(COOKIES_PATH):
        log.error("Error: TikTok cookies file not found at %s", COOKIES_PATH)
        return False
    
    log.info("Uploading video to TikTok...")
    log.info("Video: %s", video_path)
    log.info("Caption: %s", caption)
    
    try:
        upload_video(filename=video_path, description=caption, cookies=COOKIES_PATH, headless=True)
        log.info("Video uploaded successfully!")
        return True
    except Exception as e:
        log.error("Error uploading video: %s", e)
        return False
    