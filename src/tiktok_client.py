import os
from tiktok_uploader.upload import upload_video

COOKIES_PATH = "cookies.txt"


# Function to upload the video to TikTok using the tiktok-uploader library
# Parameters:
# - video_path: the file path of the video to upload
# - caption: the caption for the TikTok video
# Returns True if the upload succeeded, False otherwise.
def upload_to_tiktok(video_path: str, caption: str) -> str:
    
    # Make sure the video file exists before attempting to upload
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return False
    
    # Make sure the cookies file exists before attempting to upload
    if not os.path.exists(COOKIES_PATH):
        print(f"Error: TikTok cookies file not found at {COOKIES_PATH}")
        return False
    
    print("Uploading video to TikTok...")
    print(f"Video: {video_path}")
    print(f"Caption: {caption}")
    
    try:
        upload_video(filename=video_path, description=caption, cookies=COOKIES_PATH, headless=True)
        print("Video uploaded successfully!")
        return True
    except Exception as e:
        print(f"Error uploading video: {e}")
        return False
    