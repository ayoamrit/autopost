# Creates a quote image by overlaying text onto an author-specific template.
# Each author has their own background image in assets/images/.

# Text layout (caliberated against the 1080x1350 Canva template):
# - Text area: X = 108, Y = 865.8, Width = 864px (centered in 1080px)
# - Font: Palatino Linotype, size 24, white
# - Background: solid black rectangle behind all lines, Spread = 50px, Opacity = 1

import os
import sys
from PIL import Image, ImageDraw, ImageFont

# File paths
IMAGES_DIR = "assets/images"
OUTPUT_DIR = "output"
FONT_PATH = "assets/PALA.TTF"

# Font settings
FONT_SIZE = 28

# Text area settings
TEXT_X = 108
TEXT_Y = 865.8
TEXT_W = 864
CENTER_X = TEXT_X + TEXT_W // 2

# Background settings
BG_SPREAD = 20
BG_COLOR = (0, 0, 0, 255)  # Solid black
TEXT_COLOR = (255, 255, 255)  # White


# Returns the expected template image path for a given author.
# Example: "Fyodor Dostoevsky" -> "assets/images/template_fyodor_dostoevsky.jpg"
# Falls back to template_default.png if the author's template does not exist.
def get_template_path(author: str) -> str:
    safe_name = author.lower().replace(" ", "_").replace(".", "")
    template_path = os.path.join(IMAGES_DIR, f"template_{safe_name}.png")
    
    if not os.path.exists(template_path):
        print(f"Warning: Template for '{author}' not found. Using default template.")
        fallback_path = os.path.join(IMAGES_DIR, "template_default.png")
        
        if not os.path.exists(fallback_path):
            print("Error: Default template not found. Please ensure 'template_default.png' exists in the images directory.")
            sys.exit(1)
        
        print(f"Using fallback template: {fallback_path}")
        return fallback_path
    
    return template_path


# Function to load the specificed font at the given size.
# Falls back to the default PIL font if the font file cannot be loaded
def load_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except IOError:
        print(f"Error: could not load font at {FONT_PATH}. Loading default font instead.")
        return ImageFont.load_default()
    
    
# Function that splits text into lines that each fit within max_width pixels.
# Returns a list of strings (one per line).
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

def create_image(quote: dict, today: str) -> str:
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get the template path for the quote's author, with fallback to default if not found.
    template_path = get_template_path(quote["author"])
    print(f"Using template: {template_path}")
    
    # Load template as RGBA to composte transparent layers
    img = Image.open(template_path).convert("RGBA")
    W, H = img.size
    print(f"Template loaded - size: {W}x{H}")
    
    # Load font
    font = load_font(FONT_SIZE)
    
    # Wrap quote text into lines that fit within the text area width
    lines = wrap_text(quote["text"], font, TEXT_W)
    
    # Measure the full text block height
    draw = ImageDraw.Draw(img)
    line_h = draw.textbbox((0, 0), "Ag", font=font)[3]
    line_gap = int(line_h * 0.30)
    block_h = len(lines) * line_h + (len(lines) - 1) * line_gap
    
    # Draw solid black background rectangle 
    bg_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg_layer)
    
    # Calculate the bounding box of the text block
    text_left = TEXT_X - BG_SPREAD
    text_top = int(TEXT_Y) - BG_SPREAD
    text_right = TEXT_X + TEXT_W + BG_SPREAD
    text_bottom = int(TEXT_Y) + block_h + BG_SPREAD
    
    bg_draw.rectangle(
        [text_left, text_top, text_right, text_bottom],
        fill=BG_COLOR
    )
    
    # Composite the background layer onto the template
    img = Image.alpha_composite(img, bg_layer)
    
    # Draw each line of the text, centered within the text area
    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    
    y = int(TEXT_Y)
    for line in lines:
        bbox = text_draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        x = CENTER_X - line_w // 2
        
        text_draw.text((x, y), line, font=font, fill=TEXT_COLOR)
        y += line_h + line_gap
        
    img = Image.alpha_composite(img, text_layer)
    
    # Save the final image as PNG
    output_path = os.path.join(OUTPUT_DIR, "quote_image.png")
    img.convert("RGB").save(output_path, "PNG")
    
    print(f"Image saved to: {output_path}")
    return output_path


