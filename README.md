# Central Utility Scripts (utils)

A collection of general-purpose scripts for file processing, document conversion, and audio transcription.

## Tools Directory

Here is a list of the available tools. Click on any tool name to view its specific setup instructions and usage details:

1. **[Audio Transcriber](./audio_transcriber/)** (`audio_transcriber.py`):
   * Transcribes `.mp3`, `.ogg`, and `.wav` audio files directly to text using Google's Gemini API (via the new `google-genai` SDK).
   
2. **[HTML to PDF Converter](./html_to_pdf/)** (`html_to_pdf.py`):
   * Renders static HTML documents or entire folders of HTML files into print-ready A4 PDFs using Playwright.
   
3. **[Markdown to PDF Converter](./md_to_pdf/)** (`md_to_pdf.py`):
   * Converts Markdown documents (`.md`) to standard PDFs.
   
4. **[Extract PDF Text](./extract_pdf/)** (`extract_pdf.py`):
   * Utility for extracting plain text from PDF files.
