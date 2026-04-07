from tiktok_uploader.upload import upload_video

VIDEO_PATH = "output/quote_video.mp4"
COOKIES_PATH = "cookies.txt"
DESCRIPTION = "Daily Quote"

print("Uploading video to TikTok...")
upload_video(filename=VIDEO_PATH, description=DESCRIPTION, cookies=COOKIES_PATH)
print("Video uploaded successfully!")