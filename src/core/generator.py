import os
import instructor
from functools import lru_cache
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from .models import FlashcardSet

# --- Configuration & Factory ---

@lru_cache
def get_client() -> instructor.Instructor:
    """
    Creates and caches the Instructor client.
    Uses @lru_cache to ensure we strictly have one instance (Singleton).
    """
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434/v1")
    api_key = os.getenv("OLLAMA_API_KEY", "ollama")

    return instructor.from_openai(
        OpenAI(
            base_url=host,
            api_key=api_key,
        ),
        mode=instructor.Mode.JSON,
    )

def generate_flashcards(text_chunk: str, model: str = "llama3.2") -> FlashcardSet:
    """
    Sends a text chunk to Ollama and returns validated Flashcard objects.
    """
    client = get_client()
    # SYSTEM PROMPT: Enforcing strict LaTeX syntax for math
    system_prompt = """
    You are a university assistant specializing in creating high-quality Anki flashcards.
    
    RULES:
    1. Output MUST be a valid JSON object.
    2. The content (Front/Back) MUST be in PORTUGUESE (pt-BR).
    3. Use LaTeX ($...$) for ALL mathematical formulas.
    4. STRICT MATH FORMATTING:
       - For fractions, YOU MUST USE \\frac{numerator}{denominator}.
       - NEVER use "/" for division in formulas (e.g., use \\frac{a}{b}, not a/b).
       - Ensure variables are properly separated (e.g., "24EI" should not merge with previous terms).
    5. Be concise on the 'Front' and educational on the 'Back'.
    """

    # USER PROMPT: Providing a math-heavy example to guide the model
    user_prompt = f"""
    Analyze the text and extract key concepts.
    
    REQUIRED JSON FORMAT:
    {{
      "cards": [
        {{
          "front": "Qual a fórmula da tensão normal média?",
          "back": "A tensão é dada por: $\\sigma = \\frac{F}{A}$",
          "tags": ["resmat"]
        }}
      ]
    }}

    TEXT TO ANALYZE:
    {text_chunk}
    """

    try:
        resp = client.chat.completions.create(
            model=model,
            response_model=FlashcardSet,
            max_retries=3, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1, 
        )
        return resp

    except Exception as e:
        print(f"Error generating cards with model {model}: {e}")
        return FlashcardSet(cards=[])