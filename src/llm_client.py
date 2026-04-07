import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL")
genai.configure(api_key=api_key)

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
    
    # Parse the response to extract the caption and hashtags
    caption = ""
    hashtags = ""
    
    for line in raw.splitlines():
        if line.startswith("CAPTION:"):
            caption = line.replace("CAPTION:", "").strip()
        elif line.startswith("HASHTAGS:"):
            hashtags = line.replace("HASHTAGS:", "").strip()
            
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
    