import os
import textwrap
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from autopost.models.quote import Quote

load_dotenv()

class PostRenderer:
    def __init__(self):
        self.template_path = Path(os.getenv("TEMPLATE_PATH"))
        self.output_dir = Path(os.getenv("OUTPUT_DIR"))
        self.output_dir.mkdir(exist_ok=True)
        
    def render(self, quote: Quote) -> Path:
        img = Image.open(self.template_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        
        canvas_width, canvas_height = img.size
        font = ImageFont.load_default(size=26)
        author_font = ImageFont.load_default(size=20)
        
        # Wrap the quote text so it fits within 80% of the canvas width
        max_chars = int(canvas_width * 0.8 / 16)
        
        # Wrap the quote text into multiple lines so it doesn't run off the edge.
        wrapped_lines = textwrap.wrap(quote.text, width=max_chars)
        
        # Calculate total text block height
        line_height = 30
        author_gap = 60
        block_height = len(wrapped_lines) * line_height + author_gap
        
        # Start y position so the whole block is vertically centered
        y = (canvas_height - block_height) / 2
        
        # Draw each line of the quote, horizontally centered
        for line in wrapped_lines:
            bbox = draw.textbbox((0,0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (canvas_width - line_width) // 2
            draw.text((x, y), line , font=font, fill=(30, 30, 30))
            y += line_height
            
        # Draw the author name below the quote
        author_text = quote.author
        bbox = draw.textbbox((0, 0), author_text, font=author_font)
        author_width = bbox[2] - bbox[0]
        x = (canvas_width - author_width) // 2
        draw.text((x, y + 20), author_text, font=author_font, fill=(60, 60, 60))
        
        # Save the rendered image to the output directory
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = self.output_dir / f"post_{timestamp}.png"
        img.save(output_path)
        
        return output_path