# Central Utility Scripts (utility-deck)

A collection of general-purpose scripts for file processing, document conversion, and audio transcription.

## 🚀 Installation

You can install this toolkit directly from GitHub using `pip`. This will automatically install all dependencies and register the terminal CLI commands:

```bash
pip install git+https://github.com/Khumee/utility-deck.git
```

*Note: For the PDF conversion tools, you will also need to install the Playwright browser dependencies:*
```bash
playwright install chromium
```

---

## 🛠️ CLI Commands (Terminal Shortcuts)

Once installed, you can run these commands directly from **any directory** in your terminal:

### 1. **`audio-transcribe`**
Transcribes audio files (like `.mp3`, `.ogg`, `.wav`) to text using Google's Gemini API:
```bash
# Set your API Key first (e.g. in Windows PowerShell)
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_api_key", "User")

# Run transcription
audio-transcribe --file "my_recording.ogg" --language "Urdu"
```
* [View setup & usage details](./audio_transcriber/)

### 2. **`html-to-pdf`**
Converts HTML pages or folders of HTML files into print-ready A4 PDFs:
```bash
html-to-pdf --input "document.html" --output "output.pdf"
```
* [View setup & usage details](./html_to_pdf/)

### 3. **`md-to-pdf`**
Converts Markdown `.md` documents directly to PDF format:
```bash
md-to-pdf "document.md" "output.pdf"
```
* [View setup & usage details](./md_to_pdf/)

### 4. **`extract-pdf`**
Extracts plain text contents from a PDF file:
```bash
extract-pdf "document.pdf"
```
* [View setup & usage details](./extract_pdf/)
