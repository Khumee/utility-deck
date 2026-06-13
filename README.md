# Central Utility Scripts (utils)

A collection of general-purpose scripts for file processing, document conversion, and audio transcription.

## Table of Contents
1. [Audio Transcriber (`audio_transcriber.py`)](#1-gemini-audio-transcriber-audio_transcriberpy)
2. [HTML to PDF Converter (`html_to_pdf.py`)](#2-html-to-pdf-converter-html_to_pdfpy)
3. [Markdown to PDF Converter (`md_to_pdf.py`)](#3-markdown-to-pdf-converter-md_to_pdfpy)
4. [Extract PDF Text (`extract_pdf.py`)](#4-extract-pdf-text-extract_pdfpy)

---

## 1. Audio Transcriber (`audio_transcriber.py`)
Transcribes audio files (like `.mp3`, `.ogg`, `.wav`) to text using Google's Gemini API (via the new `google-genai` SDK supporting `AQ.` key formats).

### Setup:
```bash
pip install google-genai
```
Configure your API key in your environment variables:
* **Windows (PowerShell)**: `[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_key", "User")`
* **Linux/macOS**: `export GEMINI_API_KEY="your_key"`

### Usage:
```bash
python audio_transcriber.py --file "path/to/audio.ogg" --language "Urdu"
```
* Use `-f` or `--file` to specify the audio path.
* Use `-o` or `--output` to customize the output text file destination.
* Use `-m` or `--model` to change the Gemini model (default is `gemini-2.5-flash`).

---

## 2. HTML to PDF Converter (`html_to_pdf.py`)
Converts HTML files (or directories containing HTML files) to print-ready A4 PDFs using Playwright.

### Setup:
```bash
pip install playwright
playwright install chromium
```

### Usage:
```bash
# Convert a single HTML file
python html_to_pdf.py --input "document.html" --output "output.pdf"

# Convert a folder of HTML files
python html_to_pdf.py --input "C:\path\to\html_folder" --wait 3500
```
* Use `-w` or `--wait` to specify the delay (in milliseconds) to wait for fonts or web-assets to load before rendering.

---

## 3. Markdown to PDF Converter (`md_to_pdf.py`)
Converts Markdown `.md` documents directly to PDF.

### Usage:
```bash
python md_to_pdf.py "document.md" "output.pdf"
```

---

## 4. Extract PDF Text (`extract_pdf.py`)
Extracts text contents from target PDF documents.

### Usage:
```bash
python extract_pdf.py "document.pdf"
```
