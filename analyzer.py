import google.generativeai as genai
import os
from dotenv import load_dotenv
from prompts import get_analysis_prompt, get_keyword_prompt

load_dotenv()


def setup_gemini():
    """Configure and return a Gemini model instance."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Please set it in your .env file.")
    genai.configure(api_key=api_key)
    # gemini-1.5-flash: fast, cheap, good enough for text analysis
    model = genai.GenerativeModel("gemini-2.5-flash")
    return model


def analyze_resume(resume_text, target_role):
    """Send resume to Gemini for full structured analysis."""
    model = setup_gemini()
    prompt = get_analysis_prompt(resume_text, target_role)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting analysis: {str(e)}"


def get_keyword_match(resume_text, target_role):
    """Send resume for keyword match percentage against target role."""
    model = setup_gemini()
    prompt = get_keyword_prompt(resume_text, target_role)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
