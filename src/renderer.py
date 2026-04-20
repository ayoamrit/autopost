# Handle video creatiion by overlaying the quote text and date onto a template video.
# The template is pre-made Canva video stored in the assets/ folder.
# Pillow draws the text into a transparent image, which is then composited on top of the video using moviepy.

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from logger import get_logger

log = get_logger(__name__)

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
        log.error("Error: could not load font at %s. Loading default font instead.", FONT_PATH)
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


# Function to create the text overlay image with the quote and date.
# Returns a nummpy array for MoviePy to use as an ImageClip.
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


# Main function to create the video with the quote and date overlay.
# Returns the path to the created video file.
def create_video(quote: dict, today: str) -> str:
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    if not os.path.exists(TEMPLATE_PATH):
        log.error("Error: template video not found at %s", TEMPLATE_PATH)
        sys.exit(1)
    
    log.info("Loading template video...")
    clip = VideoFileClip(TEMPLATE_PATH)
    W, H = clip.size
    log.info("Template video loaded with resolution %s x %s", W, H)
    
    log.info("Creating text overlay...")
    overlay_array = make_overlay(W, H, quote["text"], today)
    
    overlay_clip = (
        ImageClip(overlay_array).with_duration(clip.duration)
    )
    
    log.info("Compositing final video...")
    final_clip = CompositeVideoClip([clip, overlay_clip])
    output_path = os.path.join(DOWNLOAD_DIR, "quote_video.mp4")
    
    log.info("Exporting video to %s...", output_path)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=clip.fps, logger=None)
    
    clip.close()
    log.info("Video creation complete!")
    return output_path
