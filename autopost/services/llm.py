import os
from dotenv import load_dotenv
import google.generativeai as genai
from autopost.models.quote import Quote

load_dotenv()

class CaptionGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        model_name = os.getenv("GEMINI_MODEL")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
    def generate(self, quote: Quote) -> str:
        prompt = f"""
        You are a social media copywriter for an inspirational quote page.

        Write an Instagram caption for this quote:
        "{quote.text}" — {quote.author}

        Rules:
        - Write 2-3 engaging sentences that expand on the quote's theme
        - Do NOT repeat the quote itself in the caption
        - End with 20 relevant hashtags
        - Keep the tone warm and inspiring

        Output only the caption and hashtags, nothing else.
        """
        
        response = self.model.generate_content(prompt)
        return response.text.strip()