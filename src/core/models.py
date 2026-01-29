from pydantic import BaseModel, Field
from typing import List

class Flashcard(BaseModel):
    front: str = Field(..., description="The question or concept. Must be concise. Use inline LaTeX ($...$) for math.")
    back: str = Field(..., description="The detailed answer. Explain the 'why'. Use block LaTeX ($$...$$) if needed.")
    tags: List[str] = Field(default_factory=list, description="List of 1-3 short tags (e.g., 'algebra', 'kernel').")

class FlashcardSet(BaseModel):
    cards: List[Flashcard]