# Generates a TikTok caption and relevant hashtags for a given quote using Google Gemini (LLM).
# The model name is loaded from the .env file so it can be easily switched between different Gemini models without touching the code.

import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

# Configure Gemini with credentials from .env file
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL")
genai.configure(api_key=api_key)


# Function to generate a caption and relevant hashtags for a given quote.
# Quote dictionary is required with "text", "author", and "book" keys.
# Returns a dictionary with "caption" and "hashtags" keys.
def generate_caption(quote: dict) -> dict:
    prompt = f"""
    You are a social media manager for a quotes TikTok account.
    Here is today's quote:
    "{quote['text']}" — {quote['author']} — {quote['book']}
    
    Write the following for a TikTok video caption:
    1. A short, engaging caption (2-3 sentences max) that expands on the quote's theme without repeating it.set
        - Speak directly to the viewer using "you"set
        - Make it feel personal and thought-provoking, not generic
        - Do NOT use emojis
    2. A single line of 4 to 5 relevant hashtags seperated by spaces
        - Mix broad and niche hashtags related to the quote's themes (e.g. #inspiration, #literature, #selfgrowth)
        
    Reply in this exact format and nothing else:
    CAPTION: <your caption here>
    HASHTAGS: <your hashtags here>
    """
    
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    raw = response.text.strip()
    
    # Gemini is prompted with instructions to generate the caption and hashtags in a specific format, so we can easily parse the response.
    caption = ""
    hashtags = ""
    
    for line in raw.splitlines():
        if line.startswith("CAPTION:"):
            caption = line.replace("CAPTION:", "").strip()
        elif line.startswith("HASHTAGS:"):
            hashtags = line.replace("HASHTAGS:", "").strip()
            
            
    # If parsing fails for any reason, use safe defaults so the pipeline can continue without interruption.
    # This way, something will still be posted even if the LLM response format changes or there's an issue with the model.
    if not caption:
        print("⚠️ Warning: Could not parse caption from Gemini response. (Using fallback caption.)")
        caption = f"{quote['text']} - {quote['author']}"
        
    if not hashtags:
        print("⚠️ Warning: Could not parse hashtags from Gemini response. (Using fallback hashtags.)")
        hashtags = "#quotes #dailyquotes #fyp #fyp #quoteoftheday"
    
    print(f"Generated caption: {caption}")
    print(f"Generated hashtags: {hashtags}")
    
    return{
        "caption": caption,
        "hashtags": hashtags
    }
    