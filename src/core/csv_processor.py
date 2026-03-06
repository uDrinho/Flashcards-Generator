import pandas as pd
from src.core.models import Flashcard
from typing import List

def load_flashcards_from_csv(file_path: str) -> List[Flashcard]:
    """
    Lê um arquivo CSV e retorna uma lista de objetos Flashcard.
    Usa 'sep=None' para detectar automaticamente se o separador é ',' ou ';'.
    """
    # O engine='python' é necessário para usar a detecção automática de separador
    df = pd.read_csv(file_path, sep=None, engine='python')
    
    cards = []
    for _, row in df.iterrows():
        # Acessamos por índice (0 e 1) para ignorar os nomes das colunas
        question = str(row.iloc[0])
        answer = str(row.iloc[1])
        
        cards.append(Flashcard(
            front=question,
            back=answer,
            tags=["csv_import", "calculo_numerico"]
        ))
    return cards