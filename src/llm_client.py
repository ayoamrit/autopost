# Generates a TikTok caption and relevant hashtags for a given quote using Google Gemini (LLM).
# The model name is loaded from the .env file so it can be easily switched between different Gemini models without touching the code.

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from logger import get_logger

load_dotenv()
log = get_logger(__name__)

# Configure Gemini with credentials from .env file
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL")

# Validate environment variables and provide clear error messages if they are missing
if not api_key:
    raise EnvironmentError("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")

if not model_name:
    raise EnvironmentError("Gemini model name not found. Please set GEMINI_MODEL in your .env file.")

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
    1. A short, engaging caption (4-5 sentences max) that expands on the quote's theme without repeating it.
        - Speak directly to the viewer using "you"
        - Make it feel personal and thought-provoking, not generic
        - Do NOT use emojis
    2. A single line of 4 to 5 relevant hashtags seperated by spaces
        - Mix broad and niche hashtags related to the quote's themes (e.g. #inspiration, #literature, #selfgrowth)
        
    You must reply with a valid JSON object and nothing else (no preamble, no explanation, no markdown code fences). Exactly this structure:
    {{"caption": "your caption here", "hashtags": "#hashtag1 #hashtag2 #hashtag3"}}
    """
    
    log.info("Requesting caption and hashtags from Gemini (%s)...", model_name)
    
    try: 
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        
        # Validate the response
        if not response or not response.text:
            log.warning("Gemini response is empty. Using fallback caption and hashtags.")
            return _fallback(quote)
        
        raw = response.text.strip()
        log.debug("Raw Gemini response: %s", raw)
        
        # Parse the response as JSON
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
            
        parsed = json.loads(raw)
        caption = parsed.get("caption", "").strip()
        hashtags = parsed.get("hashtags", "").strip()
        
        # Validate the parsed content
        if not caption:
            log.warning("Gemini returned empty caption. Using fallback caption.")
            caption = _fallback(quote)["caption"]
    
        if not hashtags:
            log.warning("Gemini returned empty hashtags. Using fallback hashtags.")
            hashtags = _fallback(quote)["hashtags"]
            
        log.info("Caption: %s", caption)
        log.info("Hashtags: %s", hashtags)
        
        return {"caption": caption, "hashtags": hashtags}
    
    except json.JSONDecodeError as e:
        # The response from Gemini was not valiid JSON.
        # This can happen if the model doesn't follow instructions correctly or if there's an issue with the response formatting.
        log.warning("Could not parse Gemini JSON response: %s. Using fallback caption and hashtags.", e)
        return _fallback(quote)
    
    except Exception as e:
        # Catch-all other exception that may occur during the API call or response processing.
        log.error("Gemini API call failed: %s. Using fallback caption and hashtags.", e)
        return _fallback(quote)
        
        

# Function to provide a fallback caption and hashtags in case the Gemini API call fails or returns an invalid response.
def _fallback(quote: dict) -> dict:
    return {
        "caption": f"{quote.get('text', '')}",
        "hashtags": "#quotes #dailyquotes #fyp #literature #quoteoftheday"
    }  
        
    