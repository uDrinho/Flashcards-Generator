import typer
from pathlib import Path
from src.core.extractor import extract_text_from_pdf
from src.core.generator import generate_flashcards
from src.core.formatter import AnkiFormatter
from src.core.csv_processor import load_flashcards_from_csv
from rich.progress import track
from rich import print

app = typer.Typer()

@app.command()
def csv(
    input_file: Path = typer.Argument(..., help="Path to the CSV file (2 columns: Question, Answer)"),
    output_file: Path = typer.Argument("data/output/csv_deck.tsv", help="Output TSV file path")
):
    """
    Flashcards-Generator (CSV mode): Directly converts CSV into Anki TSV with LaTeX/HTML formatting.
    No LLM is used.
    """
    if not input_file.exists():
        print(f"[bold red]File not found: {input_file}[/bold red]")
        return

    print(f"[bold green]Reading CSV: {input_file.name}...[/bold green]")
    
    try:
        all_cards = load_flashcards_from_csv(str(input_file))
    except Exception as e:
        print(f"[bold red]Error reading CSV: {e}[/bold red]")
        return

    if all_cards:
        AnkiFormatter.export_tsv(all_cards, str(output_file))
        print(f"\n[bold green]Success![/bold green] {len(all_cards)} cards saved to: {output_file}")
    else:
        print("\n[bold yellow]No cards were found in the CSV.[/bold yellow]")

@app.command()
def process(
    input_dir: Path = typer.Argument(..., help="Directory containing PDF files"),
    output_file: Path = typer.Argument("data/output/deck.tsv", help="Output TSV file path")
):
    """
    Flashcards-Generator: Converts PDFs into Anki-ready TSV files using local LLM.
    """
    all_cards = []
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("[bold red]No PDF files found in the specified directory.[/bold red]")
        return

    print(f"[bold green]Starting Flashcards-Generator with {len(pdf_files)} file(s)...[/bold green]")

    for pdf in pdf_files:
        print(f"\nProcessing file: [bold cyan]{pdf.name}[/bold cyan]")
        
        # 1. Extraction
        try:
            raw_text = extract_text_from_pdf(str(pdf))
        except Exception as e:
            print(f"[red]Failed to read {pdf.name}: {e}[/red]")
            continue
        
        # 2. Chunking (Reduced size to 2000 to improve local model stability)
        chunk_size = 2000
        chunks = [raw_text[i:i+chunk_size] for i in range(0, len(raw_text), chunk_size)]
        
        # 3. Generation
        for i, chunk in track(enumerate(chunks), description="Generating cards...", total=len(chunks)):
            # Skip very small chunks (usually artifacts or references)
            if len(chunk) < 100: 
                continue
            
            result = generate_flashcards(chunk)
            if result and result.cards:
                all_cards.extend(result.cards)

    # 4. Export
    if all_cards:
        AnkiFormatter.export_tsv(all_cards, str(output_file))
        print(f"\n[bold green]Success![/bold green] {len(all_cards)} cards saved to: {output_file}")
    else:
        print("\n[bold yellow]No cards were generated.[/bold yellow]")

if __name__ == "__main__":
    app()