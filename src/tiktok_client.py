import os
from tiktok_uploader.upload import upload_video

VIDEO_PATH = "output/quote_video.mp4"
COOKIES_PATH = "cookies.txt"

def upload_to_tiktok(video_path: str, caption: str) -> str:
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return False
    
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
    
    
if __name__ == "__main__":
    test_caption = "This is a test caption for the TikTok video."
    success = upload_to_tiktok(VIDEO_PATH, test_caption)
    
    if success:
        print("Check your TikTok account to see the uploaded video!")
    else:
        print("Failed to upload video to TikTok.")
    
    