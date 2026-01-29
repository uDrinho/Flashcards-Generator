# Flashcards-Generator

A robust, privacy-focused tool that converts technical PDF documents into high-quality Anki flashcards with proper Latex formatation. It leverages local Large Language Models (LLMs) to ensure data privacy and zero cost.

## Overview

Flashcards-Generator is designed for students who need reliable study materials. Unlike generic summarizers, this tool uses a structured extraction pipeline to:
1. Read PDF documents.
2. Extract key concepts using a local LLM (Ollama).
3. Enforce strict JSON output for stability.
4. Generate flashcards in **Portuguese (pt-BR)**, even if the source text is in English.
5. Format mathematical formulas with rigorous LaTeX syntax (e.g., `\frac{a}{b}`).

## Features

* **100% Local & Free:** Runs entirely on your machine using Ollama. No API keys or credit cards required.
* **Strict Math Formatting:** specifically engineered to handle complex formulas, ensuring fractions and variables render correctly in Anki.
* **Structured Data Validation:** Uses `Instructor` and `Pydantic` to validate every single output from the LLM, preventing broken import files.
* **Portuguese Output:** The system prompt is hardcoded to translate and synthesize concepts into Portuguese, making it ideal for non-native English speakers studying technical docs.
* **Batch Processing:** Capable of processing entire directories of PDFs in one go.

## Known Limitations & Areas for Improvement

While functional, this project relies on local hardware resources. Consider the following:

* **Hardware Dependency (Speed):** Generation speed is directly tied to your CPU/GPU.
    * *High-End (M1/M2/M3 Mac, RTX GPU):* Very fast generation.
    * *Mid-Range (Modern i5/i7):* Acceptable speeds (~5-15 seconds per chunk).
    * **Low-End / Older PCs:** Generation may be **slow**. Since the model runs locally, older CPUs may take significant time to process large PDFs.
* **Model Intelligence:** We currently recommend `llama3.2` for speed. However, larger models (like `llama3.3` or `mistral`) may produce better summaries but will require more RAM and processing power.
* **PDF Complexity:** Scanned PDFs (images) are not currently supported (OCR is not implemented yet). The tool works best with text-selectable PDFs.

## Requirements

* **Python 3.10+**
* **Ollama:** You must have Ollama installed and running.
* **Hardware:** A decent CPU (modern i5/i7) or any discrete GPU is recommended for reasonable generation speeds.

## Installation

1.  **Install Ollama**
    Follow the instructions at [ollama.com](https://ollama.com).
    Once installed, pull the required model (Llama 3.2 is recommended for the balance of speed/quality):
    ```bash
    ollama pull llama3.2
    ```

2.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/Flashcards-Generator.git](https://github.com/yourusername/Flashcards-Generator.git)
    cd Flashcards-Generator
    ```

3.  **Set Up Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Prepare your Data**
    Place your PDF files into the `data/input/` directory.

2.  **Run the Generator**
    Execute the main script. You can specify the input directory and the output file path.
    ```bash
    python main.py data/input data/output/deck.tsv
    ```

3.  **Import to Anki**
    * Open Anki.
    * Select **File > Import**.
    * Choose the generated `.tsv` file.
    * Ensure **"Allow HTML in fields"** is checked.
    * Field mapping should be: `Field 1 -> Front`, `Field 2 -> Back`, `Field 3 -> Tags`.

## Project Structure

* `src/core/`: Contains the core logic modules.
    * `extractor.py`: Handles PDF text extraction.
    * `generator.py`: Interfaces with the local Ollama instance; contains the prompts and validation logic.
    * `formatter.py`: Cleans and formats text into Anki-compatible HTML/LaTeX.
    * `models.py`: Pydantic data structures.
* `data/`: Directory for input files and output artifacts (ignored by git).
* `main.py`: CLI entry point.

## Privacy Note

This tool processes data locally. No text from your PDFs is sent to external cloud servers (like OpenAI or Anthropic). Your documents remain private on your machine.
