import re
import pandas as pd
import os

class AnkiFormatter:
    @staticmethod
    def format_latex_html(text):
        if not isinstance(text, str): return ""
        
        # Standardize line breaks
        text = text.replace("\r\n", "\n")
        
        # Convert LaTeX for Anki
        # Block math: $$...$$ -> \[ ... \]
        text = re.sub(r"\$\$(.+?)\$\$", r"\[ \1 \]", text, flags=re.DOTALL)
        
        # Inline math: $...$ -> \( ... \)
        text = re.sub(r"\$(.+?)\$", r"\( \1 \)", text)
        
        # Convert newlines to HTML breaks
        text = text.replace("\n\n", "<br><br>").replace("\n", "<br>")
        return text.strip()

    @staticmethod
    def export_tsv(cards: list, output_path: str):
        data = []
        for card in cards:
            front = AnkiFormatter.format_latex_html(card.front)
            back = AnkiFormatter.format_latex_html(card.back)
            
            # Anki tags are space-separated, so we replace spaces within tags with underscores
            tags = " ".join([t.replace(" ", "_") for t in card.tags])
            
            data.append({"Front": front, "Back": back, "Tags": tags})
            
        df = pd.DataFrame(data)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, sep="\t", index=False, header=False, encoding="utf-8")