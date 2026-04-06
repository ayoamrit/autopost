import os
import sys
import numpy as np
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

load_dotenv()

# Constants for file paths and font settings
TEMPLATE_PATH = "assets/template.mp4"
DOWNLOAD_DIR = "output/"
FONT_PATH = "assets/PALA.TTF"
FONT_SIZE = 30

# Layout settings for the quote text and date
H_PADDING = 80
QUOTE_Y_RATIO = 0.38
DATE_GAP = 30


# Function to load the specificed font at the given size.
# Falls back to the default PIL font if the font file cannot be loaded
def load_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except IOError:
        print(f"Error: could not load font at {FONT_PATH}. Loading default font instead.")
        return ImageFont.load_default()
    
    
# Function to wrap text into multiple lines that each fir within max_width pixels.
# Return a list of strings (one per each line).
def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines = []
    line = ""
    dummy = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy)
    
    for word in words:
        test = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    
    if line:
        lines.append(line)
        
    return lines

def make_overlay(video_w: int, video_h: int, quote: str, today: str) -> np.ndarray:
    img = Image.new("RGBA", (video_w, video_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    custom_font = load_font(FONT_SIZE)
    text_area_w = video_w - (H_PADDING * 2)
    
    # Wrap and measure the quote
    lines = wrap_text(quote, custom_font, text_area_w)
    line_h = draw.textbbox((0, 0), "Ag", font=custom_font)[3]
    line_gap = int(line_h * 0.35)
    
    # Draw each line of the quote, centered horizontally
    quote_xaxis = 108
    quote_yaxis = 458.6
    for line in lines:
        bbox = draw.textbbox((quote_xaxis, quote_yaxis), line, font=custom_font)
        
        draw.text((quote_xaxis, quote_yaxis), line, font=custom_font, fill=(255, 255, 255, 255))
        
        quote_yaxis += line_h + line_gap
        
        
    # Draw the date below the quote
    date_yaxis = 270.8
    date_bbox = draw.textbbox((0, 0), today, font=custom_font)
    date_w = date_bbox[2] - date_bbox[0]
    date_xaxis = 108
    
    draw.text((date_xaxis, date_yaxis), today, font=custom_font, fill=(255, 255, 255, 255))
    
    return np.array(img)

def create_video(quote: dict, today: str) -> str:
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: template video not found at {TEMPLATE_PATH}")
        sys.exit(1)
    
    print("Loading template video...")
    clip = VideoFileClip(TEMPLATE_PATH)
    W, H = clip.size
    print(f"Template video loaded with resolution {W}x{H}")
    
    print("Creating text overlay...")
    overlay_array = make_overlay(W, H, quote["text"], today)
    
    overlay_clip = (
        ImageClip(overlay_array).with_duration(clip.duration)
    )
    
    print("Compositing final video...")
    final_clip = CompositeVideoClip([clip, overlay_clip])
    output_path = os.path.join(DOWNLOAD_DIR, "quote_video.mp4")
    
    print(f"Exporting video to {output_path}...")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=clip.fps, logger=None)
    
    clip.close()
    print("Video creation complete!")
    return output_path

# Test
if __name__ == "__main__":
    sample_quote = {
        "text": "It is our choices, Harry, that show what we truly are, far more than our abilities. It is our choices, Harry, that show what we truly are, far more than our abilities. It is our choices, Harry, that show what we truly are, far more than our abilities.",
        "author": "Albus Dumbledore",
        "book": "Harry Potter and the Chamber of Secrets"
    }
    today_str = date.today().strftime("%B %d, %Y")
    create_video(sample_quote, today_str)